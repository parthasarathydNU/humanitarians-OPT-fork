
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os.path
import pathlib
import re
import pdfplumber
import docx
import streamlit as st


# Function to extract answers using regex patterns
def extract_answers(uploaded_file):

    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
    
    # Save file to a temporary directory
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
        
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Determine file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension == "txt":
        text = uploaded_file.read().decode('utf-8')
    elif file_extension == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            text = "\n".join(pages)
    elif file_extension == "docx":
        pages = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in pages.paragraphs])

    extracted_answers = []

    # Pattern
    pattern = r"(Question\s*\d:.*?)(Answer\s*\d:.*)"
    
    # Use re.search to iterate through the matches
    search_result = re.search(pattern, text, re.DOTALL)
    
    
    if search_result:
        # Extract the question and answer from the matched groups
        question = search_result.group(1).strip()

        extracted_answers.append(question)
        
        answer = search_result.group(2).strip()
        answers_cleaned = re.sub(r'(^#)', r'\\#', answer, flags=re.MULTILINE)
        
        extracted_answers.append(answers_cleaned)
        
    else:

        st.write("Assignment:" , text)
        
        return text
        
        
            
    return extracted_answers
