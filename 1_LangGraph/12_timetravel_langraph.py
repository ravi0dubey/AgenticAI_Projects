import os
from langgraph.graph import StateGraph, START,  END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Step1: Declare Model
model_openapi= ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step2: Define JokeState
class JokeState(TypedDict):
    topic: str
    joke: str
    explanation: str

# Step3: Define function to generate joke
def generate_joke(state:JokeState):
    topic = state["topic"]
    prompt = f'generate a joke on the topic:{topic}'
    response = model_openapi.invoke(prompt).content
    return {'joke': response}

# Step4: Define function to generate explanation of the Joke
def generate_explanation_on_joke(state: JokeState):
    joke = state["joke"]
    prompt = f'generate explanation on the joke: {joke}'
    response = model_openapi.invoke(prompt).content
    return {'explanation' : response}

# Step5: Define Joke Graph
joke_graph = StateGraph(JokeState)

# Step6: Add Node
joke_graph.add_node('generate_joke', generate_joke)
joke_graph.add_node('generate_explanation_on_joke', generate_explanation_on_joke)

# Step7 : Add Edges
joke_graph.add_edge(START,'generate_joke')
joke_graph.add_edge('generate_joke','generate_explanation_on_joke')
joke_graph.add_edge('generate_explanation_on_joke', END)

# Step8 : Adding checkpointer
joke_checkpointer = InMemorySaver()

# Step9 : Compile the graph
joke_workflow = joke_graph.compile(checkpointer=joke_checkpointer)

# Step10 : Initial configuration
joke_config1 = {'configurable': {'thread_id': '1'}}

# Step 11: Define initial state for First topic of the joke
initial_state: JokeState = {
    'topic' : 'pineapple',
    'joke' : ' ',
    'explanation': ' ',
}

# Step 12 : Invoke the Graph
joke_final_state = joke_workflow.invoke(initial_state, config= joke_config1)
print(joke_final_state)

# Step 13 : Print Joke_state
print(f'joke_state_ : {joke_workflow.get_state(joke_config1)}')
print(f'joke_state_history : {list(joke_workflow.get_state_history(joke_config1))}')


# Step14 : Putting checkpoint id of generate_joke
joke_config2 = {'configurable': {'thread_id': '1', "checkpoint_id":"1f0f20c3-b888-6240-8001-4c0d0f7fbc7d"}}

# Step 12 : Invoke the Graph
joke_final_state = joke_workflow.invoke( {}, config= joke_config2)
print(joke_final_state)

# Step 13 : Print Joke_state
print(f'joke_state_ : {joke_workflow.get_state( joke_config2)}')
print(f'joke_state_history : {list(joke_workflow.get_state_history(joke_config2))}')