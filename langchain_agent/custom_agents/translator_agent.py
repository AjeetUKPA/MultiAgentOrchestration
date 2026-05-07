from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig

from langchain_agent.schemas.state import MultiAgentState
from langchain_agent.custom_agents.tool_factory import transfer_to_email

from langchain_agent.llm.llms import model


translate_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt="""You are a translation agent.

Your job is to:
1. Translate the provided text into the language(s) requested by the user.
2. Return the response ONLY in valid JSON format.
3. Do not include markdown, code fences, or explanations.

Output JSON structure:

{
  "text": "<translated text>",
  "next_agent": "<value>"
}

Rules for `next_agent`:

- Set `"next_agent": "email_agent"` ONLY if the user EXPLICITLY requests to send, email, mail, or forward the translated content to someone.
- If the user ONLY asks for translation, ALWAYS set `"next_agent": "__end__"`.
- Never assume the user wants to send an email.
- Never choose `email_agent` unless the email request is clearly and explicitly stated.

Allowed values for `next_agent`:
- "email_agent"
- "__end__"

Important:
- Do not hallucinate email actions.
- Translation alone does NOT imply email delivery.
- If multiple languages are requested, still return only ONE `next_agent` value.
- Return clean JSON only.""",
)


async def call_translate_agent(state: MultiAgentState, config: RunnableConfig):
    """Node that calls the translate_agent."""
    session_id = config["configurable"].get("thread_id")

    response = await translate_agent.ainvoke(state, config={"configurable": {"thread_id": session_id}})
    return response
