"""
stats_executor.py - Lab 3: The "brain" of our first A2A agent

An AgentExecutor is where an A2A server does its actual work. The A2A
SDK handles the protocol (JSON-RPC, task storage, streaming); the
executor receives a request and publishes task updates and artifacts
to an event queue. This one computes statistics about the text it is
sent - no LLM needed, so we can focus on the protocol itself.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

from a2a.helpers import (get_message_text, new_task_from_user_message,
                         new_text_message, new_text_part)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState


class TextStatsExecutor(AgentExecutor):
    """Computes statistics about text sent by other agents."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # 1. Get (or create) the task for this request
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue=event_queue,
                              task_id=task.id, context_id=task.context_id)

        # TODO: Lab 3 - report WORKING status, compute the stats,
        # publish the artifact, and mark the task COMPLETED

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported by this agent.")
