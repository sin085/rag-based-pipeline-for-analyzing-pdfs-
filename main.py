import os
from dotenv import load_dotenv
import google.generativeai as genai

# This looks for the .env file and loads the variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
from fastapi import FastAPI
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

app = FastAPI()

# 1. Define Agent State
class AgentState(TypedDict):
    input: str
    plan: List[dict]
    results: List[str]

# 2. Define Nodes
def planner_node(state: AgentState):
    print("--- PLANNING ---")
    import json
    raw_plan = generate_plan(state["input"])
    plan_data = json.loads(raw_plan)
    return {"plan": plan_data["tasks"]}

def executor_node(state: AgentState):
    print("--- EXECUTING ---")
    results = []
    for task in state["plan"]:
        # Mock logic for execution
        res = f"Executed {task['tool']} for: {task['description']}"
        results.append(res)
    return {"results": results}

# 3. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", END)

runnable = workflow.compile()

@app.post("/run-task")
async def run_task(user_input: str):
    inputs = {"input": user_input}
    output = await runnable.ainvoke(inputs)
    return output