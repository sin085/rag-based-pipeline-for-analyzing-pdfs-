import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
load_dotenv()
# Setup API Key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class Task(BaseModel):
    description: str
    priority: str
    tool: str

class Plan(BaseModel):
    tasks: List[Task]

def generate_plan(user_input: str):
    # Initialize the model with the JSON constraint
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": Plan
        }
    )
    
    prompt = f"""
    You are an AI Task Planner. Extract actionable tasks from this input:
    "{user_input}"
    
    Available tools: email_tool, calendar_tool, general_tool.
    Assign priorities: High, Medium, Low.
    """
    
    response = model.generate_content(prompt)
    return response.text