from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI     
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Optional, Literal


# Load environment variables from .env file
load_dotenv()

# Step1 : Declare Model
model_openapi= ChatOpenAI(model = "gpt-4o-mini",temperature=0, api_key=os.getenv("OPEN_API_KEY") )

# Step2 : Create Json Schema to receive structured output from the model
json_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "feedback": {
      "type": "string",
      "description": "Feedback on the essay based on the criteria provided"
    },
    "score": {
      "type": "integer",
      "description": "Return a score from 1 to 10 where 1 being lowest and 10 being highest"
    },

  },
  "required": ["feedback", "score"]
}


# Step2 : Create Pydantic Class to store the feedback in structured format
class Review_annotated(BaseModel):
    feedback : str = Field(description="Feedback on the essay based on the criteria provided")
    score : int = Field(description="Return a score from 1 to 10 where 1 being lowest and 10 being highest")

# Step3 : Create Structured Model using eithre Json Schema or Pydantic Class
strcutured_model = model_openapi.with_structured_output(json_schema)
strcutured_model_annotated = model_openapi.with_pydantic_output(Review_annotated)


# Step 4: Define Essay State
class EssayState(TypedDict):
    essay: str
    feedback_on_clarity_of_thoughts: str
    feedback_score_on_clarity_of_thoughts: int
    feedback_on_depths_of_analysis_:  str
    feedback_score_on_depths_of_analysis: int
    feedback_on_language_of_essay: str
    feedback_score_on_language_of_essay: int
    final_feedback: str
    final_feedback_score: int

# Step 5: Create evaluate_essay_for_clarity_of_thoughts Function
def evaluate_essay_for_clarity_of_thoughts(state: EssayState):
    essay = state['essay']
    prompt = f'Read the following essay: {essay} and provide feedback on the clarity of thoughts presented in the essay along with a score out of 10.'
    feedback = strcutured_model.invoke(prompt)
    feedback_score_on_clarity_of_thoughts: int = int(feedback["score"])
    feedback_on_clarity_of_thoughts: str = feedback["feedback"]    
    return {'feedback_on_clarity_of_thoughts': feedback_on_clarity_of_thoughts, 'feedback_score_on_clarity_of_thoughts': feedback_score_on_clarity_of_thoughts}   


# Step 6: Create evaluate_essay_for_depths_of_analysis Function
def evaluate_essay_for_depths_of_analysis(state: EssayState):           
    essay = state['essay']
    prompt = f'Read the following essay: {essay} and provide feedback on the depths of analysis presented in the essay along with a score out of 10.'
    feedback = strcutured_model.invoke(prompt)
    print(feedback)
    feedback_score_on_depths_of_analysis: int = int(feedback["score"])
    feedback_on_depths_of_analysis_: str = feedback["feedback"]
    return {'feedback_on_depths_of_analysis_': feedback_on_depths_of_analysis_, 'feedback_score_on_depths_of_analysis': feedback_score_on_depths_of_analysis}

# Step 7: Create evaluate_essay_for_language_of_essay Function
def evaluate_essay_for_language_of_essay(state: EssayState):           
    essay = state['essay']
    prompt = f'Read the following essay: {essay} and provide feedback on the language of the essay along with a score out of 10.'
    feedback = strcutured_model.invoke(prompt)
    feedback_score_on_language_of_essay: int = int(feedback["score"])
    feedback_on_language_of_essay: str = feedback["feedback"]    
    return {'feedback_on_language_of_essay': feedback_on_language_of_essay, 'feedback_score_on_language_of_essay': feedback_score_on_language_of_essay}


# Step 8: Create compile_final_feedback Function
def compile_final_feedback(state: EssayState):
    clarity_score = state['feedback_score_on_clarity_of_thoughts']
    depth_score = state['feedback_score_on_depths_of_analysis']
    language_score = state['feedback_score_on_language_of_essay']
    final_feedback_score = round((clarity_score + depth_score + language_score) / 3, 2)
    final_feedback = f"""Final Feedback Summary:\n
      Clarity of Thoughts: {state['feedback_on_clarity_of_thoughts']} (Score: {clarity_score}) \n
      Depths of Analysis: {state['feedback_on_depths_of_analysis_']} (Score: {depth_score}) \n
      Language of Essay: {state['feedback_on_language_of_essay']} (Score: {language_score}) \n
      Overall Score: {final_feedback_score}"""
    return {'final_feedback': final_feedback, 'final_feedback_score': final_feedback_score} 

# Step 9: Create StateGraph and add nodes and edges
cricket_graph = StateGraph(EssayState)

# Step 10: Add nodes to the graph
cricket_graph.add_node('evaluate_essay_for_clarity_of_thoughts', evaluate_essay_for_clarity_of_thoughts)
cricket_graph.add_node('evaluate_essay_for_depths_of_analysis', evaluate_essay_for_depths_of_analysis)
cricket_graph.add_node('evaluate_essay_for_language_of_essay', evaluate_essay_for_language_of_essay)
cricket_graph.add_node('compile_final_feedback', compile_final_feedback)    

# Step 11: Define edges to create parallel workflow
cricket_graph.add_edge(START, 'evaluate_essay_for_clarity_of_thoughts')
cricket_graph.add_edge(START, 'evaluate_essay_for_depths_of_analysis')
cricket_graph.add_edge(START, 'evaluate_essay_for_language_of_essay')
cricket_graph.add_edge('evaluate_essay_for_clarity_of_thoughts', 'compile_final_feedback')
cricket_graph.add_edge('evaluate_essay_for_depths_of_analysis', 'compile_final_feedback')
cricket_graph.add_edge('evaluate_essay_for_language_of_essay', 'compile_final_feedback')
cricket_graph.add_edge('compile_final_feedback', END)

# step 12: Compile the workflow
workflow= cricket_graph.compile()

from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())

# Step 13 : ready essay from text file and pass as parameter in initial data
with open("5_parallel_blog_workflow_essay.txt", "r") as file:
    essay_text = file.read()    


# Step 14: Run the workflow with initial input data
input_data= {
    "essay": essay_text,
    'feedback_on_clarity_of_thoughts' : " ",
    'feedback_score_on_clarity_of_thoughts': 0,
    'feedback_on_depths_of_analysis_': " ",
    'feedback_score_on_depths_of_analysis': 0,
    'feedback_on_language_of_essay': " ",
    'feedback_score_on_language_of_essay': 0,
    'final_feedback': " ",
    'final_feedback_score': 0
}       

# Step 15: Invoke the workflow
result = workflow.invoke(input_data)

print(f"Final Feedback Score: {result['final_feedback_score']}")
print(f"Detailed Feedback: {result['final_feedback']}")