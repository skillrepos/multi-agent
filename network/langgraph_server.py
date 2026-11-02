"""
langgraph_server.py - Lab 5: A LangGraph agent exposed over A2A

This wraps a LangGraph research agent (like the researcher from Lab 1) in
an A2A AgentExecutor and serves it on port 10001. The agent decides which
of its tools to use - company profiles, news, or both. Other agents don't know
or care that LangGraph is inside - they only see the Agent Card.

This file is provided complete - no merge needed.
"""

import os

import uvicorn
from starlette.applications import Starlette

from langchain.agents import create_agent
from langchain.tools import tool

import company_data as data

from a2a.helpers import (get_message_text, new_task_from_user_message,
                         new_text_message, new_text_part)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (AgentCapabilities, AgentCard, AgentInterface,
                       AgentSkill, TaskState)


# ---------------------------------------------------------------
# The LangGraph agent (framework-specific - hidden behind A2A)
# ---------------------------------------------------------------

def get_model():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                      temperature=0)


@tool
def lookup_company(name: str) -> str:
    """Profile and financials for one company (Acme Corp, Globex, or Initech)."""
    return data.lookup_company(name)


@tool
def get_news(company: str) -> str:
    """Recent news headlines for one company (Acme Corp, Globex, or Initech)."""
    return data.get_news(company)


research_agent = create_agent(
    get_model(),
    tools=[lookup_company, get_news],
    system_prompt=("You are a company researcher. Use lookup_company for profiles "
                   "and financials and get_news for recent events - whichever the "
                   "request needs. Report what you found as short bullet points "
                   "with numbers. Use only facts your tools return."),
)


# ---------------------------------------------------------------
# The A2A executor - bridges the protocol to the LangGraph agent
# ---------------------------------------------------------------

class LangGraphResearchExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue=event_queue,
                              task_id=task.id, context_id=task.context_id)
        await updater.update_status(
            state=TaskState.TASK_STATE_WORKING,
            message=new_text_message("Researching with LangGraph..."))

        # Run the agent step by step, reporting each tool it decides to call
        query = get_message_text(context.message)
        answer = ""
        try:
            async for step in research_agent.astream(
                    {"messages": [{"role": "user", "content": query}]},
                    stream_mode="updates"):
                for node, update in step.items():
                    for msg in (update or {}).get("messages", []):
                        for call in getattr(msg, "tool_calls", None) or []:
                            args = ", ".join(str(v) for v in call["args"].values())
                            await updater.update_status(
                                state=TaskState.TASK_STATE_WORKING,
                                message=new_text_message(f"Calling {call['name']}({args})"))
                        if node == "model" and msg.content and not msg.tool_calls:
                            answer = msg.content
        except Exception as err:
            await updater.update_status(
                state=TaskState.TASK_STATE_FAILED,
                message=new_text_message(f"The agent failed: {err}"))
            return

        await updater.add_artifact(
            parts=[new_text_part(text=answer, media_type="text/plain")])
        await updater.update_status(state=TaskState.TASK_STATE_COMPLETED)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported by this agent.")


# ---------------------------------------------------------------
# The Agent Card and server
# ---------------------------------------------------------------

card = AgentCard(
    name="Company Research Agent (LangGraph)",
    description="Researches companies - profile, financials, and recent news. Built with LangGraph.",
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:10001",
                       protocol_version="1.0"),
    ],
    skills=[
        AgentSkill(
            id="company_research",
            name="Company Research",
            description=("Researches Acme Corp, Globex, or Initech: profile, "
                         "financials, and recent news. Say which company and "
                         "what you need to know."),
            tags=["research", "companies", "news"],
            examples=["Get Globex's profile, financials, and recent news."],
            input_modes=["text/plain"],
            output_modes=["text/plain"],
        ),
    ],
)

handler = DefaultRequestHandler(
    agent_executor=LangGraphResearchExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=card,
)

routes = []
routes.extend(create_agent_card_routes(card))
routes.extend(create_jsonrpc_routes(handler, "/"))
app = Starlette(routes=routes)


if __name__ == "__main__":
    print("LangGraph research agent (A2A) on http://127.0.0.1:10001")
    uvicorn.run(app, host="127.0.0.1", port=10001, log_level="warning")
