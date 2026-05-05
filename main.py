import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from openai_agent.schemas.route_schema.main_route import RunRequest, AgentSelector

from openai_agent import (
    email_agent,
    orchestrator,
    summarizer_agent, 
    translator_agent
)

load_dotenv()

app = FastAPI(
    title="Multi-Agent Orchestration API",
    description=(
        "A FastAPI service that routes natural-language requests to specialised AI agents.\n\n"
        "**Available agents**\n"
        "- `all` — Orchestrator automatically picks the right agent.\n"
        "- `email_agent` — Drafts an email based on your instructions.\n"
        "- `summarizer_agent` — Summarises text and extracts key points.\n"
        "- `translator_agent` — Translates text into a target language.\n\n"
        "Set the `agent` field in the request body to target a specific agent, "
        "or leave it as `all` to let the orchestrator decide."
    )
)

@app.post(
    "/openai_agent",
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
