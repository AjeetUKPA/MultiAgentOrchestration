from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command


@tool
def transfer_to_summarise(
    runtime: ToolRuntime,
) -> Command:
    """Transfer to Summarise Agent."""
    latest_ai_message = next(
        msg for msg in reversed(runtime.state["messages"])
        if isinstance(msg, AIMessage))
    transfer_message = ToolMessage(
        content = "Transferred to Summarise Agent",
        tool_call_id = runtime.tool_call_id,
    )
    return Command(
        goto = "summarise_agent",
        update = {
            "active_agent": "summarise_agent",
            "messages": [latest_ai_message, transfer_message],
        },
        graph = Command.PARENT
    )


@tool
def transfer_to_translate(
    runtime:ToolRuntime,
)-> Command:
    "Transfer to Translate Agent"
    latest_ai_message = next(
        msg for msg in reversed(runtime.state["messages"])
        if isinstance(msg, AIMessage)
    )
    transfer_message = ToolMessage(
        content = "Transfer to Translate Agent",
        tool_call_id = runtime.tool_call_id,
    )
    return Command(
        goto ="translate_agent",
        update = {
            "active_agent":"translate_agent",
            "messages": [latest_ai_message, transfer_message],
        },
        graph = Command.PARENT
    )


@tool
def transfer_to_email(
    runtime:ToolRuntime,
)-> Command:
    "Transfer to Email Agent"
    latest_ai_message = next(
        msg for msg in reversed(runtime.state["messages"])
        if isinstance(msg, AIMessage)
    )
    transfer_message = ToolMessage(
        content = "Transfer to Email Agent",
        tool_call_id = runtime.tool_call_id,
    )
    return Command(
        goto ="email_agent",
        update = {
            "active_agent":"email_agent",
            "messages": [latest_ai_message, transfer_message],
        },
        graph = Command.PARENT
    )
