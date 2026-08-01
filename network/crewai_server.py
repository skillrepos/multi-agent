"""
crewai_server.py - Lab 5: A CrewAI agent exposed over A2A

This wraps a CrewAI writing crew in an A2A AgentExecutor and serves
it on port 10002. Same protocol as the LangGraph server - completely
different framework inside.

This file is provided complete - no merge needed.
"""

import asyncio
import os

import uvicorn
from starlette.applications import Starlette

from crewai import LLM, Agent, Crew, Process, Task

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
# The CrewAI crew (framework-specific - hidden behind A2A)
# ---------------------------------------------------------------

def get_llm():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        return LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)
    return LLM(model="ollama/" + os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
               base_url="http://localhost:11434", temperature=0.3)


writer = Agent(
    role="Executive Brief Writer",
    goal="Turn raw notes into a crisp two-sentence executive brief",
    backstory=("You write for busy executives. Every word earns its place. "
               "You never exceed two sentences."),
    llm=get_llm(),
    verbose=False,
)

writing_task = Task(
    description=("Write a two-sentence executive brief based on these "
                 "notes:\n{notes}"),
    expected_output="Exactly two sentences.",
    agent=writer,
)

writing_crew = Crew(
    agents=[writer],
    tasks=[writing_task],
    process=Process.sequential,
    verbose=False,
)


# ---------------------------------------------------------------
# The A2A executor - bridges the protocol to the crew
# ---------------------------------------------------------------

class CrewAIWriterExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue=event_queue,
                              task_id=task.id, context_id=task.context_id)
        await updater.update_status(
            state=TaskState.TASK_STATE_WORKING,
            message=new_text_message("Writing with CrewAI..."))

        notes = get_message_text(context.message)
        result = await asyncio.to_thread(
            writing_crew.kickoff, inputs={"notes": notes})

        await updater.add_artifact(
            parts=[new_text_part(text=str(result), media_type="text/plain")])
        await updater.update_status(state=TaskState.TASK_STATE_COMPLETED)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported by this agent.")


# ---------------------------------------------------------------
# The Agent Card and server
# ---------------------------------------------------------------

card = AgentCard(
    name="Executive Brief Writer (CrewAI)",
    description="Writes short executive briefs from notes. Built with CrewAI.",
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:10002"),
    ],
    skills=[
        AgentSkill(
            id="exec_brief",
            name="Executive Brief Writing",
            description="Turns notes or facts into a two-sentence executive brief.",
            tags=["writing", "summarize", "briefs"],
            examples=["Write a brief from these notes: ..."],
            input_modes=["text/plain"],
            output_modes=["text/plain"],
        ),
    ],
)

handler = DefaultRequestHandler(
    agent_executor=CrewAIWriterExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=card,
)

routes = []
routes.extend(create_agent_card_routes(card))
routes.extend(create_jsonrpc_routes(handler, "/"))
app = Starlette(routes=routes)


if __name__ == "__main__":
    print("CrewAI writer agent (A2A) on http://127.0.0.1:10002")
    uvicorn.run(app, host="127.0.0.1", port=10002, log_level="warning")
