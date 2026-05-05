from pydantic import BaseModel, Field


class TranslatorAgentInput(BaseModel):
    text: str = Field(..., description="The source text to be translated")
    target_language: str = Field(
        ...,
        description="Target language for translation (e.g. French, Spanish, Hindi)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Good morning, how are you?",
                    "target_language": "French",
                }
            ]
        }
    }


class TranslatorAgentOutput(BaseModel):
    translated_text: str = Field(
        ..., description="The translated text in the target language"
    )
    target_language: str = Field(
        ..., description="The language the text was translated into"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "translated_text": "Bonjour, comment allez-vous?",
                    "target_language": "French",
                }
            ]
        }
    }
