import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
import operator

# Load environment variables from .env file
load_dotenv()

# Step1: Declare Model
model_openapi= ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step2: Define workflow state
class ChatState(TypedDict):
    chat_messages: Annotated[list[BaseMessage],add_messages]

# Step3: Create chat_node function
def chat_node(state: ChatState):
    chat_message = state['chat_messages']
    response =model_openapi.invoke(chat_message)
    return ({'chat_messages': [response]})

# Step4: Create StateGraph and add nodes and edges
chatgraph = StateGraph(ChatState)

# Step5: Create a MemorySaver
chat_checkpointer = MemorySaver()

# Step6: Add Node
chatgraph.add_node('chat_node', chat_node)


# Step7: Add Edge
chatgraph.add_edge(START, 'chat_node')
chatgraph.add_edge('chat_node',END)

# Step8: Compile the chatgraph
chat_workflow =chatgraph.compile(checkpointer=chat_checkpointer)