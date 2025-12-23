from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI     
from typing import TypedDict
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown

# Load environment variables from .env file
load_dotenv()

# model initialization
model_openapi= ChatOpenAI(temperature=0, api_key=os.getenv("OPEN_API_KEY") )


# Step 1: Define State
class LLMState(TypedDict):           
    question: str
    answer: str       

# Step 2: Define llm_response function
def llm_response(state: LLMState) -> LLMState:      
    prompt = state['question']
    response = model_openapi.invoke(prompt).content
    state['answer'] = response
    return state  
 

# Step 3: Define Graph
llm_graph = StateGraph(LLMState)   

# Step 4: Add Nodes to the graph
llm_graph.add_node('llm_response', llm_response)        

# Step 5: Add Edges to your graph
llm_graph.add_edge(START, 'llm_response')   
llm_graph.add_edge('llm_response', END)        

# Step 6: Compile the Graph 
workflow= llm_graph.compile()

# Step 7: Execute the Graph with initial data
initial_data = {
    "question": "Explain the theory of relativity in simple terms.",
    "answer": ""
}
llm_result = workflow.invoke(initial_data)
print(f"**Question:** {llm_result['question']}")
print(f"**Answer:** {llm_result['answer']}")