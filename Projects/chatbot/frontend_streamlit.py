import streamlit as st
from backend_langgraph import chatbot, retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid



# ********************************************* Utility/Helper functions *********************************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)



def reset_chat():
    new_thread_id = generate_thread_id()                # generate new thread id
    st.session_state['thread_id'] = new_thread_id       # store in session
    add_thread(st.session_state['thread_id'])           # append in session list whenever New Chat button clicked
    st.session_state['message_history'] = []



def load_conversation(thread_id):                       # get history from langgraph of specific thread_id
    return chatbot.get_state(config = {'configurable': {'thread_id': thread_id}}).values['messages']



# ********************************************* Session Setup *********************************************

# session_state -> dict ,  it does not trunckat when we hit enter in chat message
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'chat_threads' not in st.session_state:      # list of threads
    st.session_state['chat_threads'] = retrive_all_threads()


add_thread(st.session_state['thread_id'])   # 1st time


CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}




# ********************************************* Sidebar *********************************************
st.sidebar.title('AI Assistant')

if st.sidebar.button('New Chat'):
    reset_chat()


st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:        # load all thread ids in reverse order(so that recent chat appear on top)
    if st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)


# convert into the following formate so that it can print on frontend smoothly
# [
#     {'role': 'user', 'content': 'hi'},
#     {'role': 'user', 'content': 'hi, how can i assist you today?'}
# ]
        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.text})


        st.session_state['message_history'] = temp_messages




# ********************************************* Main UI *********************************************

# load current conversation history
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

    with st.chat_message('assistant'):

        assistent_output = st.write_stream(
            message_chunk.text for message_chunk, metadate in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'

            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': assistent_output})