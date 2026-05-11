import json
from typing import Literal

from langchain.agents import create_agent
from langchain.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_agent.schemas.state import MultiAgentState

from langchain_agent.llm.llms import model

orchestrator_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt="""You are an orchestrator agent. Based on the user input that is provided to you, you have to determine which of the sub-agent to call:
    1. email_agent: An agent that handles all the email related query
    2. summarise_agent: An agent that handles summairsation related query
    3. translate_agent: An agent that handles language translation related query.
    4. fallback_agent: An agent that handles query not related to email, summarization or language translation.
    Just give one word answer on the name of the agent to call and nothing else.
    """
)




async def call_orchestrator_agent(state: MultiAgentState, config: RunnableConfig):
    """Node that calls the summarise_agent."""
    session_id = config["configurable"].get("thread_id")
    response = await orchestrator_agent.ainvoke(state, config={"configurable": {"thread_id": session_id}})
    print("after calling the orchestrator agent the output is:",response["messages"][-1].content)
    state['active_agent'] = response["messages"][-1].content
    return response



def route_after_summarise_agent(
    state: MultiAgentState
    )-> Literal[
        "summarise_agent", 
        "translate_agent", 
        "email_agent",
        "fallback_agent",
        "__end__"
        ]:
    """Route based on active_agent, or END if the agent finished without handoff."""
    messages = json.loads(state['messages'][-1].content)
    state['messages'] =  messages['text']
    next_agent = messages['next_agent']
    print(f"Summarizer agent output is:{next_agent}")
    return next_agent


def route_after_translate_agent(
    state: MultiAgentState
    )-> Literal[
        "email_agent",
        "__end__"
        ]:
    """Route based on active_agent, or END if the agent finished without handoff."""
    messages = json.loads(state['messages'][-1].content)
    state['messages'] =  messages['text']
    next_agent = messages['next_agent']
    print(f"translation agent agent output is:{next_agent}")
    return next_agent

def route_initial(
        state: MultiAgentState
) -> Literal[
        "summarise_agent",
        "translate_agent",
        "email_agent",
        ]:
    print("By orchestrator agent, GOTO:",state['messages'][-1].content)
    return state['messages'][-1].content or "fallback_agent"
