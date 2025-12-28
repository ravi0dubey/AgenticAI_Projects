from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Step 1: Define State
class BMIState(TypedDict):
    weight: float  # in kilograms
    height: float  # in meters
    bmi: float     # Body Mass Index
    category: str  # BMI Category

# Step 2: Define calculate_bmi function
def calculate_bmi(state: BMIState) -> BMIState:
    weight = state['weight']
    height = state['height']
    state['bmi'] = round(weight / (height**2),2)
    return state    

# Step 3: Define bmi_category function
def bmi_category(state: BMIState) -> BMIState:
    bmi = state['bmi']
    if bmi < 18.5:
        state['category'] = 'Underweight'
    elif 18.5 <= bmi <= 24.99:
        state['category'] = 'Normal weight'
    elif 25 <= bmi <= 29.99:
        state['category'] = 'Overweight'
    else:
        state['category'] = 'Obesity'
    return state

# Step 4: Define Graph
bmi_graph = StateGraph(BMIState)     

# Step 5: Add Nodes to the graph
bmi_graph.add_node('calculate_bmi', calculate_bmi)  
bmi_graph.add_node('bmi_category', bmi_category)  

# Step 6: Add Edges to your graph
bmi_graph.add_edge(START, 'calculate_bmi')
bmi_graph.add_edge('calculate_bmi', 'bmi_category')
bmi_graph.add_edge('bmi_category', END)    

# Step 7: Compile the Graph
workflow= bmi_graph.compile()   

# Step 8: Execute the Graph with initial data
initial_data = {
    "weight": 80.85,
    "height": 1.80,
    "bmi": 0.0
}

bmi_result = workflow.invoke(initial_data)

print(f"Bmi: {bmi_result['bmi']}")
print(f"Category: {bmi_result['category']}")

# Step 9: Visualize the workflow
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())


