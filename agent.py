from langgraph.graph import StateGraph, END

# Define the state shape
class AgentState(TypedDict):
    input: str
    plan: List[Dict]
    results: List[str]
    steps_taken: int

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", plan_node)
workflow.add_node("executor", execute_node)

# Define edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", END)

app = workflow.compile()