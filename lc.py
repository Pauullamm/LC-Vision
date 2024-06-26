from im_t import response
from CustomDocLoader import CustomDocumentLoader
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

import os

api_key = os.environ["OPENAI_API_KEY"]
path_to_file = ""
img_info = response.json()["choices"][0]["message"]["content"]
loader = CustomDocumentLoader(path_to_file)
docs = loader.load()
llm = ChatOpenAI(openai_api_key=api_key, max_tokens=1000, model='gpt-4-turbo')
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key, model='text-embedding-3-large', dimensions=1536)