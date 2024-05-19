# Import necessary libraries and modules
import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
import pinecone
from pinecone import Pinecone, PodSpec
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import streamlit as st
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader, UnstructuredPowerPointLoader, DirectoryLoader
import os.path
import pathlib
import tempfile


## Set up the environment
# Load secret keys

secrets = st.secrets  # Accessing secrets (API keys) stored securely

openai_api_key = secrets["openai"]["api_key"]  # Accessing OpenAI API key from secrets
os.environ["OPENAI_API_KEY"] = openai_api_key  # Setting environment variable for OpenAI API key

pinecone_api_key = secrets["pinecone"]["api_key"]  # Accessing Pinecone API key from secrets
os.environ["PINECONE_API_KEY"] = pinecone_api_key  # Setting environment variable for Pinecone API key

# Initializing Pinecone with API key
pc = Pinecone(pinecone_api_key=pinecone_api_key)

# Initializing OpenAI embeddings model with API key
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Name for the index
index_name = "info_7375"

# Embed the documents
def vector_db():
  #Load the directory
  loader = DirectoryLoader('/Users/anshaya/Downloads/QA_System/Test_Case')
  pages = loader.load_and_split()
  # Split documents into chunks and create indexes
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
  split_data = text_splitter.split_documents(pages)
  indexes = PineconeVectorStore.from_documents(split_data, embeddings_model, index_name=index_name)

  return indexes


def get_retrieval_chain(result):
    # Define system prompt for chat interaction
    system_prompt = (
        """ 
        You are a helpful assistant who helps users answer their {question}.
        Answer the question in your own words only from the context given to you.
        If questions are asked where there is no relevant context available, please ask the user to upload relevant document.
        
        
        Context: {context}
        """
    )
    system_prompt.format(context = "result", question = "query")
    
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{question}")]
    )
    
    
    # Assigning the OPENAI model and Retrieval chain
    model_name = "gpt-4"
    llm = ChatOpenAI(model_name=model_name)

    # Define the Retrieval chain
    retrieval_chain = RetrievalQA.from_chain_type(
        llm, retriever=result.as_retriever(), chain_type_kwargs={"prompt": prompt}
    )
    st.session_state.chat_active = True

    return retrieval_chain


# Define Response Function
def get_answer(query):
    # Get retrieval chain
    retrieval_chain = get_retrieval_chain(st.session_state.vector_store)
    # Get answer from retrieval chain
    answer = retrieval_chain({"query": query})
    return answer


# Title for the web app
st.title("🦜🔗 QueryDoc for INFO 7375")

if "vector_store" not in st.session_state:
  # Initialize vector store
  st.session_state.vector_store = vector_db()

if "messages" not in st.session_state:
  st.session_state.messages = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
    
# React to user input
if query := st.chat_input("Ask your question here"):
    # Display user message in chat message container
    with st.chat_message("user"):
      st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Get answer from retrieval chain
    answer = get_answer(query)
    result = answer["result"]
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(result)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})
    
    # Button to clear chat messages
    def clear_messages():
        st.session_state.messages = []
    st.button("Clear", help = "Click to clear the chat", on_click=clear_messages)


# # Function to reset the session
# def reset_session():
#     index = pc.Index(index_name)
#     index.delete(delete_all = True)


# # Add a button at the bottom right corner
# if st.button("Reset your Documents", help="Click to reset the documents", on_click=reset_session):
#     pass
