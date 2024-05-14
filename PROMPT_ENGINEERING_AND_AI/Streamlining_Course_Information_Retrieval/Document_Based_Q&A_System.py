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
from pinecone import Pinecone
from docx import Document
from io import StringIO
import PyPDF2  
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader
import pdfplumber
import os.path
import pathlib
import preprocessing as pre
import tempfile

# Set up the environment

# Load secret keys
secrets = st.secrets
openai_api_key = secrets["openai"]["api_key"] # Access OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key

pinecone_api_key = secrets["pinecone"]["api_key"] # Access Pinecone API key
os.environ["PINECONE_API_KEY"] = pinecone_api_key


# def doc_preprocessing():
    
    # def extract_text_from_docx(uploaded_file):
    #     doc = docx.Document(uploaded_file)
    #     full_text = []
    #     for para in doc.paragraphs:
    #         full_text.append(para.text)
    #     return '\n'.join(full_text)

    # # Function to extract text from PDF file
    # def extract_text_from_pdf(uploaded_file):
    #     pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    #     full_text = []
    #     for page_num in range(pdf_reader.numPages):
    #         page = pdf_reader.getPage(page_num)
    #         full_text.append(page.extractText())
    #     return '\n'.join(full_text)

    # try:
    #     file_type = uploaded_file.type
    #     if  file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # DOCX
    #         # file_contents = extract_text_from_docx(uploaded_file)
    #         loader = Docx2txtLoader(uploaded_file)
    #         docs = loader.load()
            
    #     elif file_type == 'application/pdf':  # PDF
    #         # file_contents = extract_text_from_pdf(uploaded_file)
    # loader = PyPDFLoader(uploaded_file)
    # docs = loader.load()
            
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
    #                                              chunk_overlap=50)
    # split_data = text_splitter.split_documents(docs)

    # except Exception as e:
    #     st.error(f"An error occurred: {e}")

    
    # return split_data



# Embed the documents
def vector_db():

    for file in uploaded_file:
        file.seek(0)

    if uploaded_file is not None:
        for file in uploaded_file:
            # display the name and the type of the file
            file_details = {"filename":file.name,
                            "filetype":file.type
            }
            st.write(file_details)    


    
    if uploaded_file:
        
        data = file.getvalue()
        parent_path = pathlib.Path(__file__).parent.parent.resolve()           
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, file.name)
            
        loader = PyPDFLoader(complete_name)
        docs = loader.load()
        st.write("file contents: ", file)
    
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                               chunk_overlap=50)
        split_data = text_splitter.split_documents(docs)
          
       
        # temp_dir = tempfile.mkdtemp()
        # path = os.path.join(temp_dir, file.name)
        # with open(path, "wb") as f:
        #     f.write(file.getvalue())
    
    else:
        # Handle the case where uploaded_file is not a file object
        st.write("Please upload a file.")
    
    

    pc = Pinecone(pinecone_api_key=pinecone_api_key)
    embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    # Create a new Pinecone Index and setup the vector database and search engine
        
    index_name = "langchain-demo"
    global index
    
        # try:
        # loader = PyPDF2.PdfReader(uploaded_file)
        
        # loader = PyPDFLoader(uploaded_file)
       
    indexes = PineconeVectorStore.from_documents(split_data, embeddings_model, index_name=index_name)
            
        # except Exception:
        #     # If index retrieval fails or total vector count is 0, create vector
        #     # st.error(f"An error occurred: {e}")   
        #     # Try to retrieve vectors from existing index
        #     index = pc.Index(index_name)
        #     describe_stats = index.describe_index_stats()
        #     total_vector_count = describe_stats['total_vector_count']
        #     print(total_vector_count)
        #     if total_vector_count == 0:
        #         raise Exception("Total Vector Count is 0")
        #     # If vectors exists, load it
        #     indexes = PineconeVectorStore.from_existing_index(index_name, embeddings_model)
    
    return indexes

# Define chain

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

