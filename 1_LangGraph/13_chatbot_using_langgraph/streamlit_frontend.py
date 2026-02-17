import streamlit as st
from langgraph_backend import chat_workflow
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Loading the conversation history  
for message in  st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    
user_input =  st.chat_input("Type Here" )

if user_input:
    # first add user message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    # Display user message on the screen
    with st.chat_message('user'):
        st.text(user_input)

    #  Get response of the user message by invoking llm from the backend
    response = chat_workflow.invoke({'chat_messages' : [HumanMessage(content= user_input)]}, config= CONFIG)
    ai_message = response['chat_messages'][-1].content

    # Add AI message response to message_history
    st.session_state['message_history'].append({'role': 'AI', 'content': ai_message})
    
    # Display AI response message on the screen
    with st.chat_message('AI'):
        st.text(ai_message)  


        