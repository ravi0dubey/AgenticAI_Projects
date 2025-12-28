from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI     
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Literal
import operator


# Load environment variables from .env file
load_dotenv()

# Step1 : Declare Model
model_openapi= ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step2 : Create Pydantic Class to store the feedback in structured format
class Feedback_Sentiment_Schema(BaseModel):
    sentiment : Literal["Positive", "Negative"] = Field(description="Positive or Negative sentiment based on the feedback provided")
    issue_type: Literal["UX","Performance", "Bug", "Support", "Other"] = Field(description="Type of issue")
    feedback_tone: Literal["Frustrated","Relaxed", "Calm"] = Field(description="Whether user is Frustrated,Relaxed")
    issue_urgency_type: Literal["Urgent","Medium", "Low"] = Field(description="Urgency of Issue, User needs to get it resolved Urgent, or normal")


# Step3 : Create Structured Model using eithre Json Schema or Pydantic Class
strcutured_model = model_openapi.with_structured_output(Feedback_Sentiment_Schema)


# Step 4: Define Essay State
class FeedbackSentiment(TypedDict):
    feedback: str
    feedback_sentiment: Literal["Positive", "Negative"]
    urgency_from_user: Literal["Urgent","Medium", "Low"]
    feedback_tone : Literal["Frustrated","Relaxed", "Calm"]
    issue_type: Literal["UX","Performance", "Bug", "Support", "Other"]
    response_to_user: str


# Step 5:
def evaluate_feedback_sentiment(state: FeedbackSentiment):
    feedback = state['feedback']
    prompt = f'Read the {feedback} and let us know if the sentimnent of feedback is Positive or Negative'
    response = strcutured_model.invoke(prompt)
    feedback_sentiment = response.sentiment
    return {'feedback_sentiment': feedback_sentiment}

  
# Step 5:
def response_for_positive_feedback(state: FeedbackSentiment):
    feedback_sentiment = state['feedback_sentiment']
    prompt = f'Based on the positive {feedback_sentiment} of the user, provide a nice reply to user, thanking him/her for the feedback'
    response_to_user = model_openapi.invoke(prompt)
    return {'response_to_user': response_to_user}

# Step 
def run_diagnosis(state: FeedbackSentiment):
    feedback = state['feedback']
    prompt = f'Read the {feedback} and let us know if tone of user is Frustrated or Relaxed, urgency type is Urgent or Normal and the type if issue'
    response = strcutured_model.invoke(prompt)
    issue_type = response.issue_type
    feedback_tone = response.feedback_tone
    urgency_from_user = response.issue_urgency_type
    return {'issue_type': issue_type, 'feedback_tone' : {feedback_tone}, 'urgency_from_user' : {urgency_from_user} }

# Step 5:
def response_for_negative_feedback(state: FeedbackSentiment):
    feedback_sentiment = state['feedback_sentiment']
    urgency_from_user= state['urgency_from_user']
    feedback_tone = state['feedback_tone']
    issue_type = state['issue_type']
    prompt = f'Based on the Negative {feedback_sentiment} of the user,understanding the issue_type {issue_type}, and the feedback_tone {feedback_tone} and acknowledging the urgency {urgency_from_user}, provide a nice reply'
    response_to_user = model_openapi.invoke(prompt)
    return {'response_to_user': response_to_user}

def conditional_check(state:FeedbackSentiment) -> Literal['response_for_positive_feedback', 'run_diagnosis']:
    feedback_sentiment = state['feedback_sentiment']
    if feedback_sentiment =='Postive':
        return 'response_for_positive_feedback'
    else :
        return 'run_diagnosis'

# Step 8: Create StateGraph and add nodes and edges
feedback_state = StateGraph(FeedbackSentiment)

# Step : Add the node
feedback_state.add_node('evaluate_feedback_sentiment', evaluate_feedback_sentiment)
feedback_state.add_node('run_diagnosis', run_diagnosis)
feedback_state.add_node('response_for_positive_feedback', response_for_positive_feedback)
feedback_state.add_node('response_for_negative_feedback',response_for_negative_feedback)


# Step : Add edges
feedback_state.add_edge(START, 'evaluate_feedback_sentiment')
feedback_state.add_conditional_edges('evaluate_feedback_sentiment',conditional_check)                                     
feedback_state.add_edge('run_diagnosis','response_for_negative_feedback')
feedback_state.add_edge('response_for_positive_feedback',END)
feedback_state.add_edge('response_for_negative_feedback',END)

# Step 11: Compile the workflow
workflow= feedback_state.compile()

# Step 12: Define initial state
initial_state: FeedbackSentiment = {
    # 'feedback' : 'This new apple phone is waste of money, Call button is not working, I cannot pick up the calls or dial a number, I need urgent replace/return of product',
    'feedback' : 'I am loving this new apple phone',
    'feedback_sentiment' : ' ',
    'urgency_from_user': ' ',
    'feedback_tone' : ' ' ,
    'issue_type': ' ',
    'response_to_user': ' '
}

# Step 13: Execute the workflow with an initial state
final_state = workflow.invoke(initial_state)
print(final_state)

# Step 14: Visualize the workflow
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())
