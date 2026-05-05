from enum import Enum

from pydantic import BaseModel, Field

class AgentSelector(str, Enum):
    all = "all"
    email_agent = "email_agent"
    summarizer_agent = "summarizer_agent"
    translator_agent = "translator_agent"


class RunRequest(BaseModel):
    user_input: str = Field(
        ...,
        description="Natural-language instruction for the agent",
        examples=["Translate 'Good morning' into Spanish"],
    )
    agent: AgentSelector = Field(
        AgentSelector.all,
        description=(
            "Select which agent handles the request.  "
            "Use **all** to let the orchestrator route automatically."
        ),
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_input": "Summarise the history of the internet in three sentences.",
                    "agent": "all",
                },
                {
                    "user_input": "Draft a follow-up email about the project deadline.",
                    "agent": "email_agent",
                },
                {
                    "user_input": "Summarise: AI is changing how businesses operate worldwide.",
                    "agent": "summarizer_agent",
                },
                {
                    "user_input": "Translate 'Hello, how are you?' into Hindi",
                    "agent": "translator_agent",
                },
            ]
        }
    }
