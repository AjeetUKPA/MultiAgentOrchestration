from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

from langchain_agent.schemas.state import MultiAgentState
from langchain_agent.llm.llms import model

@tool
async def send_mail(receiver_email: str, subject: str, body: str) -> dict:
    """Send an email to receiver_email with the given subject and body."""

    print("tool call happened")
    return f"email sent to {receiver_email}, {subject} {body}"

fallback_agent = create_agent(
    model=model,
    system_prompt="You are a fallback agent. When other sub-agents couldn't handle the request, fallback happens to you. So handle the request accordingly",
)

email_agent = create_agent(
    model="gpt-4o-mini",
    tools=[send_mail],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_mail": True,
                "transfer_to_email": False,
            },
            description_prefix="Please approve the following mail to be sent to the user.",
        ),
    ],
    system_prompt="You are a email agent. Help with drafting, sending email to the user.",
)

# email_agent = create_agent(
#     model="gpt-4o-mini",
#     tools=[],
#     system_prompt="You are a email agent. Help with drafting, sending email to the user. If the user has asked about sending the email, use human-in-the-loop for confirmation.",
# )
from .interrupt_hander.handle_email_interrupt import handle_interrupt

async def call_email_agent(state: MultiAgentState , config: RunnableConfig):
    """Node that calls the email agent."""
    session_id = config["configurable"].get("thread_id")

    response = await email_agent.ainvoke(state, config={"configurable": {"thread_id": session_id}})
    return response

async def call_fallback_agent(state: MultiAgentState, config: RunnableConfig):
    """Node that calls the fallback."""
    session_id = config["configurable"].get("thread_id")
    response = await fallback_agent.ainvoke(state, config={"configurable": {"thread_id": session_id}})
    return response
