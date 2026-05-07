# OpenAI Agents SDK vs CrewAI — Comparison

## 1. Framework Origin

| | OpenAI Agents SDK | CrewAI |
|---|---|---|
| Import | `from agents import Agent, Runner` | `from crewai import Agent, Task, Crew` |
| Model binding | Set globally or via `Runner` | Explicit `llm=` per agent |

---

## 2. Agent Definition Style

**OpenAI Agents SDK** — instruction-driven, close to a raw system prompt:
```python
Agent(name="...", instructions="You translate...", output_type=...)
```

**CrewAI** — persona-driven, structured with role/goal/backstory:
```python
Agent(role="Senior Researcher", goal="Find facts", backstory="Expert who...")
```

CrewAI agents feel like job descriptions. SDK agents feel like system prompts.

---

## 3. Task Abstraction

**OpenAI Agents SDK** — no explicit task object; input is a string passed at runtime:
```python
await Runner.run(agent, input="Say hello in Spanish")
```

**CrewAI** — `Task` is a first-class object defined separately from the agent:
```python
Task(description="Research {topic}", expected_output="bullet points", agent=researcher)
```
Tasks can be reused, chained (`context=[task]`), and have enforced outputs independently of the agent.

---

## 4. Orchestration Model

**OpenAI Agents SDK** — **agent-as-tool**: the orchestrator calls sub-agents as function tools:
```python
main_agent = Agent(tools=[email_agent.as_tool(...)])
```
The orchestrator decides when/how to invoke each sub-agent during its own LLM reasoning loop.

**CrewAI** — **process-based**: execution strategy is declared upfront:
- `Process.sequential` — tasks run in order, output flows forward via `context=`
- `Process.hierarchical` — a manager LLM reads all agents/tasks and delegates automatically

---

## 5. Async vs Sync

| | OpenAI Agents SDK | CrewAI |
|---|---|---|
| Execution | Fully async (`await Runner.run()`) | Synchronous by default (`crew.kickoff()`) |
| Concurrency | Natural — multiple agents can run in parallel | Sequential by default, no built-in concurrency |
| Best for | I/O-heavy tasks, concurrent agents | Simpler pipelines, notebooks |

---

## 6. Subclassing vs Tools

**OpenAI Agents SDK** — agents are subclassable Python objects:
```python
class EmailAgent(Agent):
    async def send_mail(self, ...): ...
```

**CrewAI** — agents stay declarative; custom behavior lives in `BaseTool` subclasses:
```python
class EmailDraftTool(BaseTool):
    def _run(self, topic: str) -> str: ...
```

---

## 7. Speed Comparison

For most workloads, LLM API latency dominates — both frameworks are roughly equal. Differences appear at the edges:

| Scenario | Faster |
|---|---|
| Single agent call | Tied |
| Sequential pipeline (A → B → C) | Tied |
| Multiple independent agents at once | OpenAI Agents SDK (async) |
| Hierarchical delegation | OpenAI Agents SDK (one fewer LLM hop) |

**Why CrewAI hierarchical is slower:** the manager LLM first decides who to delegate to, *then* the specialist runs — that is 2 LLM calls where the SDK does 1.

---

## 8. When to Use Which

| Requirement | Use |
|---|---|
| Simple sequential pipeline | Either |
| Concurrent / parallel agents | OpenAI Agents SDK |
| Config-driven, no-code-style setup | CrewAI |
| Sub-agents callable independently AND via orchestrator | **OpenAI Agents SDK** |
| Typed persona-based agents | CrewAI |
| Subclass agents with custom methods | OpenAI Agents SDK |

---

## 9. Use Case: 1 Main Agent + 5 Sub-agents (callable independently)

**Verdict: Use the OpenAI Agents SDK.**

Sub-agents are plain Python objects — the same instance works both standalone and as a tool inside the orchestrator, with no extra setup.

```python
email_agent    = Agent(name="email_agent",    instructions="...")
research_agent = Agent(name="research_agent", instructions="...")
kyc_agent      = Agent(name="kyc_agent",      instructions="...")
summary_agent  = Agent(name="summary_agent",  instructions="...")
data_agent     = Agent(name="data_agent",     instructions="...")

main_agent = Agent(
    name="main_agent",
    instructions="Route tasks to the right specialist...",
    tools=[
        email_agent.as_tool(tool_name="email_sender",       tool_description="..."),
        research_agent.as_tool(tool_name="researcher",      tool_description="..."),
        kyc_agent.as_tool(tool_name="kyc_handler",          tool_description="..."),
        summary_agent.as_tool(tool_name="summariser",       tool_description="..."),
        data_agent.as_tool(tool_name="data_processor",      tool_description="..."),
    ]
)

# Default path — routes through main_agent
result = await Runner.run(main_agent, input="Draft a KYC verification email")

# Independent path — call any sub-agent directly, bypassing main_agent
result = await Runner.run(kyc_agent, input="Draft a KYC verification email")
```

**Why CrewAI is awkward for this:** calling a single agent independently requires wrapping it in a `Crew` every time, since agents are not designed to run standalone:
```python
# Verbose just to call one agent independently in CrewAI
Crew(agents=[kyc_specialist], tasks=[one_off_task]).kickoff()
```

---

## 10. Summary Table

| Feature | OpenAI Agents SDK | CrewAI |
|---|---|---|
| Agent style | Instruction / system-prompt | Role / goal / backstory |
| Task definition | Runtime input string | Explicit `Task` object |
| Orchestration | Agent-as-tool | Process (sequential / hierarchical) |
| Execution | Async | Sync |
| Independent agent calls | Native | Requires wrapping in a Crew |
| Custom agent behavior | Subclass `Agent` | Subclass `BaseTool` |
| Extra LLM hops (hierarchical) | 1 (tool call) | 2 (manager + specialist) |
| Best for | Flexible, production-grade systems | Declarative pipelines |
