from pydantic import BaseModel


class SummarizerAgentInput(BaseModel):
    text: str


class SummarizerAgentOutput(BaseModel):
    summary: str
    key_points: list[str]
