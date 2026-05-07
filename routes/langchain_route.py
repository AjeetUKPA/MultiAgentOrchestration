from fastapi import APIRouter

from langchain_agent.schemas.route_schema.main_route import RunRequest, AgentSelector
from langchain_agent.graph import graph
from langchain_agent.custom_agents.summarizer_agent import summarise_agent
from langchain_agent.custom_agents.translator_agent import translate_agent
from langchain_agent.custom_agents.email_agent import email_agent

router = APIRouter(prefix="/langchain_agent", tags=["LangChain Agents"])


@router.post(
    "",
    summary="Run a LangChain agent",
    description=(
        "Submit a natural-language request to one of the LangChain-powered agents.\n\n"
        "- Leave `agent` as `all` to let the **orchestrator** decide which "
        "specialised agent handles the task.\n"
        "- Set `agent` to a specific value(\n **email_agent** \n , **summarizer_agent**\n  ,**translator_agent** \n) "
        "to **bypass the orchestrator** and call that agent directly.\n\n"
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
                                "result": "The text has been summarised: AI is reshaping industries.",
                            },
                        },
                        "summarizer_direct": {
                            "summary": "Direct SummarizerAgent response",
                            "value": {
                                "agent": "summarizer_agent",
                                "result": "AI is reshaping industries. Key points: Automation, Personalisation.",
                            },
                        },
                    }
                }
            },
        }
    },
)
async def run_langchain_agent(request: RunRequest):
    messages = [{"role": "user", "content": request.user_input}]

    if request.agent == AgentSelector.all:
        result = await graph.run({"messages": messages}, session_id=request.session_id)
        import json
        response = result.value["messages"][-1].content

        interrupts = result.value.get("interrupts", [])

        description = None
        receiver_email = None
        subject = None
        body = None
        allowed_decisions = []
        interrupt = False

        if interrupts:
            interrupt = True

            first_interrupt = interrupts[0]

            action_request = first_interrupt.value["action_requests"][0]
            review_config = first_interrupt.value["review_configs"][0]

            args = action_request["args"]

            receiver_email = args.get("receiver_email")
            subject = args.get("subject")
            body = args.get("body")

            description = action_request.get("description")

            allowed_decisions = review_config.get("allowed_decisions", [])

        return {
            "messages": response,
            "interrupt": interrupt,
            "description": description,
            "allowed_decisions": allowed_decisions,
            "receiver_email": receiver_email,
            "subject": subject,
            "body": body,
        }
