import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crewai_tools import MCPServerAdapter
from mcp import StreamableHTTPServerParameters

from agents.policy_expert import get_policy_agent
from agents.activity_analyzer import get_activity_analyzer
from agents.breach_judge import get_breach_judge
from retriever.policy_retriever import setup_retriever

from crewai import Crew, Task
from langchain_ollama import ChatOllama

# Load .env vars
load_dotenv()
model_name = os.getenv("MODEL", "llama3")  # fallback default

# === 1. Create FastAPI App ===
app = FastAPI()

# === 2. Enable CORS for browser requests (frontend) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 3. LLM Setup ===
llm = ChatOllama(
    model=model_name,
    provider="ollama",
    base_url="http://localhost:11434",
    temperature=0.1,
    max_tokens=1000
)

# === 4. PDF Retriever Setup ===
retriever = setup_retriever("data/policies/company_policy.pdf")

# === 5. Request Schema ===
class AnalyzeRequest(BaseModel):
    banking_activity: str

# === 6. POST Endpoint ===
@app.post("/analyze")
async def analyze_policy(request: AnalyzeRequest):
    banking_input = request.banking_activity

    # Set MCP Adapter Params
    mcp_params = StreamableHTTPServerParameters(
        url="http://localhost:8001/mcp",
        transport="streamable-http"
    )

    # Use tools from MCP
    with MCPServerAdapter(mcp_params) as mcp_tools:
        print(f"✔ MCP Tools Loaded: {[tool.name for tool in mcp_tools]}")

        # Create agents with tools
        analyzer = get_activity_analyzer(llm, tools=mcp_tools)
        policy_expert = get_policy_agent(llm, tools=mcp_tools)
        judge = get_breach_judge(llm, tools=mcp_tools)

        # === Task 1: Activity Summary ===
        task1 = Task(
            description=f"""
            Summarize the following banking activity in one sentence:
            {banking_input}
            """,
            expected_output="A one-line summary.",
            agent=analyzer,
            return_output=True
        )
        crew1 = Crew(agents=[analyzer], tasks=[task1], verbose=True)
        activity_summary = str(crew1.kickoff())

        # === Retrieve Policy ===
        docs = retriever.get_relevant_documents(activity_summary)
        if not docs:
            return {"error": "No relevant policy found for this activity."}
        relevant_policy = docs[0].page_content

        # === Task 2: Breach Judgment ===
        task2 = Task(
            description=f"""
            The user did this: {activity_summary}
            The policy says: {relevant_policy}

            Does this activity breach the policy?
            Respond in:
            Answer: Yes/No
            Reason: Explanation
            """,
            expected_output="Answer and explanation.",
            agent=judge,
            return_output=True
        )
        crew2 = Crew(agents=[judge], tasks=[task2], verbose=True)
        decision = str(crew2.kickoff())

        # === Final Response ===
        return {
            "activity_summary": activity_summary,
            "relevant_policy": relevant_policy,
            "decision": decision
        }