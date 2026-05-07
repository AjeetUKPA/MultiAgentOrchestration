from typing_extensions import NotRequired
from langchain.agents import AgentState
from langgraph.types import Interrupt

class MultiAgentState(AgentState):
    active_agent: NotRequired[str]
    interrupts: tuple[Interrupt, ...]