
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langgraph.llms import OpenAILLM   
from Ipython import display
from langgraph.prompts import PromptTemplate


class BlogState(TypedDict):
    title: str
    outline: str
    content: str
    evaluate: str

# Create create_outline Function
def create_outline(state: BlogState) -> BlogState:
    title = state['title']
    prompt = f'Create a detailed outline for a blog post titled: {title}'
    outline = OpenAILLM.invoke(prompt).content
    state['outline'] = outline
    return state

# Create create_blog Function
def create_blog(state: BlogState) -> BlogState:
    outline = state['outline']
    prompt = f'Create a blog post based on the outline: {outline}'
    content = OpenAILLM.invoke(prompt).content
    state['content'] = content
    return state    

# Create evaluate_blog Function
def evaluate_blog(state: BlogState) -> BlogState:
    outline = state['outline']
    content = state['content']
    prompt = f'Based on the outline - {outline}, evaluate the blog content - {content} and provide feedback on how to improve it.'
    evaluation = OpenAILLM.invoke(prompt).content
    state['evaluate'] = evaluation
    return state


# Step 3: Define Graph
blog_graph = StateGraph(BlogState)

# nodes
blog_graph.add_node('create_outline', create_outline)
blog_graph.add_node('create_blog', create_blog)
blog_graph.add_node('evaluate_blog', evaluate_blog)



# edges
blog_graph.add_edge(START, 'create_outline')
blog_graph.add_edge('create_outline', 'create_blog')
blog_graph.add_edge('create_blog', 'evaluate_blog')
blog_graph.add_edge('evaluate_blog', END)
