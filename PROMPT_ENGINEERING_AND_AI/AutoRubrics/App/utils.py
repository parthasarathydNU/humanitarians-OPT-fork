import streamlit as st

def select_option():
    
    options_1 = ("None", "Broad Overview", "Moderately Detailed", "Highly Detailed")
    options_2 = ("None", "Linient","Somewhat Linient","Moderate","Very Strict")
    options_3 = ("None", "Technical Accuracy","Depth of Analysis","Clarity and Creativity","Real-World Application","Problem Solving Skills")
    options_4 = ("None", "Writing Report or Essay","Coding or Programming Aissignment","Design or Creative Project","Research Paper or Thesis","Case Study Analysis")
    options_5 = ("None", "Research Oriented","Problem Solving","Case Studies","Presentations","Experiential Learning","Literature Reviews","Reflective Journals")
    
 # Maintain index based on previous selections if they exist
    option_1 = st.selectbox(
        "Detail Level of Criteria",
        options_1,
        index=options_1.index(st.session_state.selected_option[0]) if len(st.session_state.selected_option) > 0 else 0
    )
    st.session_state.selected_option[0:1] = [option_1]

    option_2 = st.selectbox(
        "Grading Strictness",
        options_2,
        index=options_2.index(st.session_state.selected_option[1]) if len(st.session_state.selected_option) > 1 else 0
    )
    st.session_state.selected_option[1:2] = [option_2]
    
    option_3 = st.selectbox(
        "Area of Emphasis in Grading",
        options_3,
        index=options_3.index(st.session_state.selected_option[2]) if len(st.session_state.selected_option) > 2 else 0
    )
    st.session_state.selected_option[2:3] = [option_3]

    option_4 = st.selectbox(
        "Assignment Type",
        options_4,
        index=options_4.index(st.session_state.selected_option[3]) if len(st.session_state.selected_option) > 3 else 0
    )
    st.session_state.selected_option[3:4] = [option_4]

    option_5 = st.selectbox(
        "Assignment Style",
        options_5,
        index=options_5.index(st.session_state.selected_option[4]) if len(st.session_state.selected_option) > 4 else 0
    )
    st.session_state.selected_option[4:5] = [option_5]

    return st.session_state.selected_option
        
