#@title Generating embeddings with huggingface model and upsert to vector database
from sentence_transformers import SentenceTransformer
import os
import requests
from pinecone import Pinecone, ServerlessSpec, PineconeApiException
from tqdm import tqdm
import time
from dotenv import load_dotenv

load_dotenv()


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Pinecone settings
pc_api_key = os.getenv('PINECONE_API_KEY')
pc_index_name = os.getenv('PINECONE_INDEX_NAME')

# Initialize Pinecone
pc = Pinecone(api_key=pc_api_key)

# Check if the index exists, and create it if necessary
if pc_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pc_index_name,
        dimension=384,  # Update to match the dimensions of the model embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Ensure Pinecone index is ready
while not pc.describe_index(pc_index_name).status['ready']:
    time.sleep(1)

# Function to upsert embeddings to Pinecone
def upsert_to_pinecone(chunks, url_metadata, drug_name, doc_type):
    index = pc.Index(pc_index_name)

    for chunk in tqdm(chunks):
        chunk = chunk.strip()  # Clean line from any trailing spaces or newlines
        if chunk:
            # Get the embedding from Hugging Face model
            # 2. Encode
            embedding = model.encode([chunk])

            if embedding is not None:
                try:
                    # Upsert the vector into Pinecone with text as metadata
                    index.upsert([
                        {
                            'id': str(hash(chunk)),  # Unique ID for the line
                            'values': embedding[0],  # The embedding from Hugging Face
                            'metadata': {'url_storage_path': url_metadata,
                                        'drug_name': drug_name,
                                        'doc_type': doc_type
                                        }  # Store the original line as metadata
                        }
                    ])
                except PineconeApiException as e:
                    print(f"Error during batch upsert: {e}")
            else:
                print(f"Failed to get embedding for line: {chunk}")




