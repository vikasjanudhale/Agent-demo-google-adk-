from google.adk.agents import Agent as llmAgent
import re
from typing import Optional
from google.adk.models import llm_request,llm_response
from google.genai import types


PII_PATTERNS = {
    "CREDIT_CARD": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "SSN": re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"),
}
REDACTION_PLACEHOLDER = "[REDACTED PII]"

def before_model_callback():
    