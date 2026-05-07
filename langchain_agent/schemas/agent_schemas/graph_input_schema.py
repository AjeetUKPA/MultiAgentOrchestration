from pydantic import BaseModel


class GraphInput(BaseModel):
    role: str
    content: str