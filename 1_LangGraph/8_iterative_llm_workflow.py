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
   evaluation_of_the_tweet: Literal ["approved", "needs_improvement"] = Field(description="Evaluation of the tweet")


# Step1 : Declare LLM Models each having specific tasks
generator_llm= ChatOpenAI(model = "gpt-4o",temperature=0, api_key=os.getenv("OPEN_API_KEY") )
evaluator_llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )
optimizer_llm= ChatOpenAI(model = "gpt-4o",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step3 : Create Structured Model using eithre Json Schema or Pydantic Class
strcutured_evaluator_llm_model = evaluator_llm.with_structured_output(evaluation_tweet_schema)


# Step2 : Define workflow state
class TweetOnTopicState(TypedDict):
    topic : str
    tweet_generated_on_the_topic : str
    evaluation_of_the_tweet: Literal ["approved", "needs_improvement"]
    optimized_tweet_on_the_topic: str
    iteration: int
    max_iteration: int


def generate_tweet_for_the_topic(state: TweetOnTopicState):
    # creating prompt
    topic = state["topic"]
    max_iteration = state['max_iteration'] + 1
    messages=[
        SystemMessage(content="You are Funny and clever Twitter/X Influencer."),
        HumanMessage(content=f"""
                    Write a short, original, and hilarious tweet on the topic {topic}.
                    Rules
                    1. Do not use question-answer format.
                    2. Max 280 Characters.
                    3. Use Observational humor, irony, sarcasm, or cultural refernces.
                    4. Think in mem logic, punchlines, or relatable takes.
                    5. Use simple, day to day english
                    6. This is version {max_iteration}.
                     """)
    ]
    tweet_generated_on_the_topic = generator_llm.invoke(messages).content
    print(tweet_generated_on_the_topic)  
    return {'tweet_generated_on_the_topic': tweet_generated_on_the_topic}


def tweet_it(state : TweetOnTopicState):
    tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
    return {'tweet_generated_on_the_topic', tweet_generated_on_the_topic}

def optimize_the_tweet(state: TweetOnTopicState):
    optimized_tweet_on_the_topic= state['tweet_generated_on_the_topic']
    max_iteration = state['max_iteration'] + 1
    if max_iteration > 5:
        tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
        prompt = f"Optimize the {tweet_generated_on_the_topic} to make it more original and funny"
        optimized_tweet_on_the_topic = optimizer_llm.invoke(prompt).optimized_tweet_on_the_topic
    return{'optimized_tweet_on_the_topic': optimized_tweet_on_the_topic, 'max_iteration': max_iteration}

def evaluate_the_tweet_for_the_topic(state: TweetOnTopicState) -> Literal['tweet_it','optimize_the_tweet']:
    tweet_generated_on_the_topic = state["tweet_generated_on_the_topic"]
    evaluation_messages =[
            SystemMessage(content="You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets based on humor, originality, virality, and tweet format."),
            HumanMessage(content=f"""
                        Evaluate the following tweet:
                        Tweet: "{tweet_generated_on_the_topic}"
                        Use the criteria below to evaluate the tweet:
                        1. Originality  Is this fresh, or have you seen it a hundred times before?  
                        2. Humor : Did it genuinely make you smile, laugh, or chuckle?  
                        3. Punchiness : Is it short, sharp, and scroll-stopping?  
                        4. Virality Potential : Would people retweet or share it?  
                        5. Format : Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)?

                        Auto-reject if:
                        - It's written in question-answer format (e.g., "Why did..." or "What happens when...")
                        - It exceeds 280 characters
                        - It reads like a traditional setup-punchline joke
                        - Dont end with generic, throwaway, or deflating lines that weaken the humor (e.g., “Masterpieces of the auntie-uncle universe” or vague summaries)

                        ### Respond ONLY in structured format:
                        - evaluation: "approved" or "needs_improvement"  
                        - feedback: One paragraph explaining the strengths and weaknesses 
                        """)
                        ]

    response = strcutured_evaluator_llm_model.invoke(evaluation_messages).evaluation_of_the_tweet
    if response == 'approved':
        return 'tweet_it'
    else:
        return 'optimize_the_tweet'

# Step 8: Create StateGraph and add nodes and edges
tweet_topic_state = StateGraph(TweetOnTopicState)

# Step 9 : Add the Node
tweet_topic_state.add_node('generate_tweet_for_the_topic',generate_tweet_for_the_topic)
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
initial_state: TweetOnTopicState = {
    'topic' : 'Banning Phones in Schools',
    'tweet_generated_on_the_topic' : ' ',
    'evaluation_of_the_tweet': ' ',
    'optimized_tweet_on_the_topic' : ' ' ,
    'iteration' : 0,
    'max_iteration': 5

}

# Step 13: Execute the workflow with an initial state
final_state = workflow.invoke(initial_state)
print(final_state)

# Step 14: Visualize the workflow
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())




