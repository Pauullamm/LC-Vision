from dotenv import load_dotenv
import os
from openai import OpenAI
import requests

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def embed_query(query, apikey, embed_model):
  client = OpenAI(api_key=apikey)
  return client.embeddings.create(input = [query], model=embed_model, dimensions=1536).data[0].embedding

def hf_embed(url:str, query:str, apikey:str) -> list[float]:
  headers = {'Authorization': 'Bearer ' + apikey,
          'x-wait-for-model': 'True'
          }
  payload = {
    'inputs': query
  }
  response = requests.post(url=url, headers=headers, json=payload)
  if response.status_code == 200:
        result = response.json()
        # The response contains embeddings; assuming it's the first element
        return result if isinstance(result, list) else None
  else:
      print(f"Error querying Hugging Face API: {response.status_code}, {response.text}")
      return None