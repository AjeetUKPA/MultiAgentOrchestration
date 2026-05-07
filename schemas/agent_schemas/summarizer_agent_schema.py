from pydantic import BaseModel, Field


class SummarizerAgentInput(BaseModel):
    text: str = Field(..., description="The full text content to be summarised")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": (
                        "Artificial intelligence is transforming industries worldwide. "
                        "From healthcare to finance, organisations are adopting AI to "
                        "automate repetitive tasks, uncover insights in large datasets, "
                        "and deliver personalised experiences at scale."
                    )
                }
            ]
        }
    }


class SummarizerAgentOutput(BaseModel):
    summary: str = Field(..., description="Concise summary of the provided text")
    key_points: list[str] = Field(
        ..., description="List of key points extracted from the text"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summary": "AI is reshaping multiple industries by automating tasks and enabling data-driven decisions.",
                    "key_points": [
                        "AI adoption is widespread across industries",
                        "Automates repetitive tasks",
                        "Enables personalised experiences at scale",
                    ],
                }
            ]
        }
    }
