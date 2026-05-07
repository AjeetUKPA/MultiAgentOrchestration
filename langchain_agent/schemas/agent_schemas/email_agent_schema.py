from pydantic import BaseModel


class EmailAgentInput(BaseModel):
    to: str
    subject: str
    body: str


class EmailAgentOutput(BaseModel):
    subject: str
    body: str
