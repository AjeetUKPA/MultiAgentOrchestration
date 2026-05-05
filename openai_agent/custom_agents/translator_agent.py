from agents import Agent, Runner

from ..schemas import TranslatorAgentOutput
from .prompts.translator_agent_prompt import TRANSLATOR_AGENT_DESCRIPTION_AS_TOOL


class TranslatorAgent(Agent):
    def __init__(self, name: str, instructions: str, *args, **kwargs):
        self.description = TRANSLATOR_AGENT_DESCRIPTION_AS_TOOL
        super().__init__(
            name=name,
            instructions=instructions,
            model = "gpt-4o-mini",
            *args,
            **kwargs
        )

    async def run_agent(self, user_input: str):
        print("calling TranslatorAgent agent")
        result = await Runner.run(self, input=user_input)
        return result.final_output


translator_agent = TranslatorAgent(
    name="TranslatorAgent",
    instructions=(
        """You are a professional language translator. 
            Translate the given text accurately into the specified target language. 
            Always respond using the structured output format. """
    ),
    # output_type=TranslatorAgentOutput,
)
