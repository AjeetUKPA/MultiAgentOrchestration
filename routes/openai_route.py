from fastapi import APIRouter
from schemas.route_schema.main_route import RunRequest, AgentSelector

from openai_agent import (
    email_agent,
    orchestrator,
    summarizer_agent,
    translator_agent
)

router = APIRouter(prefix="/openai_agent", tags=["OpenAI Agents"])


@router.post(
    "",
    summary="Run an agent",
    description=(
        "Submit a natural-language request to one of the available agents.\n\n"
        "- Leave `agent` as `all` to let the **orchestrator** decide which "
        "specialised agent handles the task.\n"
        "- Set `agent` to a specific value(\n **email_agent** \n , **summarizer_agent**\n  ,**translator_agent** \n) to **bypass the orchestrator** and "
        "call that agent directly.\n\n"
        "The response always includes an `agent` key indicating which agent ran "
        "and a `result` key containing its structured output."
    ),
    response_description="JSON object with `agent` (which agent ran) and `result` (agent output).",
    responses={
        200: {
            "description": "Successful agent response",
            "content": {
                "application/json": {
                    "examples": {
                        "orchestrator": {
                            "summary": "Orchestrator response",
                            "value": {
                                "agent": "orchestrator",
                                "result": {
                                    "agent_invoked": "SummarizerAgent",
                                    "result": {
                                        "summary": "AI is reshaping industries.",
                                        "key_points": ["Automation", "Personalisation"],
                                    },
                                },
                            },
                        },
                        "summarizer_direct": {
                            "summary": "Direct SummarizerAgent response",
                            "value": {
                                "agent": "summarizer_agent",
                                "result": {
                                    "summary": "AI is reshaping industries.",
                                    "key_points": ["Automation", "Personalisation"],
                                },
                            },
                        },
                    }
                }
            },
        }
    },
)
async def run_orchestrator(request: RunRequest):
    if request.agent == AgentSelector.all:
        result = await orchestrator.run_agent(request.user_input)
        return {"agent": "orchestrator", "result": result.final_output}

    if request.agent == AgentSelector.email_agent:
        result = await email_agent.run_agent(receiver_email=None, user_input=request.user_input)
        return {"agent": "email_agent", "result": result.model_dump()}

    if request.agent == AgentSelector.summarizer_agent:
        result = await summarizer_agent.run_agent(request.user_input)
        return {"agent": "summarizer_agent", "result": result.model_dump()}

    if request.agent == AgentSelector.translator_agent:
        result = await translator_agent.run_agent(request.user_input)
        return {"agent": "translator_agent", "result": result.model_dump()}
