from agents import Agent, Runner

from ..schemas import SummarizerAgentOutput
from .prompts.summarizer_agent_prompt import SUMMARIZER_AGENT_DESCRIPTION_AS_TOOL


class SummarizerAgent(Agent):
    def __init__(self, name: str, instructions: str, *args, **kwargs):
        self.description = SUMMARIZER_AGENT_DESCRIPTION_AS_TOOL
        super().__init__(
            name=name,
            instructions=instructions,
            model = "gpt-4o-mini",
            *args,
            **kwargs
        )

    async def run_agent(self, user_input: str):
        print("calling SummarizerAgent agent")
        result = await Runner.run(self, input=user_input)
        return result.final_output


summarizer_agent = SummarizerAgent(
    name="SummarizerAgent",
    instructions=(
        "You are a text summarisation expert. "
        "Produce a concise summary and extract the key points from the given text. "
        "Always respond using the structured output format. "
    ),
    # output_type=SummarizerAgentOutput,
)
