import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from pydantic import BaseModel, Field
import operator

# Load environment variables from .env file
load_dotenv()

# Step1 : Declare Model
model_openapi= ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step :
class ChatState(TypedDict):
    chat_messages: Annotated[list[BaseMessage],add_messages]

# Step : chat_node function
def chat_node(state: ChatState):
    chat_message = state['chat_messages']
    response =model_openapi.invoke(chat_message)
    return ({'chat_messages': [response]})

# Step : State
chatgraph = StateGraph(ChatState)

# Step Add Node
chatgraph.add_node('chat_node', chat_node)


# step add Edge
chatgraph.add_edge(START, 'chat_node')
chatgraph.add_edge('chat_node',END)

# Step Compile thechatgraph
chat_workflow =chatgraph.compile()

# # Step 12: Define initial state
# initial_state: ChatState = {
#     'chat_messages' : [HumanMessage(content= 'What is capital of Canada')],
# }

# # Step 13: Execute the workflow with an initial state
# final_state = chat_workflow.invoke(initial_state)
# print(final_state['chat_messages'])

while True:
    user_message = input('User: ')
    # print('User:', user_message)
    if user_message.strip().lower() in ['exit','quit','bye']:
        print('AI: It was lovely talking to you, have a good day!')
        break
    response = chat_workflow.invoke({'chat_messages' : [HumanMessage(content= user_message)]})
    print('AI:', response['chat_messages'][-1].content)



# Step 14: Visualize the workflow
from IPython.display import Image
Image(chat_workflow.get_graph().draw_mermaid_png())