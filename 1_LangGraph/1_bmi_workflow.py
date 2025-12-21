from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Step 1: Define State
class BMIState(TypedDict):
    weight: float  # in kilograms
    height: float  # in meters
    bmi: float     # Body Mass Index

# Step 2: Define calculate_bmi function
def calculate_bmi(state: BMIState) -> BMIState:
    weight = state['weight']
    height = state['height']
    state['bmi'] = round(weight / (height**2),2)
    return state    

# Step 3: Define Graph
bmi_graph = StateGraph(BMIState)     

# Step 4: Add Nodes to the graph
bmi_graph.add_node('calculate_bmi', calculate_bmi)  

# Step 5: Add Edges to your graph
bmi_graph.add_edge(START, 'calculate_bmi')
bmi_graph.add_edge('calculate_bmi', END)    

# Step 6: Compile the Graph
workflow= bmi_graph.compile()   

# Step 7: Execute the Graph with initial data
initial_data = {
    "weight": 80.85,
    "height": 1.80,
    "bmi": 0.0
}

bmi_result = workflow.invoke(initial_data)

print(f"Bmi: {bmi_result['bmi']}")


