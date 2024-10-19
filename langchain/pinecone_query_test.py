from pinecone import Pinecone
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
pc_index_name = os.getenv('PINECONE_INDEX_NAME')

index = pc.Index(pc_index_name)

query_vector = np.random.rand(1536).tolist()  # Random vector for demonstration

query_results = index.query(
    vector=query_vector,
    top_k=3,
    include_values=True
)

print(query_results)