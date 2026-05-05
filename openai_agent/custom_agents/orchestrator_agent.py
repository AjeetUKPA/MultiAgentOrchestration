from agents import Agent, Runner

from .prompts.orchestrator_agent_prompt import AGENT_ORCHESTRATOR_PROMPT
from .tool_factory import handoffs


class AgentOrchestrator(Agent):
    def __init__(
        self,
        handoffs: list,
        instructions: str = AGENT_ORCHESTRATOR_PROMPT,
        *args,
        **kwargs,
    ):
        self.agent_instructions = instructions
        super().__init__(
            instructions=self.agent_instructions,
            handoffs=handoffs,
            model = "gpt-4o-mini",
            *args,
            **kwargs,
        )

    async def run_agent(self, user_input: str):
        print("calling AgentOrchestrator agent")
        result = await Runner.run(self, input=user_input)
        print(result)
        return result
orchestrator = AgentOrchestrator(name="orchestrator_agent", handoffs=handoffs)
