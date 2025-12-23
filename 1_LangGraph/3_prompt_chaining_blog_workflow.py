from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI     
from typing import TypedDict
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown

# Load environment variables from .env file
load_dotenv()

model_openapi= ChatOpenAI(temperature=0, api_key=os.getenv("OPEN_API_KEY") )

class BlogState(TypedDict):
    title: str
    outline: str
    content: str
    evaluation_score: str

# Step 1: Create create_outline Function
def create_outline(state: BlogState) -> BlogState:
    title = state['title']
    prompt = f'Create a detailed outline for a blog post titled: {title}'
    outline = model_openapi.invoke(prompt).content
    state['outline'] = outline
    return state

# Step 2: Create create_blog Function
def create_blog(state: BlogState) -> BlogState:
    outline = state['outline']
    prompt = f'Create a blog post based on the outline: {outline}'
    content = model_openapi.invoke(prompt).content
    state['content'] = content
    return state    

# Step 3: Create evaluate_blog Function
def evaluate_blog(state: BlogState) -> BlogState:
    outline = state['outline']
    content = state['content']
    prompt = f'Based on the outline - {outline}, evaluate the blog content - {content} and provide feedback on how to improve it.'
    evaluation = model_openapi.invoke(prompt).content
    state['evaluation_score'] = evaluation
    return state


# Step 4: Define Graph
blog_graph = StateGraph(BlogState)

# Step 5: Add Nodes to the graph
blog_graph.add_node('create_outline', create_outline)
blog_graph.add_node('create_blog', create_blog)
blog_graph.add_node('evaluate_blog', evaluate_blog)

# Step 6: Add Edges to your graph
blog_graph.add_edge(START, 'create_outline')
blog_graph.add_edge('create_outline', 'create_blog')
blog_graph.add_edge('create_blog', 'evaluate_blog')
blog_graph.add_edge('evaluate_blog', END)


# Step 7: Compile the Graph 
workflow= blog_graph.compile()

# Step 8: Execute the Graph with initial data
initial_data = {
    "title": "Married Life: Tips for a Happy Union",
    "outline": "",
    "content": "",
    "evaluation_score": ""
}
llm_result = workflow.invoke(initial_data)
print(f"**title:** {llm_result['title']}")
print(f"**outline:** {llm_result['outline']}")
print(f"**content:** {llm_result['content']}")
print(f"**evaluation_score:** {llm_result['evaluation_score']}")