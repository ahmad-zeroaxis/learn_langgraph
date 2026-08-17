from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage
import sqlite3

load_dotenv()


# state schemas
class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# generative model
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")



# graph node
def chat_node(state: MessageState):

    # take user query from state
    messages = state['messages']

    # send query to llm
    response = llm.invoke(messages)

    # store response to state
    return {"messages": [response]}


# checkpointer
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)     # support multiple threats
checkpointer = SqliteSaver(conn=conn)        # where to store state of graph


graph = StateGraph(MessageState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)








# retrive all checkpointers fron db 
def retrive_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)