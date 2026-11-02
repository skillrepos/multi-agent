"""
analyst_client.py - Lab 4: Speaking A2A from the client side

This client:
  1. discovers the remote agent by fetching its Agent Card
  2. opens a connection using the card's preferred interface
  3. sends a question and streams back the task's progress as it happens
  4. fetches the finished task by id afterward

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import asyncio
import sys

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import (get_message_text, get_stream_response_text,
                         new_text_message)
from a2a.types import GetTaskRequest, Role, SendMessageRequest

AGENT_URL = "http://127.0.0.1:9999"
EXAMPLE = "How much revenue per employee does Initech bring in, and what's its latest news?"


async def main(question: str) -> None:
    async with httpx.AsyncClient(timeout=300.0) as httpx_client:

        # 1. Discovery: fetch the Agent Card from the well-known URL
        # TODO: Lab 4 - resolve the Agent Card and print its skills

        # 2. Create a client for this agent (transport chosen from the card)
        # TODO: Lab 4 - create the A2A client

        # 3. Send the question and stream the task's progress events
        # TODO: Lab 4 - send the question and print the streamed events

        # 4. Retrieve the finished task by id
        # TODO: Lab 4 - fetch the task with get_task and print a summary

        await client.close()


def TaskStateName(state) -> str:
    """Turn the numeric TaskState enum into a readable name."""
    from a2a.types import TaskState
    return TaskState.Name(state).replace("TASK_STATE_", "")


def get_question() -> str:
    """Question from the command line, or ask for one (Enter = example)."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    print(f'Type a question, or press Enter for the example: "{EXAMPLE}"')
    return input("> ").strip() or EXAMPLE


if __name__ == "__main__":
    asyncio.run(main(get_question()))
