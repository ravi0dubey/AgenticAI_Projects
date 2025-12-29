import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Step2 : Create Pydantic Class to store the feedback in structured format
class evaluation_tweet_schema(BaseModel):
   evaluation_of_the_tweet: Literal ["Okay", "NotOkay"] = Field(description="Evaluation of the tweet")


# Step1 : Declare LLM Models each having specific tasks
generator_llm= ChatOpenAI(model = "gpt-4o",temperature=0, api_key=os.getenv("OPEN_API_KEY") )
evaluator_llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )
optimizer_llm= ChatOpenAI(model = "gpt-4o",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step3 : Create Structured Model using eithre Json Schema or Pydantic Class
strcutured_evaluator_llm_model = evaluator_llm.with_structured_output(evaluation_tweet_schema)


# Step2 : Define workflow state
class TweetTopicState(TypedDict):
    topic : str
    tweet_generated_on_the_topic : str
    evaluation_of_the_tweet: Literal ["Okay", "NotOkay"]
    optimized_tweet_on_the_topic: str


def generate_tweet_for_the_topic(state: TweetTopicState):
    topic = state["topic"]
    prompt = f"Using the {topic}, generate 2 liner, original and funny tweet which engages audience"
    response = generator_llm.invoke(prompt).content
    print(response)
    tweet_generated_on_the_topic = response
    return {'tweet_generated_on_the_topic': tweet_generated_on_the_topic}


def tweet_it(state : TweetTopicState):
    tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
    return {'tweet_generated_on_the_topic', tweet_generated_on_the_topic}

def optimize_the_tweet(state: TweetTopicState):
    tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
    prompt = f"Optimize the {tweet_generated_on_the_topic} to make it more original and funny"
    optimized_tweet_on_the_topic = optimizer_llm.invoke(prompt).optimized_tweet_on_the_topic
    return{'optimized_tweet_on_the_topic': optimized_tweet_on_the_topic}

def evaluate_the_tweet_for_the_topic(state: TweetTopicState) -> Literal['tweet_it','optimize_the_tweet']:
    tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
    evaluation_of_the_tweet = state["evaluation_of_the_tweet"]
    prompt = f"Evaluate the {tweet_generated_on_the_topic} on the parameters its original and funny and let us know the criteria where it falls {evaluation_of_the_tweet}"
    response = strcutured_evaluator_llm_model.invoke(prompt).evaluation_of_the_tweet
    if response == 'Okay':
        return 'tweet_it'
    else:
        return 'optimize_the_tweet'

# Step 8: Create StateGraph and add nodes and edges
tweet_topic_state = StateGraph(TweetTopicState)

# Step 9 : Add the Node
tweet_topic_state.add_node('generate_tweet_for_the_topic',generate_tweet_for_the_topic)
# tweet_topic_state.add_node('evaluate_the_tweet_for_the_topic',evaluate_the_tweet_for_the_topic)
tweet_topic_state.add_node('optimize_the_tweet',optimize_the_tweet)
tweet_topic_state.add_node('tweet_it',tweet_it)

# Step 10 : Add the Edge

tweet_topic_state.add_edge(START, 'generate_tweet_for_the_topic')
tweet_topic_state.add_conditional_edges('generate_tweet_for_the_topic',evaluate_the_tweet_for_the_topic )
tweet_topic_state.add_edge('optimize_the_tweet','generate_tweet_for_the_topic')
tweet_topic_state.add_edge('tweet_it', END)

# Step 11: Compile the workflow
workflow= tweet_topic_state.compile()


# Step 12: Define initial state
initial_state: TweetTopicState = {
    'topic' : 'Banning Phones in Schools',
    'tweet_generated_on_the_topic' : ' ',
    'evaluation_of_the_tweet': ' ',
    'optimized_tweet_on_the_topic' : ' ' ,

}

# Step 13: Execute the workflow with an initial state
final_state = workflow.invoke(initial_state)
print(final_state)

# Step 14: Visualize the workflow
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())




