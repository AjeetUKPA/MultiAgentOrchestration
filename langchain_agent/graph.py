from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import GraphOutput
from langchain_agent.schemas.state import MultiAgentState
from langchain_agent.custom_agents.orchestrator_agent import (
    call_orchestrator_agent,
    route_initial,
    route_after_translate_agent,
    route_after_summarise_agent,
)
from langchain_agent.custom_agents.summarizer_agent import call_summarise_agent
from langchain_agent.custom_agents.translator_agent import call_translate_agent
from langchain_agent.custom_agents.email_agent import call_email_agent, call_fallback_agent

from langchain_agent.schemas.agent_schemas.graph_input_schema import GraphInput

class GraphBuilder:
    def __init__(self):
        self.builder = StateGraph(MultiAgentState)
        self.checkpointer = InMemorySaver()
        self.graph = None
        self._build()

    def _build(self):
        self._build_nodes()
        self._build_edges()
        self.graph = self.builder.compile(
            checkpointer = self.checkpointer,
            )

    def get_graph(self):
        return self.graph
    
    def get_state(self, session_id):
        config = {"configurable": {"thread_id": session_id}}
        return self.graph.get_state(config)

    async def run(self, user_input, session_id: str):
        config={
            "configurable": {
                "thread_id": session_id
                }
            }
        if self.graph is None:
            raise RuntimeError("Graph is not built. Please build the graph first.")
        result = await self.graph.ainvoke(
            user_input,
            version="v2",
            config=config,
            )
        print("\n\n\n")
        states = self.graph.get_state(config)
        print(states)
        # result = result.value['interrupts']
        return result

    def _build_nodes(self):
        self.builder.add_node("orchestrator_agent", call_orchestrator_agent)
        self.builder.add_node("email_agent", call_email_agent)
        self.builder.add_node("fallback_agent", call_fallback_agent)
        self.builder.add_node("translate_agent", call_translate_agent)
        self.builder.add_node("summarise_agent", call_summarise_agent)

    def _build_edges(self):
        self.builder.add_edge(
            "__start__",
            "orchestrator_agent"
        )
        self.builder.add_conditional_edges(
            "orchestrator_agent", 
            route_initial,
            [
                "summarise_agent", 
                "translate_agent", 
                "fallback_agent", 
                "email_agent", 
                "__end__"
            ]
        )
        self.builder.add_conditional_edges(
            "summarise_agent", 
            route_after_summarise_agent, 
            [
                "translate_agent", 
                "email_agent", 
                END
            ]
        )
        self.builder.add_conditional_edges(
            "translate_agent", 
            route_after_translate_agent, [
                "email_agent", 
                END
            ]
        )
graph = GraphBuilder()
