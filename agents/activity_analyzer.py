import os
from crewai import Agent, LLM
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

model_name = os.getenv("MODEL")  # example: "qwen2.5:0.5b"

# LLM object
llm = ChatOllama(
    model=model_name,
    provider="ollama",
    temperature=0.1,
    max_tokens=1000,
    base_url="http://localhost:11434" 
)

def get_activity_analyzer(llm, tools=[]):
    return Agent(
        role="Activity Analyzer",
        goal="Analyze user's banking activity and extract key actions",
        backstory="Expert in understanding transaction logs and financial behaviors.",
        verbose=True,
        tools=tools,
        memory=True,
        llm=llm,
        allow_delegation=True
    )

