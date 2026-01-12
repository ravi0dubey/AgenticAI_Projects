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


class JokeState(TypedDict):
    topic: str
    joke: str
    explanation: str


def generate_joke(state:JokeState):
    topic = state["topic"]
    prompt = f'generate a joke on the topic:{topic}'
    response = model_openapi.invoke(prompt).content
    return {'joke': response}

def generate_explanation_on_joke(state: JokeState):
    joke = state["joke"]
    prompt = f'generate explanation on the joke: {joke}'
    response = model_openapi.invoke(prompt).content
    return {'explanation' : response}


