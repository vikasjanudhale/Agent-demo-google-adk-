from google.adk import Agent
from dotenv import load_dotenv
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents import SequentialAgent,LlmAgent
from langchain_community.embeddings import OllamaEmbeddings
from google.adk.apps import App
from google.adk.plugins.save_files_as_artifacts_plugin import SaveFilesAsArtifactsPlugin

from agentic_rag_bot.sub_agent import rag_piplinene_agent,Answering_agent
load_dotenv()
main_flow_agent=LlmAgent(
    name="HelpDeskRagCoordinator",
    model="gemini-2.5-flash",
    description="Main help desk router",
    instruction="""Route user request:use seaquential agent which rag_piplinene_agent if the the user uploaded the document and asking the processing document , 
        -use anwering agent for query over the data base
        -provide the final output to the user without modifying it
        -if no relevant data found in the document reply to the user no relevant data found in the document
        """,

sub_agents=[rag_piplinene_agent,Answering_agent]

)

root_agent=main_flow_agent



app=app = App(
    name="agentic_rag_bot",
    root_agent=root_agent,
    plugins=[SaveFilesAsArtifactsPlugin()], # This line enables auto-saving of uploads
)







        
      
    

        
