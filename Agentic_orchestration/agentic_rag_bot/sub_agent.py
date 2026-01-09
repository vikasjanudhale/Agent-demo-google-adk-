from google.adk import Agent
from dotenv import load_dotenv
from google.adk.tools import FunctionTool 
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents import SequentialAgent,LlmAgent

from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
from agentic_rag_bot.tools import check_uploded_documents,chunk_embedding_vectore_store,query_document

chunk_embedded_vectores_agent=LlmAgent(
    name="chunk_embedded_vectores_agent",
    model="gemini-2.5-flash",
    description="an agent that can split the text into smaller chunks and create the embedded vector store",
    instruction=f"""You are an AI assistant that helps users by splitting the given text into smaller chunks and creating an embedded vector store for efficient retrieval.""",
    tools=[FunctionTool(func=chunk_embedding_vectore_store)],
    output_key="embedd_output"
    

)


uploded_agent=LlmAgent(
    name="uploded_agent",
    model="gemini-2.5-flash",
    description="an agent that can check the uploaded document in the artifact system",
    instruction="""You are an AI assistant that helps users by checking the uploaded documents in the artifact
        -extract the content from the particular file as it is dont add ur own
        -making the output redy for the next agent""",
    tools=[FunctionTool(func=check_uploded_documents)],
    output_key="processed_output"
    

)

    



rag_piplinene_agent=SequentialAgent(
    name="orchester_agent",
    description="ur an agent which can handle task to the subagent and return the final output without modifying it ",
    sub_agents=[uploded_agent,chunk_embedded_vectores_agent],
    
)








Answering_agent=LlmAgent(
    name="answering_agent",
    model="gemini-2.5-flash",
    description="an agent which gives response to the user query",
    instruction="""ur an quetion answering agent ur job is to retrive the data from the vector database based on the user query.
     -use the relevant to tool to query over the vectorestaore and genarate the response and update its state with the same response.
     -if u found the relevant data otherwise reply to the user that no relevant data found in the document""",
    tools=[FunctionTool(func=query_document)]

)
