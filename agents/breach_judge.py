import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from crewai import Agent
load_dotenv()

model_name = os.getenv("MODEL")  # example: "qwen2.5:0.5b"

# Create the actual LLM object
llm = ChatOllama(
    model=model_name,
    temperature=0.1,
    max_tokens=1000
)

def get_breach_judge(llm):
    return Agent(
        role="Breach Decision Maker",
        goal="Decide whether a policy is breached based on expert input",
        backstory="Makes logical decisions with legal grounding.",
        verbose=True,
        tools=[],
        memory=True,
        llm=llm
    )
