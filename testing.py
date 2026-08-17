# import uuid

# def create_thread_id():
#     thread_id = uuid.uuid4()
#     return str(thread_id)



# print(create_thread_id())
# print(type(create_thread_id()))




# ************************************************** Get state of graph **************************************************

from langchain_core.messages import HumanMessage
from Projects.chatbot.backend_langgraph import chatbot




CONFIG = {'configurable': {'thread_id': '1'}}

response = chatbot.invoke(
    {'messages': [HumanMessage(content="can you list our conversation history?")]},
    config=CONFIG,
)
print(response["messages"][-1].text)
# print(response)

print(end='\n\n\n')

# print(chatbot.get_state(config = CONFIG).values['messages'])