from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage

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




checkpointer = InMemorySaver()        # where to store state of graph (currently in RAM)
graph = StateGraph(MessageState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)