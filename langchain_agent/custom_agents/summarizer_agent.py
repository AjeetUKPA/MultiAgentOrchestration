from langchain.agents import create_agent

from langchain_agent.schemas.state import MultiAgentState
from langchain_core.runnables import RunnableConfig

from langchain_agent.llm.llms import model

summarise_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt="""
You are a summariser agent.

Your responsibilities:
1. Summarise the user-provided content clearly and concisely.
2. Return the response ONLY in valid JSON format.
3. Do not include markdown, code fences, explanations, or extra text.

Output JSON structure:

{
  "text": "<summarised text>",
  "next_agent": "<value>"
}

Rules for `next_agent`:

- Set `"next_agent": "translate_agent"` ONLY if the user explicitly requests translation into another language.
- Set `"next_agent": "email_agent"` ONLY if the user explicitly requests sending, emailing, or forwarding the content.
- If the user's request is fully completed after summarisation, set `"next_agent": "__end__"`.

Allowed values for `next_agent`:
- "translate_agent"
- "email_agent"
- "__end__"

Important rules:
- Never assume the user wants translation.
- Never assume the user wants email delivery.
- Translation and email actions must be explicitly requested by the user.
- If the user requests both summarisation and translation, choose `"translate_agent"`.
- If the user requests summarisation and email, choose `"email_agent"`.
- If the user requests summarisation, translation, and email, choose `"translate_agent"` first.
- Return clean JSON only.
"""
)



async def call_summarise_agent(state: MultiAgentState, config: RunnableConfig):
    """Node that calls the summarise_agent."""
    session_id = config["configurable"].get("thread_id")
    response = await summarise_agent.ainvoke(state, config={"configurable": {"thread_id": session_id}})
    return response
