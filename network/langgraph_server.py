"""
langgraph_server.py - Lab 5: A LangGraph agent exposed over A2A

This wraps a LangGraph research agent (like the one from Lab 1) in an
A2A AgentExecutor and serves it on port 10001. Other agents don't know
or care that LangGraph is inside - they only see the Agent Card.

This file is provided complete - no merge needed.
"""

import asyncio
import os

import uvicorn
from starlette.applications import Starlette

from langchain.agents import create_agent
from langchain.tools import tool

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
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                      temperature=0)


COMPANY_FACTS = {
    "acme corp": "Acme Corp is headquartered in Portland, Oregon and has 1200 employees.",
    "globex": "Globex is headquartered in Berlin, Germany and has 5400 employees. It makes industrial robots.",
    "initech": "Initech is headquartered in Austin, Texas and has 350 employees.",
}


@tool
def lookup_company(name: str) -> str:
    """Look up facts about a company by name."""
    return COMPANY_FACTS.get(name.strip().lower(),
                             f"No information found for {name}.")


research_agent = create_agent(
    get_model(),
    tools=[lookup_company],
    system_prompt=("You are a research specialist. Use the lookup_company "
                   "tool to find facts. Answer briefly with only the facts."),
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

        query = get_message_text(context.message)
        result = await asyncio.to_thread(
            research_agent.invoke,
            {"messages": [{"role": "user", "content": query}]})
        answer = result["messages"][-1].content

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
    description="Looks up facts about companies. Built with LangGraph.",
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:10001"),
    ],
    skills=[
        AgentSkill(
            id="company_research",
            name="Company Research",
            description="Finds facts about companies: location, size, business.",
            tags=["research", "companies", "facts"],
            examples=["Tell me about Globex."],
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
