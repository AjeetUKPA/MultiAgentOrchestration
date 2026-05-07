from enum import Enum

from pydantic import BaseModel


class AgentSelector(str, Enum):
    all = "all"
    email_agent = "email_agent"
    summarizer_agent = "summarizer_agent"
    translator_agent = "translator_agent"


class RunRequest(BaseModel):
    user_input: str
    agent: AgentSelector = AgentSelector.all
    session_id: str = "default"
