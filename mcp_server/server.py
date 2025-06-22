import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from agents.policy_expert import get_policy_agent
from agents.activity_analyzer import get_activity_analyzer
from agents.breach_judge import get_breach_judge
from retriever.policy_retriever import setup_retriever

from crewai import Crew, Task
from langchain_ollama import ChatOllama


# Load environment variables
load_dotenv()
model_name = os.getenv("MODEL") or "llama3"  # fallback to llama3 if not in .env

# FastAPI app instance
app = FastAPI()

# Create LLM object
llm = ChatOllama(
    model=model_name,
    temperature=0.1,
    max_tokens=1000
)



# PDF Retriever setup
retriever = setup_retriever("data/policies/company_policy.pdf")

# Pydantic schema for request
class AnalyzeRequest(BaseModel):
    banking_activity: str

# Main API endpoint
@app.post("/analyze")
async def analyze_policy(request: AnalyzeRequest):
    banking_input = request.banking_activity

    # Agents setup
    analyzer = get_activity_analyzer(llm)
    policy_expert = get_policy_agent(llm)
    judge = get_breach_judge(llm)

    # Task 1: Analyze Activity
    task1 = Task(
        description=f"Analyze this banking activity and summarize it:\n{banking_input}",
        expected_output="A summary of the user's action.",
        agent=analyzer
    )
    crew1 = Crew(agents=[analyzer], tasks=[task1], verbose=True)
    activity_summary = crew1.kickoff()

    # Retrieve policy document based on summary
    relevant_policy = retriever.get_relevant_documents(activity_summary)[0].page_content

    # Task 2: Judge for policy breach
    task2 = Task(
        description=f"""
        User did this: {activity_summary}
        Policy says: {relevant_policy}
        Determine if the user's action breaches the policy. Give a Yes/No and explain.
        """,
        expected_output="Yes/No and explanation.",
        agent=judge
    )
    crew2 = Crew(agents=[judge], tasks=[task2], verbose=True)
    decision = crew2.kickoff()

    return {
        "activity_summary": activity_summary,
        "relevant_policy": relevant_policy,
        "decision": decision
    }
