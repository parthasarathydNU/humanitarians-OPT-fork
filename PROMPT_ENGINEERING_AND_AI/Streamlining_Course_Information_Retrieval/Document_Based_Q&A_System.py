# Import necessary libraries and modules

import os
import streamlit as st
import pinecone
from openai import OpenAI 
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from pinecone import Pinecone, PodSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.prompts import PromptTemplate

# Set up the environment

# Load secret keys
secrets = st.secrets

# Access OpenAI API key
openai_api_key = secrets["openai"]["api_key"]

# Access Pinecone API key
pinecone_api_key = secrets["pinecone"]["api_key"]

# Add a file uploader widget
uploaded_file = st.file_uploader("Upload your file")

if uploaded_file is not None:
    # Process the uploaded file
    # You can perform any necessary operations here
    file_contents = uploaded_file.read()
    loader = st.write("File contents:", file_contents)
    pages = loader.load()

# Split the documents into smaller chunks for processing

def split_docs(pages, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

docs = split_docs(pages)

# Embed the documents

embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create a new Pinecone Index and setup the vector database and search engine

index_name = "langchain-demo"
index = PineconeVectorStore.from_documents(docs, embeddings_model, index_name=index_name)

# Define a function to find similar documents based on a given query

def get_similiar_docs(query, k=1, score=False):
    if score:
        similar_docs = index.similarity_search_with_score(query, k=k)
    else:
        similar_docs = index.similarity_search(query, k=k)
    return similar_docs

# Creating the Prompt

template = """
Answer the question in your own words from the context given to you.
If questions are asked where there is no relevant context available, please answer from what you know.

Context: {context}

Human: {question}
Assistant:

"""

prompt = PromptTemplate(
    input_variables=["context", "question"], template=template
)

# Assigning the OPENAI model and Retrieval chain

model_name = "gpt-4"
llm = ChatOpenAI(model_name=model_name)

chain = RetrievalQA.from_chain_type(llm, retriever=index.as_retriever(),chain_type_kwargs={'prompt': prompt}
    )

# Define Response Function

def get_answer(query):
    similar_docs = get_similiar_docs(query)
    answer = chain({"query":query})
    return answer

# Streamlit Application

st.title("Streamlit Langchain Application")

question_input = st.text_input("Ask your question here:")

if st.button("Get Answer"):
    answer = get_answer(question_input)
    st.write("Answer:", answer)
