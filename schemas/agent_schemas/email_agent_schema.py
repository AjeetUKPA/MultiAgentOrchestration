from pydantic import BaseModel, Field


class EmailAgentInput(BaseModel):
    to: str = Field(..., description="Email address of the recipient")
    subject: str = Field(..., description="Subject line of the email")
    body: str = Field(..., description="Body content of the email")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "to": "recipient@example.com",
                    "subject": "Project Update",
                    "body": "Hi, just wanted to share the latest project status...",
                }
            ]
        }
    }


class EmailAgentOutput(BaseModel):
    subject: str = Field(..., description="Drafted subject line of the email")
    body: str = Field(..., description="Drafted body content of the email")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Project Update – Q2 Summary",
                    "body": "Hi Team,\n\nHere is the Q2 project summary...",
                }
            ]
        }
    }
