"""
analyst_executor.py - Lab 3: The bridge between A2A and our agent

An AgentExecutor is where an A2A server does its actual work. The A2A
SDK handles the protocol (JSON-RPC, task storage, streaming); the
executor receives a request, runs the agent, and publishes what happens
as task updates: a progress message for every step the agent takes, the
answer as an artifact, and a final state.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

from a2a.helpers import (get_message_text, new_task_from_user_message,
                         new_text_message, new_text_part)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState

from analyst_agent import analyst_agent


def describe(call) -> str:
    """Turn a tool call into a short progress message, e.g. 'get_news(Globex)'."""
    args = ", ".join(str(v) for v in call["args"].values())
    return f"Calling {call['name']}({args})"


class AnalystExecutor(AgentExecutor):
    """Runs the Company Analyst agent and reports each step over A2A."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # 1. Get (or create) the task for this request
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue=event_queue,
                              task_id=task.id, context_id=task.context_id)

        # TODO: Lab 3 - report WORKING, run the agent step by step (a progress
        # update for every tool call, FAILED if it errors), then publish the
        # answer as an artifact and mark the task COMPLETED

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported by this agent.")
