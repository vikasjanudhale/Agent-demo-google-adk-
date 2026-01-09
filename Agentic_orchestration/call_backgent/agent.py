import uuid
from datetime import datetime,timezone
from typing import Optional
from google.adk.agents import Agent as llmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
def before_agent_callback(callback_context:CallbackContext)->Optional[types.Content]:
    if "session_id" not in callback_context.state:
        callback_context.state["session_id"]=str(uuid.uuid4())
    

    callback_context.state["start_interaction_time"]=datetime.now(timezone.utc)
    request_num=callback_context.state.get("request_counter",0)+1
    callback_context.state["request_counter"]=request_num
    print(
        f"\n [Before agent SID:{callback_context.state['session_id']} interaction intiated {request_num}"
    )

    print(f'time stamp:{callback_context.state["start_interaction_time"]}')
    print("\n\n")

    return None

def after_agent_callback(callback_context:CallbackContext)->Optional[types.Content]:
    start_time=callback_context.state.get("start_interaction_time",None)
    duration="N/A"
    if start_time:
        duration=(datetime.now(timezone.utc)-start_time)
        duration_str = f'{duration.total_seconds():.2f} seconds'

    print(
        f"\n[AFTER AGENT - SID: {callback_context.state['session_id']} Interaction #{callback_context.state['request_counter']} completed."
    )
    print(f"Duration: {duration_str}")
    print("\n\n")
    return None

lifecycle_logger_agent=llmAgent(
    name='lifecycle_logger_agent',
    description="An agent that logs its lifecycle intercaction.",
    model='gemini-2.5-flash',
    instruction="Ur an eco agent repeat the user message",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback
)
root_agent=lifecycle_logger_agent







