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
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader, UnstructuredPowerPointLoader
import os.path
import pathlib
import tempfile


## Set up the environment
# Load secret keys

secrets = st.secrets

openai_api_key = secrets["openai"]["api_key"] # Access OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key

pinecone_api_key = secrets["pinecone"]["api_key"] # Access Pinecone API key
os.environ["PINECONE_API_KEY"] = pinecone_api_key



pc = Pinecone(pinecone_api_key=pinecone_api_key)
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
index_name = "langchain-demo"

# Embed the documents

def vector_db():
    
    for file in uploaded_files:
        file.seek(0)
        
        # display the name and the type of the file
        file_details = {"filename":file.name,
                        "filetype":file.type
        }
        st.write(file_details)    

    
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, file.name)
        with open(path, "wb") as f:
            f.write(file.getvalue())
        # Get the file extension from the filename
        file_extension = file.name.split(".")[-1].lower()
        
        if file_extension == "pdf":
                loader = PyPDFLoader(path)
            
        elif file_extension == "docx":
                loader = Docx2txtLoader(path)

        docs = loader.load()
        for doc in docs:
            text = doc.page_content
            st.write("file contents:", text) 
    
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                       chunk_overlap=50)
        split_data = text_splitter.split_documents(docs)      
        indexes = PineconeVectorStore.from_documents(split_data, embeddings_model, index_name=index_name)

    
    return indexes

    
    

def get_retrieval_chain(result):
    
    # Creating the Prompt
    system_prompt = (
    """ 
    You are a helpful assistant who helps users answer their question based on the documents they upload.
    Answer the question in your own words from the context given to you.
    If questions are asked where there is no relevant context available, please answer from what you know and say please upload your documents first for better response.

    
    Context: {context}
    """
        
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )
            
    prompt.format(context = "text", question = "query")
    
    # Assigning the OPENAI model and Retrieval chain
    model_name = "gpt-4"
    llm = ChatOpenAI(model_name=model_name)

    # Define the Retrieval chain
    retrieval_chain = RetrievalQA.from_chain_type(llm, retriever=result.as_retriever(), chain_type_kwargs={'prompt': prompt})
    st.session_state.chat_active = True
    
    return retrieval_chain


# Define Response Function

def get_answer(query):
    
    retrieval_chain = get_retrieval_chain(st.session_state.vector_store)
    answer = retrieval_chain({"query":query})
    return answer


st.title("🦜🔗Learning Assistance")
# File uploader for user to upload a document
uploaded_files = st.file_uploader("Upload your document", type=["pdf","docx"], accept_multiple_files = True)
if st.button("Process your File"):
    if uploaded_files is None:
        st.write("Please upload a file first.")
        
    elif uploaded_files is not None:
        if "vector_store" not in st.session_state:
            # Initialize vector store
            st.session_state.vector_store = vector_db()


# Initialize chat history
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
                    
    answer = get_answer(query)
    result = answer['result']
                        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(result)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})
                
    def clear_messages():
        st.session_state.messages = []
        
    st.button('Clear',on_click=clear_messages)


if st.button("Reset"):
    st.rerun()












# def upload_file_section():
#     st.title("🦜🔗Learning Assistance")
#     # File uploader for user to upload a document
#     uploaded_file = st.file_uploader("Upload your document", type=["pdf","docx"], accept_multiple_files = True)
#     return uploaded_file 


# def process_file_section(uploaded_file):
#     if uploaded_file is None:
#         st.warning("Please upload a file first.")
#         return
        
#     elif uploaded_file is not None:
#         if "vector_store" not in st.session_state:
#             # Initialize vector store
#             st.session_state.vector_store = vector_db(uploaded_file)
        
# def chat_section():
#     st.title("Chat with Me 🦜")

#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
                
#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
                        
#                 # React to user input
#     if query := st.chat_input("Ask your question here"):
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(query)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": query})
                    
#         answer = get_answer(query)
#         result = answer['result']
                        
#         # Display assistant response in chat message container
#         with st.chat_message("assistant"):
#             st.markdown(result)
#             # Add assistant response to chat history
#             st.session_state.messages.append({"role": "assistant", "content": result})
                
#         def clear_messages():
#             st.session_state.messages = []
        
#         st.button('Clear',on_click=clear_messages)




# def main():
#     st.sidebar.title("Navigation")

    
        
#     app_mode = st.sidebar.radio("Choose a mode", ["Upload File", "Chat"])

#     if "uploaded_file" not in st.session_state:
#         st.session_state.uploaded_file = None
            
#     if app_mode == "Upload File":
#         uploaded_file = upload_file_section()
#         if uploaded_file is not None:
#             st.session_state.uploaded_file = uploaded_file
            
#         if st.button("Process File"):
#             process_file_section(uploaded_file)
        
#     # elif app_mode =="Process File":
#     #     process_file_section(uploaded_file)
#     if app_mode == "Chat":
#          if st.session_state.uploaded_file is None:
#             st.warning("Please upload a file first.")
#          else:
#              chat_section()

# if __name__ == "__main__":
#     main()












# template = """
# Answer the question in your own words from the context given to you.
# If questions are asked where there is no relevant context available, please answer from what you know.

# Context: {context}

# Human: {question}
# Assistant:

# """

# prompt = PromptTemplate(
#     input_variables=["context", "question"], template=template
# )

# # Assigning the OPENAI model and Retrieval chain

# model_name = "gpt-4"
# llm = ChatOpenAI(model_name=model_name)

# chain = RetrievalQA.from_chain_type(llm, retriever=index.as_retriever(),chain_type_kwargs={'prompt': prompt}
#     )

# # Define Response Function

# def get_answer(query):
#     similar_docs = get_similiar_docs(query)
#     answer = chain({"query":query})
#     return answer

# # Streamlit Application

# st.title("Streamlit Langchain Application")

# question_input = st.text_input("Ask your question here:")

# if st.button("Get Answer"):
#     answer = get_answer(question_input)
#     st.write("Answer:", answer)


# File upload
# uploaded_file = st.file_uploader("Upload your file")

# if uploaded_file is not None:
#     # Process the uploaded file
#     file_contents = uploaded_file.read()
#     st.write("File contents:", file_contents)

#     # Try decoding with different encodings until successful
#     encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1']  # Add more encodings if needed
#     decoded_content = None
#     for encoding in encodings_to_try:
#         try:
#             decoded_content = file_contents.decode(encoding)
#             break  # Break out of loop if decoding is successful
#         except UnicodeDecodeError:
#             continue  # Try next encoding if decoding fails
    
#     if decoded_content is None:
#         st.write("Unable to decode file contents with any of the specified encodings.")
#     else:
#         # Call the function or method to split decoded_content into pages
#         pages = decoded_content.load_and_split()
    
#     #Split the documents into smaller chunks for processing
#     chunk_size=1000 
#     chunk_overlap=200
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     split_docs = text_splitter.split_documents(pages)

