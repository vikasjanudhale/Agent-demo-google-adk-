# remote_a2a/facts_agent/agent.py
import os
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk import Agent
from google.adk.tools import google_search
from dotenv import load_dotenv
load_dotenv()
print("Starting Facts Agent...",os.environ.get("GOOGLE_API_KEY"))
# Define server-side agent
root_agent = Agent(
    # Agent unique identifier
    name="facts_agent",
    # Large language model to use
    model="gemini-2.0-flash",
    # Agent functionality description
    description="Agent to give interesting facts.",
    # Agent behavior instructions
    instruction=(
        "You are a helpful agent who can provide interesting facts. "
        "Use Google Search to find accurate and up-to-date information. "
        "Always provide sources for your facts."
    ),
    # Available tools list
    tools=[google_search],
)



a2a_app=to_a2a(root_agent,port=8002)
print("Facts Agent is running at port 8002")


