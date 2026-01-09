from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from a2a.types import AgentCard
from dotenv import load_dotenv   
import os

load_dotenv()
root_agent=RemoteA2aAgent(
    #client agent name
    name="facts_agent",
    description="agent give interesting facts",
    agent_card="http://localhost:8002/.well-known/agent-card.json"
    )   

print("Starting Remote agent...",os.environ.get("GOOGLE_API_KEY"))  