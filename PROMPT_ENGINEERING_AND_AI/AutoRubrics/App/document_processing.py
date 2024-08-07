import chardet
import tempfile
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def example_file(uploaded_files):
    detector = chardet.UniversalDetector()
    for uploaded_file in uploaded_files:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
        # Save file to a temporary directory
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())
        with open(path, "rb") as f:
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        encoding = detector.result['encoding']
        raw_documents = TextLoader(path, encoding=encoding).load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, OpenAIEmbeddings())
    return db
