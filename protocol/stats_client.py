"""
stats_client.py - Lab 4: Speaking A2A from the client side

This client:
  1. discovers the remote agent by fetching its Agent Card
  2. opens a connection using the card's preferred interface
  3. sends a message and streams back the task lifecycle events
  4. fetches the finished task by id afterward

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import asyncio

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import get_stream_response_text, new_text_message
from a2a.types import GetTaskRequest, Role, SendMessageRequest

AGENT_URL = "http://127.0.0.1:9999"


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:

        # 1. Discovery: fetch the Agent Card from the well-known URL
        # TODO: Lab 4 - resolve the Agent Card and print its skills

        # 2. Create a client for this agent (transport chosen from the card)
        # TODO: Lab 4 - create the A2A client

        # 3. Send a message and stream the task lifecycle events
        # TODO: Lab 4 - send a message and print the streamed events

        # 4. Retrieve the finished task by id
        # TODO: Lab 4 - fetch the task with get_task and print a summary

        await client.close()


def TaskStateName(state) -> str:
    """Turn the numeric TaskState enum into a readable name."""
    from a2a.types import TaskState
    return TaskState.Name(state).replace("TASK_STATE_", "")


if __name__ == "__main__":
    asyncio.run(main())
