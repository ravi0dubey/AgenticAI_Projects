import streamlit as st

message_history = []
# with st.chat_message('user'):
#     st.text('Hello')

# with st.chat_message('AI'):
#     st.text('How can i help you today')   
    
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])
    
user_input =  st.chat_input("Type Here" , key="chat_input")

if user_input:
    # first add user message to message_history
    message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    # Step : Add AI message message to message_history
    message_history.append({'role': 'AI', 'content': user_input})
    with st.chat_message('AI'):
        st.text(user_input)  
    print(message_history)
        