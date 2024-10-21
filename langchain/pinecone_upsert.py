from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec, PineconeApiException
from dotenv import load_dotenv
import time, os
from tqdm import tqdm

# load keys
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pc_api_key = os.getenv('PINECONE_API_KEY')
pc_index_name = os.getenv('PINECONE_INDEX_NAME')
path_to_file = "upsert_data.txt"

# initialise pinecone
pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

if pc_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pc_index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# initialise embeddings model and generate embeddings
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key, model='text-embedding-3-large', dimensions=1536)

# Wait for the index to be ready
while not pc.describe_index(pc_index_name).status['ready']:
    time.sleep(1)

# Attempt to upsert data, and handle errors
print('Upserting Data...')
index = pc.Index(pc_index_name)
with open(path_to_file, 'r', encoding="utf8") as file:
    for line in tqdm(file):
        if line:
            vector = embeddings_model.embed_query(line.strip()) 
            try:
                # Upsert the vector into Pinecone with text as metadata
                index.upsert([
                    {
                        'id': str(hash(line)),  # Unique ID for the line (ensure it's unique)
                        'values': vector,
                        'metadata': {'text': line}  # Store the original line as metadata
                    }
                ])
            except PineconeApiException as e:
                print(f"Error during batch upsert: {e}")

print("All lines have been stored in Pinecone.")

