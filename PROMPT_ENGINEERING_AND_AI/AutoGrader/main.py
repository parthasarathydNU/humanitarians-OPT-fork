import streamlit as st
from App.vectordb import vector_db
from App.chain import get_chain,get_scores
from App.chat_history import format_chat_history
from App.document_handler import  extract_answers
import re


#Save all the variables in streamlit sessions
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "rubrics" not in st.session_state:
    st.session_state.rubrics = None
    
if "chain" not in st.session_state:
    st.session_state.chain = None

if "extracted_answers" not in st.session_state:
    st.session_state.extracted_answers = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None



# Streamlit app interface
st.title("Automatic Grading System")

# Multi-page navigation
page = st.sidebar.selectbox("Choose a page", ["Home", "Upload Assignment"])

if page == "Home":
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
                                
    if query := st.chat_input("Ask your question here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(query)
        # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})

        st.session_state.chat_history = format_chat_history(st.session_state.messages)
    
        answer = get_scores(query)

        #Extract user name from chat
        # pattern = r'\s*"?(\w+)"?'
        pattern = r'(?:user_name\s*=\s*)"?(\w+)"?'
        
        search_results = re.search(pattern, answer, re.DOTALL)
        
        if search_results:
            st.session_state.user_name = search_results.group(1)

            st.write("result: ", st.session_state.user_name)

            if st.session_state.user_name:
                #Fetch predefined rubrics using user name
                st.session_state.rubrics = vector_db()

        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history                
        st.session_state.messages.append({"role": "assistant", "content": answer})

            
                                        
        # Button to clear chat messages
        def clear_messages():
            st.session_state.messages = []
            st.button("Clear", help = "Click to clear the chat", on_click=clear_messages)


if page == "Upload Assignment":

    
    # File uploader
    uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])
    
    
    # Document Handler:
    if uploaded_file:
    
        # Extract answers using regex patterns
        st.session_state.extracted_answers = extract_answers(uploaded_file)
    
        st.write("Assignment Uploaded Successfully")
    
        
       


