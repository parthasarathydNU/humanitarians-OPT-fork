{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1b705524",
   "metadata": {},
   "outputs": [],
   "source": [
    "%pip install --upgrade --quiet  \"unstructured[all-docs]\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "25f32310",
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install --upgrade langchain openai -q"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ee37f11f",
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install pinecone-client -q"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c19626a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install -qU langchain-openai"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6fa4846e",
   "metadata": {},
   "outputs": [],
   "source": [
    "%pip install --upgrade --quiet  langchain-pinecone langchain-openai langchain"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "541d51a3-eaf1-4ed9-9853-67212fd94758",
   "metadata": {},
   "outputs": [],
   "source": [
    "!brew install poppler"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bde4085d-a841-46bd-8d54-68fb6efffb4e",
   "metadata": {},
   "outputs": [],
   "source": [
    "!brew install tesseract"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "85bafd22-e3cd-43db-885d-adfffeef32f6",
   "metadata": {},
   "outputs": [],
   "source": [
    "%pip install -qU langchain-text-splitters"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0047a291",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Import necessary libraries and modules\n",
    "\n",
    "import os\n",
    "import streamlit as st\n",
    "import openai\n",
    "import pinecone\n",
    "from langchain_community.document_loaders import DirectoryLoader\n",
    "from langchain.text_splitter import Language, RecursiveCharacterTextSplitter\n",
    "from langchain.embeddings.openai import OpenAIEmbeddings\n",
    "from langchain.vectorstores import Pinecone\n",
    "from langchain.llms import OpenAI\n",
    "from langchain.chains.question_answering import load_qa_chain\n",
    "from langchain_openai import ChatOpenAI\n",
    "from pinecone import Pinecone, PodSpec\n",
    "from langchain_pinecone import PineconeVectorStore\n",
    "from langchain_community.chat_models import ChatOpenAI\n",
    "from langchain_core.documents import Document\n",
    "from langchain_core.prompts import ChatPromptTemplate\n",
    "from langchain.chains.combine_documents import create_stuff_documents_chain\n",
    "from langchain.chains import ConversationalRetrievalChain,RetrievalQA\n",
    "from langchain.prompts import PromptTemplate"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a0204dc5",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Set up the environment\n",
    "\n",
    "st.write(\n",
    "    \"Has environment variables been set:\",\n",
    "    os.environ[\"DB_USERNAME_1\"] == st.secrets[\"DB_TOKEN_1\"],\n",
    "    os.environ[\"DB_USERNAME_2\"] == st.secrets[\"DB_TOKEN_2\"],\n",
    ")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9e0e39c5",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Load the directory\n",
    "\n",
    "loader = DirectoryLoader('/Users/anshaya/Downloads/Test_Case')\n",
    "\n",
    "pages = loader.load_and_split()\n",
    "# len(pages)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b6c3bfdb",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Split the documents into smaller chuncks for processing\n",
    "\n",
    "def split_docs(pages, chunk_size=1000, chunk_overlap=200):\n",
    "  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)\n",
    "  docs = text_splitter.split_documents(pages)\n",
    "  return docs\n",
    "\n",
    "docs = split_docs(pages)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "52a8c892",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Verify the contents\n",
    "\n",
    "print(docs[0].page_content)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e3a708ca",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Embed the documents\n",
    "\n",
    "embeddings_model = OpenAIEmbeddings(model=\"text-embedding-3-large\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "68176b50",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Create a new Pinecone Index and setup the vector database and search engine\n",
    "\n",
    "index_name = \"langchain-demo\"\n",
    "\n",
    "index = PineconeVectorStore.from_documents(docs, embeddings_model, index_name=index_name)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9e87e8e8",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Define a function to find similar documents based on a given query\n",
    "\n",
    "def get_similiar_docs(query, k=1, score=False):\n",
    "  if score:\n",
    "    similar_docs = index.similarity_search_with_score(query, k=k)\n",
    "  else:\n",
    "    similar_docs = index.similarity_search(query, k=k)\n",
    "  return similar_docs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1791e55e-96a8-4414-a830-e4edd135124e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Creating the Prompt\n",
    "\n",
    "template = \"\"\"Answer the question in your own words from the context given to you.\n",
    "If questions are asked where there is no relevant context available, please answer from what you know.\n",
    "\n",
    "Context: {context}\n",
    "\n",
    "Human: {question}\n",
    "Assistant:\n",
    "\n",
    "\"\"\"\n",
    "\n",
    "prompt = PromptTemplate(\n",
    "input_variables=[\"context\", \"question\"], template=template\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "70a8c4f5-b0a4-4e93-a9a0-fea3754dd47b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Assigning the OPENAI model and Retrieval chain\n",
    "\n",
    "model_name = \"gpt-4\"\n",
    "llm = ChatOpenAI(model_name=model_name)\n",
    "\n",
    "chain = RetrievalQA.from_chain_type(llm, retriever=index.as_retriever(),chain_type_kwargs={'prompt': prompt}\n",
    "    )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e9046392-ce34-4e99-b440-8f2726a2474e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Define Response Function\n",
    "\n",
    "def get_answer(query):\n",
    "  similar_docs = get_similiar_docs(query)\n",
    "  answer = chain({\"query\":query})\n",
    "  return answer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ad853a54",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Testing\n",
    "\n",
    "question1 = \"When is the course start date?\"\n",
    "answer = chain({\"query\": question1})\n",
    "print(answer)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6437e9f6",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Conversation Flow\n",
    "\n",
    "import re\n",
    "\n",
    "conversation = []\n",
    "\n",
    "while True:\n",
    "    \n",
    "    query = input(\"Human: \" )\n",
    "    conversation.append('Human: ' + query)\n",
    "\n",
    "    output = get_answer(query)\n",
    "    conversation.append('Assistant: ' + str(output))\n",
    "\n",
    "    result = output.get('result','')\n",
    "\n",
    "    conversation.append('Assistant: ', + result)\n",
    "    \n",
    "    print(result)\n",
    "    \n",
    "    if query == \"bye\":\n",
    "        print(\"bye\")\n",
    "        break "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "068b444f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3e164a3b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
