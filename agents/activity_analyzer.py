import os
from crewai import Agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

model_name = os.getenv("MODEL")  # example: "qwen2.5:0.5b"

# Create the actual LLM object
llm = ChatOllama(
    model=model_name,
    temperature=0.1,
    max_tokens=1000
)

def get_activity_analyzer(llm):
    return Agent(
        role="Activity Analyzer",
        goal="Analyze user's banking activity and extract key actions",
        backstory="Understands transaction logs and financial behaviors.",
        verbose=True,
        tools=[],
        memory=True,
        llm=llm
    )

