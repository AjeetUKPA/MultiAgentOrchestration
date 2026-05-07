from typing import Optional
from fastapi import APIRouter

from pydantic import BaseModel

from langchain_agent.schemas.route_schema.main_route_schema.main_route_schema import RunRequest, AgentSelector
from langchain_agent.graph import graph
from langchain_agent.custom_agents.summarizer_agent import summarise_agent
from langchain_agent.custom_agents.translator_agent import translate_agent
from langchain_agent.custom_agents.email_agent import email_agent

router = APIRouter(prefix="/langchain_agent", tags=["LangChain Agents"])


class ResumeRequest(BaseModel):
    session_id: str = "default"
    decision: str                       # "y" | "n" | "e"
    receiver_email: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None


def _extract_result(result):
    """Pull the last message content out of a graph result regardless of v2 wrapping."""
    try:
        return result.value["messages"][-1].content
    except (AttributeError, KeyError, IndexError, TypeError):
        pass
    try:
        return result["messages"][-1].content
    except (KeyError, IndexError, TypeError):
        pass
    return str(result)


def _extract_interrupt(result):
    """Return interrupt objects from a graph result, or an empty list."""
    try:
        return result.value.get("interrupts", [])
    except AttributeError:
        pass
    try:
        return result.get("interrupts", [])
    except AttributeError:
        return []


@router.post(
    "",
    summary="Run a LangChain agent",
    description=(
        "Submit a natural-language request to one of the LangChain-powered agents.\n\n"
        "- Leave `agent` as `all` to let the **orchestrator** decide which "
        "specialised agent handles the task.\n"
        "- Set `agent` to a specific value (`email_agent`, `summarizer_agent`, "
        "`translator_agent`) to **bypass the orchestrator** and call that agent directly.\n\n"
        "The response includes `interrupt: true` when an email approval is required."
    ),
)
async def run_langchain_agent(request: RunRequest):
    messages = [{"role": "user", "content": request.user_input}]

    # ── Direct agent calls ────────────────────────────────────────────────
    if request.agent == AgentSelector.summarizer_agent:
        result = await summarise_agent.ainvoke({"messages": messages})
        response = result["messages"][-1].content
        return {"messages": response, "interrupt": False}

    if request.agent == AgentSelector.translator_agent:
        result = await translate_agent.ainvoke({"messages": messages})
        response = result["messages"][-1].content
        return {"messages": response, "interrupt": False}

    if request.agent == AgentSelector.email_agent:
        result = await email_agent.ainvoke({"messages": messages})
        response = result["messages"][-1].content
        return {"messages": response, "interrupt": False}

    # ── Orchestrator (agent == "all") ─────────────────────────────────────
    result = await graph.run({"messages": messages}, session_id=request.session_id)

    response   = _extract_result(result)
    interrupts = _extract_interrupt(result)

    description     = None
    receiver_email  = None
    subject         = None
    body            = None
    allowed_decisions = []
    interrupt       = False

    if interrupts:
        interrupt       = True
        first_interrupt = interrupts[0]

        try:
            action_request    = first_interrupt.value["action_requests"][0]
            review_config     = first_interrupt.value["review_configs"][0]
            args              = action_request["args"]
            receiver_email    = args.get("receiver_email")
            subject           = args.get("subject")
            body              = args.get("body")
            description       = action_request.get("description")
            allowed_decisions = review_config.get("allowed_decisions", [])
        except (AttributeError, KeyError, IndexError, TypeError):
            # interrupt_before without HumanInTheLoopMiddleware — surface what we have
            pass

    return {
        "messages":          response,
        "interrupt":         interrupt,
        "description":       description,
        "allowed_decisions": allowed_decisions,
        "receiver_email":    receiver_email,
        "subject":           subject,
        "body":              body,
    }


@router.post(
    "/resume",
    summary="Resume after an email interrupt",
    description=(
        "Resume a session that is paused at the email-approval interrupt.\n\n"
        "- `decision: 'y'` — approve and send the email as drafted.\n"
        "- `decision: 'n'` — reject; the email will not be sent.\n"
        "- `decision: 'e'` — approve with edited fields "
        "(`receiver_email`, `subject`, `body` are updated before sending)."
    ),
)
async def resume_langchain_agent(request: ResumeRequest):
    if request.decision == "n":
        return {"messages": "Email sending was cancelled by the user.", "interrupt": False}

    result = await graph.resume(
        decision=request.decision,
        session_id=request.session_id,
        receiver_email=request.receiver_email,
        subject=request.subject,
        body=request.body,
    )

    response = _extract_result(result)
    return {"messages": response, "interrupt": False}
