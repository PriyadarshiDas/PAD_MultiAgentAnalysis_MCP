import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from crewai import Agent
from crewai import Crew, Task, LLM
load_dotenv()

model_name = os.getenv("MODEL")  # example: "qwen2.5:0.5b"

# Create the actual LLM object
llm = ChatOllama(
    model=model_name,
    provider="ollama",
    temperature=0.1,
    base_url="http://localhost:11434" 
)

def get_breach_judge(llm):
    return Agent(
        role="Breach Decision Maker",
        goal="Decide whether a policy is breached based on expert input",
        backstory="Experts in making logical decisions with legal grounding.",
        verbose=True,
        tools=[],
        memory=True,
        llm=llm,
        allow_delegation=False
    )
