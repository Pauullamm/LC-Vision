from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def embed_query(query, apikey, embed_model):
  client = OpenAI(api_key=apikey)
  return client.embeddings.create(input = [query], model=embed_model, dimensions=1536).data[0].embedding