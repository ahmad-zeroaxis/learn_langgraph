import streamlit as st
from backend_langgraph import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': '1'}}


st.title("AI Assistant")

# session_state -> dict
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# loading conversation history
if st.session_state['message_history']:
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            st.write(message['content'])


user_input = st.chat_input("Ask anything")


if user_input:
    # user 
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)


    # assistant
    response = chatbot.invoke({"messages": HumanMessage(content=user_input)}, config=CONFIG)
    assistent_output = response["messages"][-1].text

    st.session_state['message_history'].append({'role': 'assistant', 'content': assistent_output})
    with st.chat_message('assistant'):
        st.write(assistent_output)