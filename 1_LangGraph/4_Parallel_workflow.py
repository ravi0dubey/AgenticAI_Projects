from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# instead of returning state in parallel workflow, we return only the computed value as dictionary

# Step 1: Define Cricket State
class cricketState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float
    boundary_percentage: float
    balls_per_boundary: float
    summary : str
    
# Step 2: Define functions to calculate strike rate
def calculate_strike_rate(state: cricketState):
    runs = state['runs']
    balls = state['balls']
    strike_rate = round((runs / balls) * 100, 2) if balls > 0 else 0.0
    return {'strike_rate': strike_rate}

# Step 3: Define functions to calculate boundary percentage
def calculate_boundary_percentage(state: cricketState):
    runs = state['runs']
    boundary_runs = (state['fours'] * 4) + (state['sixes'] * 6)
    boundary_percentage = round((boundary_runs / runs) * 100, 2) if runs > 0 else 0.0
    return {'boundary_percentage': boundary_percentage}

# Step 4: Define functions to calculate balls per boundary
def calculate_balls_per_boundary(state: cricketState):
    balls = state['balls']
    boundaries = state['fours'] + state['sixes']
    balls_per_boundary = round(balls / boundaries, 2) if boundaries > 0 else 0.0
    return {'balls_per_boundary': balls_per_boundary}

# Step 5: Define function to summarize performance
def summary(state: cricketState):
    summary = f"""Performance Summary:\n
      Strike Rate: {state['strike_rate']} \n
      Boundary Percentage: {state['boundary_percentage']} \n
      Balls per Boundary: {state['balls_per_boundary']}"""
    return {'summary': summary}

# Step 6: Create StateGraph and add nodes and edges
cricket_graph = StateGraph(cricketState)

# Step 7: Add nodes to the graph
cricket_graph.add_node('calculate_strike_rate', calculate_strike_rate)
cricket_graph.add_node('calculate_boundary_percentage', calculate_boundary_percentage)
cricket_graph.add_node('calculate_balls_per_boundary', calculate_balls_per_boundary)
cricket_graph.add_node('summary', summary)

# Step 8: Define edges to create parallel workflow
cricket_graph.add_edge(START, 'calculate_strike_rate')
cricket_graph.add_edge(START, 'calculate_boundary_percentage')
cricket_graph.add_edge(START, 'calculate_balls_per_boundary')
cricket_graph.add_edge('calculate_strike_rate', 'summary')
cricket_graph.add_edge('calculate_boundary_percentage', 'summary')        
cricket_graph.add_edge('calculate_balls_per_boundary', 'summary')
cricket_graph.add_edge('summary', END)



workflow= cricket_graph.compile()


initial_data = {
    "runs": 150,
    "balls": 120, 
    "fours": 15,
    "sixes": 5,
    "strike_rate": 0.0,
    "boundary_percentage": 0.0,
    "balls_per_boundary": 0.0,
    "summary": ""
}           

cricket_result = workflow.invoke(initial_data)
print(f"Strike Rate: {cricket_result['strike_rate']}")
print(f"Boundary Percentage: {cricket_result['boundary_percentage']}")
print(f"Balls per Boundary: {cricket_result['balls_per_boundary']}")
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())
