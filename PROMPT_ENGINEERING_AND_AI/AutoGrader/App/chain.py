from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, create_retrieval_chain
from langchain.prompts.chat import ChatPromptTemplate
import streamlit as st


def get_chain(assignment,predefined_rubrics,chat_history):
        
        system_prompt = """
        
        You are an expert grader, your name is AutoGrader. Your job is to grade {assignment} based on {predefined_rubrics}.

        Start by greeting the user respectfully, collect the name of the user. Save the name of the user in a variable called user_name.
        Display the name to the user exactly in the following format and ask if you can use this user name to fetch their predefined rubrics.
        
        user_name = 
        
        Only after verifying the user_name, move to the next step.

        Next step is to verify {predefined_rubrics} with the user by displaying whole exact {predefined_rubrics} to them clearly.
        Only after successfully verifying predefined_rubrics, move to the next step.
        
        Next step is to ask the user to upload the assignment through navigating to uploag page from left hand side. 
        
        Go through the {assignment} and highlight the mistakes that user made, make sure you explain all the mistakes in detail with soultions.
        Be consistent with the scores and feedbacks generated.
        
        Lastly, ask user if they want any modification or adjustments to the scores generated, if user says no then end the conversation.

        Keep the chat history to have memory and do not repeat questions.
        
        chat history: {chat_history}
        
        """

        prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", "{input}")]
        )

        prompt.format_messages(input = "query", assignment = "st.session_state.extracted_answers", predefined_rubrics = "st.session_state.rubrics", chat_history = "st.session_state.chat_history")

        model_name = "gpt-4o"
        llm = ChatOpenAI(model_name=model_name)
        

        st.session_state.chain = LLMChain(llm = llm,prompt = prompt)

        st.session_state.chat_active = True


        return st.session_state.chain

def get_scores(query):
        
        chains = get_chain(st.session_state.extracted_answers,st.session_state.rubrics,st.session_state.chat_history)
        response = chains.invoke({"input": query, "assignment": st.session_state.extracted_answers, "predefined_rubrics": st.session_state.rubrics,"chat_history": st.session_state.chat_history})
        
        try:
                answer = response['text']
                
        except:
                ans = response['answer']
                answer = ans['text']
              
        
        return answer
