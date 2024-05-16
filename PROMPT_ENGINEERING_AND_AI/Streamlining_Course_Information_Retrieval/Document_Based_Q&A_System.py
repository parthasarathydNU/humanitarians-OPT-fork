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
import preprocessing as pre
import tempfile




## Set up the environment
# Load secret keys

secrets = st.secrets

openai_api_key = secrets["openai"]["api_key"] # Access OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key

pinecone_api_key = secrets["pinecone"]["api_key"] # Access Pinecone API key
os.environ["PINECONE_API_KEY"] = pinecone_api_key



# Embed the documents

def vector_db():

    for file in uploaded_file:
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

    # Check the file extension and process accordingly
    if file_extension == "pdf":
        loader = PyPDFLoader(path)
    elif file_extension == "docx":
        loader = Docx2txtLoader(path)
    elif file_extension == "pptx":
        loader = UnstructuredPowerPointLoader(path)
    else: 
        st.error("Unsupported file format. Please upload a PDF, DOCX, or PPTX file.")
    
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                               chunk_overlap=50)
    split_data = text_splitter.split_documents(docs)

    pc = Pinecone(pinecone_api_key=pinecone_api_key)
    embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

    index_name = "langchain-demo"
    global index

    indexes = PineconeVectorStore.from_documents(split_data, embeddings_model, index_name=index_name)      

    return indexes

    
    

def get_retrieval_chain(result):
    
    # Creating the Prompt
    system_prompt = (
    """ 
    You are a helpful assistant who helps users answer their question.
    Answer the question in your own words from the context given to you.
    If questions are asked where there is no relevant context available, please answer from what you know.
    
    Context: {context}
    """
        
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )
            
    prompt.format(context = "split_data", question = "query")
    
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


def process():
    if uploaded_file:
        if "vector_store" not in st.session_state:
            # Initialize vector store
            st.session_state.vector_store = vector_db()                        
    else:
         st.error("Please upload a file first")



st.title("🦜🔗Learning Assistance")

def upload_file_section():
    st.title("Upload Your File")
    # File uploader for user to upload a document
    uploaded_file = st.file_uploader("Upload your document", type=["pdf","docx","pptx"], accept_multiple_files = True)
    st.button('process your file', on_click = process):

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode", ["Upload File", "Chat"])

    if app_mode == "Upload File":
        upload_file_section()
    elif app_mode == "Chat":
        chat_section()

if __name__ == "__main__":
    main()

def chat_section():
    st.title("Chat with Me 🦜")
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

