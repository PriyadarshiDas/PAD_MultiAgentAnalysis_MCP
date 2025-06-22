import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from retriever.policy_retriever import setup_retriever
from langchain_ollama import ChatOllama

load_dotenv()

model_name = os.getenv("MODEL")  # example: "qwen2.5:0.5b"

# Create the actual LLM object
llm = ChatOllama(
    model=model_name,
    provider="ollama",
    temperature=0.1,
    max_tokens=1000,
    base_url="http://localhost:11434" 
)

def get_policy_agent(llm, tools=[]):
    return Agent(
        role="Policy Expert",
        goal="Interpret company policy clauses relevant to banking activities",
        backstory="An expert in legal compliance and digital policy governance.",
        verbose=True,
        tools=tools,
        memory=True,
        llm=llm,
        allow_delegation=True
    )