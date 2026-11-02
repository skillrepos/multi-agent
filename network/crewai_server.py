"""
crewai_server.py - Lab 5: A CrewAI agent exposed over A2A

This wraps a CrewAI writer (like the one from Lab 2) in an A2A
AgentExecutor and serves it on port 10002. The writer checks the house
style guide for its audience before writing. Same protocol as the
LangGraph server - completely different framework inside.

This file is provided complete - no merge needed.
"""

import asyncio
import os

import uvicorn
from starlette.applications import Starlette

from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool

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
# The CrewAI crew (framework-specific - hidden behind A2A)
# ---------------------------------------------------------------

def get_llm():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        # CrewAI splits this string once: provider="openai", model="openai/gpt-oss-120b".
        # The first "openai/" selects CrewAI's native OpenAI-compatible client (CrewAI has
        # no "groq" provider); the rest is Groq's own model id, which also starts "openai/".
        # The doubled prefix is correct - do not "simplify" it to one.
        return LLM(model="openai/openai/gpt-oss-120b",
                   base_url="https://api.groq.com/openai/v1",
                   api_key=os.environ["GROQ_API_KEY"], temperature=0.3)
    return LLM(model="ollama/" + os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
               base_url="http://localhost:11434", temperature=0.3)


@tool("get_style_guide")
def get_style_guide(audience: str) -> str:
    """House writing rules for an audience: board, investor, or engineering."""
    return data.get_style_guide(audience)


writer = Agent(
    role="Business Writer",
    goal="Write the business document requested, in the house style",
    backstory=("You write clear business documents. Before writing anything, you "
               "check the house style guide for the audience you're writing for."),
    tools=[get_style_guide],
    llm=get_llm(),
    verbose=False,
)

writing_task = Task(
    description=("{request}\n\nFirst get the style guide for the audience "
                 "mentioned above. Then write the document using only the "
                 "facts provided."),
    expected_output="The finished document, following the style guide.",
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
            message=new_text_message("Checking the style guide and writing with CrewAI..."))

        request = get_message_text(context.message)
        try:
            result = await asyncio.to_thread(
                writing_crew.kickoff, inputs={"request": request})
        except Exception as err:
            await updater.update_status(
                state=TaskState.TASK_STATE_FAILED,
                message=new_text_message(f"The writer failed: {err}"))
            return

        await updater.add_artifact(
            parts=[new_text_part(text=str(result), media_type="text/plain")])
        await updater.update_status(state=TaskState.TASK_STATE_COMPLETED)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported by this agent.")


# ---------------------------------------------------------------
# The Agent Card and server
# ---------------------------------------------------------------

card = AgentCard(
    name="Business Writer (CrewAI)",
    description="Writes business documents in the house style. Built with CrewAI.",
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:10002",
                       protocol_version="1.0"),
    ],
    skills=[
        AgentSkill(
            id="business_writing",
            name="Business Writing",
            description=("Writes a board brief, investor note, or engineering "
                         "summary in the house style. Send the audience, what "
                         "to write, and the facts to use."),
            tags=["writing", "briefs", "style"],
            examples=["Audience: board. Write a brief on Globex as a supplier. Facts: ..."],
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
