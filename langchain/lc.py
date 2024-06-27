from langchain.CustomDocLoader import CustomDocumentLoader
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
import os

api_key = os.environ["OPENAI_API_KEY"]
path_to_file = "formatted_text.txt"
loader = CustomDocumentLoader(path_to_file)
docs = loader.load()
llm = ChatOpenAI(openai_api_key=api_key, max_tokens=1000, model='gpt-4o')
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key, model='text-embedding-3-large', dimensions=1536)

vector_store = LanceDB.from_documents(
    documents=docs,
    embedding=embeddings_model
)