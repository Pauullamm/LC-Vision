from pinecone import Pinecone
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

def query_db(query_vector):
  pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
  pc_index_name = os.getenv('PINECONE_INDEX_NAME')

  index = pc.Index(pc_index_name)

  query_results = index.query(
      vector=query_vector,
      top_k=3,
      include_metadata=True
  )
  contexts = [f"{item['metadata']['text']} (Score: {item['score']})" for item in query_results['matches']]
  
  augmented_query = "\n\n---\n\n".join(contexts) + "\n\n-----\n\n"
  print(augmented_query)
  return augmented_query