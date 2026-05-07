from pydantic import BaseModel


class TranslatorAgentInput(BaseModel):
    text: str
    target_language: str


class TranslatorAgentOutput(BaseModel):
    translated_text: str
    target_language: str
