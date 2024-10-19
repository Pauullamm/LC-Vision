from CustomDocLoader import CustomDocumentLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec, PineconeApiException
from dotenv import load_dotenv
import time, os

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


#load documents
loader = CustomDocumentLoader(path_to_file)
docs = loader.load()

# initialise embeddings model and generate embeddings
llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens=1000, model='gpt-4o')
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key, model='text-embedding-3-large', dimensions=1536)
embeddings = embeddings_model.embed_documents([doc.page_content for doc in docs])  # Assuming docs is a list of Document objects
upsert_data = [(str(i), embedding) for i, embedding in enumerate(embeddings)]

# Wait for the index to be ready
while not pc.describe_index(pc_index_name).status['ready']:
    time.sleep(1)

# Attempt to upsert data, and handle errors
index = pc.Index(pc_index_name)
try:
    index.upsert(vectors=upsert_data)
except PineconeApiException as e:
    if e.code == 11:  # Error code for "message length too large"
        print("Payload too large, switching to batch upsert...")
        
        # Perform batch upsert
        batch_size = 100  # Adjust this size as needed
        for i in range(0, len(upsert_data), batch_size):
            try:
                index.upsert(vectors=upsert_data[i:i + batch_size])
            except PineconeApiException as batch_e:
                print(f"Error during batch upsert: {batch_e}")

    else:
        print(f"Error during upsert: {e}")

