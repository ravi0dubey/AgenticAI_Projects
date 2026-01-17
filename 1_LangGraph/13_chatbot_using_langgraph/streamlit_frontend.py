import streamlit as st
from langgraph_backend import chat_workflow
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
for message in  st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    
user_input =  st.chat_input("Type Here" )

if user_input:
    # first add user message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Step : Add AI message message to message_history
    response = chat_workflow.invoke({'chat_messages' : [HumanMessage(content= user_input)]}, config= CONFIG)
    ai_message = response['chat_messages'][-1].content

    st.session_state['message_history'].append({'role': 'AI', 'content': ai_message})
    with st.chat_message('AI'):
        st.text(ai_message)  


        