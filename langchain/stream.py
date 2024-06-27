from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from lc import llm, vector_store
from langchain.image_process import response

img_info = response.json()["choices"][0]["message"]["content"]

prompt = ChatPromptTemplate.from_template("""
Use the following context and any existing knowledge of medicines to answer the question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
If you don't know the answer, do not provide any information about manufacturers or drugs except that which is your most confident, but do explain why you don't know the answer. 
Use three sentences maximum and keep the answer as concise as possible.

{context}

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector_store.as_retriever()
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


retrieval_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question_to_ask = f"{img_info} - Based on the description mentioned, what drug does it describe and what is its manufacturer?"
output_message = retrieval_chain.invoke(question_to_ask)
for i in output_message.split("."):
  print(i)

user_response = input("How accurate is this response? If there is no answer, reply N/A, if the answer is wrong, say 'wrong' followed by the correct answer")

