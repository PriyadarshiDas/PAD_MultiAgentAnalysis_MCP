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
model_name = os.getenv("MODEL")

# FastAPI app instance
app = FastAPI()

# Create LLM object
llm = ChatOllama(
    model=model_name,
    provider="ollama",
    temperature=0.1,
    base_url="http://localhost:11434",
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

    # Agent setup
    analyzer = get_activity_analyzer(llm)
    policy_expert = get_policy_agent(llm)
    judge = get_breach_judge(llm)

    # Task 1: Summarize user activity
    task1 = Task(
        description=f"""
        Summarize the following banking activity in one clear sentence.

        Banking Activity: {banking_input}

        Only return the clean summary.
        """,
        expected_output="A one-line summary of the user's activity.",
        agent=analyzer,
        return_output=True
    )
    crew1 = Crew(agents=[analyzer], tasks=[task1], verbose=True)
    activity_summary = crew1.kickoff()

    # Safely cast to string (handles cases where .output doesn't exist)
    activity_summary_text = str(activity_summary)

    # Get relevant policy content
    docs = retriever.get_relevant_documents(activity_summary_text)
    if not docs:
        return {"error": "No relevant policy found for the given activity."}
    relevant_policy = docs[0].page_content

    # Task 2: Determine policy breach
    task2 = Task(
        description=f"""
        User did this: {activity_summary_text}
        Policy says: {relevant_policy}
        Does the user's activity breach the policy?.
        Respond in this format:
        Answer: Yes or No
        Reason: [A short explanation]
        """,
        expected_output="Yes/No and explanation.",
        agent=judge,
        return_output=True
    )
    crew2 = Crew(agents=[judge], tasks=[task2], verbose=True)
    decision = crew2.kickoff()
    decision_text = str(decision)

    # Return final result
    return {
        "activity_summary": activity_summary_text,
        "relevant_policy": relevant_policy,
        "decision": decision_text
    }
