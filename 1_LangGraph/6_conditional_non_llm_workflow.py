from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

# Step 1: Define Quadratic State
class Quadratic(TypedDict):
    a: int
    b: int
    c: int
    discriminant: float
    equation: str
    result: str

# Step 2: Define function to create equation string
def create_equation(state: Quadratic):
    a = state['a']
    b = state['b']
    c = state['c']
    equation = f"{a}x^2 + {b}x + {c} = 0"
    return {'equation': equation}

# Step 3: Define function to calculate discriminant
def calculate_discriminant(state: Quadratic):   
    a = state['a']
    b = state['b']
    c = state['c']
    discriminant = b**2 - 4*a*c
    return {'discriminant': discriminant}   

# Step 4: Define functions for different root cases
def no_real_roots(state: Quadratic):
    result = "No real roots exist."
    return {'result': result}

# Step 5: Define function for real root
def real_roots(state: Quadratic):
    a = state['a']
    b = state['b']
    c = state['c']
    root1 = (-b + (b**2 - 4*a*c)**0.5) / (2 * a)
    root2 = (-b - (b**2 - 4*a*c)**0.5) / (2 * a)
    result = f"Two distinct real roots exist: x1 = {root1}, x2 = {root2}"
    return {'result': result}

# Step 6: Define function for two repeated real roots
def repeated_roots(state: Quadratic):
    a = state['a']
    b = state['b']
    root = -b / (2 * a)
    result = f"Two repeated real roots exist: x1 = x2 = {root}"
    return {'result': result}


# Step 7: Create Conditional Workflow
def check_condition(state: Quadratic) -> Literal['no_real_roots', 'real_roots', 'repeated_roots']:
    discriminant = state['discriminant']
    if discriminant < 0:
        return 'no_real_roots'
    elif discriminant == 0:
        return 'real_root'
    else:
        return 'repeated_roots'
    

# Step 8: Create StateGraph and add nodes and edges
quadratic_graph = StateGraph(Quadratic)

# Step 9: Add nodes to the graph
quadratic_graph.add_node('create_equation', create_equation)
quadratic_graph.add_node('calculate_discriminant', calculate_discriminant)
quadratic_graph.add_node('no_real_roots', no_real_roots)
quadratic_graph.add_node('real_roots', real_roots)
quadratic_graph.add_node('repeated_roots', repeated_roots)

# Step 10: Define edges to create conditional workflow
quadratic_graph.add_edge(START, 'create_equation')
quadratic_graph.add_edge('create_equation', 'calculate_discriminant')
quadratic_graph.add_conditional_edges('calculate_discriminant', check_condition)
quadratic_graph.add_edge('no_real_roots', END)
quadratic_graph.add_edge('real_roots', END)
quadratic_graph.add_edge('repeated_roots', END)
             
# Step 11: Compile the workflow
workflow= quadratic_graph.compile()

# Step 12: Define initial state
initial_state: Quadratic = {
    'a': 1,
    'b': 1,
    'c': 1,
    'discriminant': 0.0,
    'equation': '',
    'result': ''
}

# Step 13: Execute the workflow with an initial state
final_state = workflow.invoke(initial_state)
print(final_state)

# Step 14: Visualize the workflow
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())

