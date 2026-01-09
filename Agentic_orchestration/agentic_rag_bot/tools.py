
from dotenv import load_dotenv
import os
from google.adk.tools import FunctionTool
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext

import io
import pdfplumber
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

async def check_uploded_documents(tool_context:ToolContext):
    
    """
    Checks if the specified document is uploaded and available in the session state.
    Args:
        tool_context: The context object provided by the ADK framework, containing state.
    Returns:
        A confirmation message.
    """

        
    artifact_ids = await tool_context.list_artifacts()
    if not artifact_ids:
        return "No documents have been uploaded."

    print(f"Uploaded documents1vikas: {artifact_ids}")
    result=[]
   
    for artifact_id in artifact_ids:
        artifact = await tool_context.load_artifact(artifact_id)
        print(artifact)
        mime_type = artifact.inline_data.mime_type
        file_bytes=artifact.inline_data.data
        filename=artifact.inline_data.display_name
        file_steram=io.BytesIO(file_bytes)
        text=""
        if mime_type == "application/pdf":
            with pdfplumber.open(file_steram) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        elif mime_type in ["text/plain", "text/csv"]:
            text=file_bytes.decode('utf-8')
        else:
            text=f"Unsupported file type: {mime_type} please provide the correct mime type"
        result.append({
            "filename":filename,
            "mime_type":mime_type,
            "content":text.strip()
        })
    return{
        "processed_files":len(result),
        "files":result
    }




async def chunk_embedding_vectore_store(tool_context:ToolContext):
    """Splits the given text into smaller chunks for processing.
    Args:
        text: The text to be split.
    Returns:
        A list of text chunks.
    """
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
   
    text = tool_context.state.get("processed_output")
    print(text)


    if not text:
        return "No output found from the uploaded_agent."
    chunks=text_splitter.split_text(text)
    print(chunks)
    embeddings=OllamaEmbeddings(model="all-minilm:latest")
    vectorstore_chroma= Chroma(
     embedding_function=embeddings,
    persist_directory="./chroma_db" 

)  
    metadatas = [{"source": "uploaded_agent_output"} for _ in chunks]
    vectorstore_chroma.add_texts(chunks,metadatas=metadatas)
    vectorstore_chroma.persist()
    print(vectorstore_chroma)
    return f"Successfully created vector store with {len(chunks)}{chunks}chunks and persisted to ./chroma_db"





async def query_document(query_text:str):
    """based on the user query search the relevant data into the vectore database
    Arg:
    query:str
    returns
    final output
    """
    print(query_text)
    embeddings=OllamaEmbeddings(model="all-minilm:latest")
    vectorstore = Chroma(
        persist_directory="/Applications/my_project/Agent_learner/parent_folder/chroma_db",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    

    # Retrieve relevant chunks
    relevant_docs = retriever.invoke(query_text)
    context_text = "\n".join([doc.page_content for doc in relevant_docs])
    print(context_text)

    return context_text