# Define a function to find similar documents based on a given query

# def get_similar_docs(query, k=1, score=False):
#     if score:
#         similar_docs = indexes.similarity_search_with_score(query, k=k)
#     else:
#         similar_docs = indexes.similarity_search(query, k=k)
#     return similar_docs

# Define Response Function

def get_answer(query):
    
    retrieval_chain = get_retrieval_chain(st.session_state.vector_store)
    answer = retrieval_chain({"query":query})
    return answer

    
# def upload():
#     if uploaded_file is None:
#         st.session_state["upload_state"] = "Upload a file first!"
#     else:
#         if isinstance(uploaded_file, list):
#             # If uploaded_file is a list, take the first element
#             uploaded_file = uploaded_file[0]
                
#         # Read the content of the uploaded file
#         file_content = uploaded_file.read()
#         # Create a file-like object from the content
#         file_buffer = BytesIO(file_content)
#         bytes_data = file_buffer.getvalue()
#         data = file_buffer.getvalue().decode('utf-8').splitlines()         
#         st.session_state["preview"] = ''
#         for i in range(0, min(5, len(data))):
#             st.session_state["preview"] += data[i]
#         preview = st.text_area("File Preview", "", height=150, key="preview")
#         upload_state = st.text_area("Upload State", "", key="upload_state")
            
#         data = uploaded_file.getvalue().decode('utf-8')
#         parent_path = pathlib.Path(__file__).parent.parent.resolve()           
#         save_path = os.path.join(parent_path, "data")
#         complete_name = os.path.join(save_path, file_buffer.name)
#         destination_file = open(complete_name, "w")
#         destination_file.write(data)
#         destination_file.close()
#         st.session_state["upload_state"] = "Saved " + complete_name + " successfully!"
            
# def process():

    # # loader = PyPDFLoader(complete_name)
    # # docs = loader.load()
    # if uploaded_file is None:
    #     # st.session_state["upload_state"] = "Upload a file first!"
    #     # uploaded_file = st.file_uploader("Upload your document", type=["pdf"], accept_multiple_files = True)
    #     st.write("Upload a file first!")

    # # else:
    # if isinstance(uploaded_file, list):
    #     # If uploaded_file is a list, take the first element
    #     uploaded_file = uploaded_file[0]
                
    # # Read the content of the uploaded file
    # file_content = uploaded_file.read()
    # st.write("file_content", file_content)
    # # Create a file-like object from the content
    # file_buffer = BytesIO(file_content)
    # bytes_data = file_buffer.getvalue()
    # data = file_buffer.getvalue().decode('utf-8').splitlines()         
    # st.session_state["preview"] = ''
    # for i in range(0, min(5, len(data))):
    #     st.session_state["preview"] += data[i]
    #     preview = st.text_area("File Preview", "", height=150, key="preview")
    # upload_state = st.text_area("Upload State", "", key="upload_state")
        
    # data = file_buffer.getvalue().decode('utf-8')
    # parent_path = pathlib.Path(__file__).parent.parent.resolve()           
    # save_path = os.path.join(parent_path, "data")
    # complete_name = os.path.join(save_path, file_buffer.name)
    # destination_file = open(complete_name, "w")
    # destination_file.write(data)
    # destination_file.close()
    # st.session_state["upload_state"] = "Saved " + complete_name + " successfully!"


    
def process():

    if "vector_store" not in st.session_state:
        # Initialize vector store
        st.session_state.vector_store = vector_db()

def chat():

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


st.title("🦜🔗Learning Assistance")

# File uploader for user to upload a document
uploaded_file = st.file_uploader("Upload your document", type=["pdf"], accept_multiple_files = True)

st.button("Process the uploaded file", on_click=process)

# st.button("Retrieve", on_click = process)

st.button("Chat", on_click = chat)

# try:
#     if uploaded_file is not None:
#         # st.success("Uploaded the file")


# except Exception as e:
#         st.error(f"An error occurred: {e}")


# # React to user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})




















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

