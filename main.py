import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.langchain_route import router as langchain_router
from routes.openai_route import router as openai_router

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

app.include_router(langchain_router)
app.include_router(openai_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
