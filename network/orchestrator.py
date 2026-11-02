"""
orchestrator.py - Lab 5: An AI orchestrator for a cross-framework agent network

The orchestrator knows NOTHING about LangGraph or CrewAI. It:
  1. discovers the available agents by fetching their Agent Cards
  2. turns each card's skills into tools an AI model can choose from
  3. lets the model decide which agents to call, in what order, and with
     what instructions - then delegates each call over A2A

It talks to the model with plain HTTP (llm.py), so it uses no agent
framework at all: any framework behind the cards, one way to talk to them.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import asyncio
import json
import sys

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import get_stream_response_text, new_text_message
from a2a.types import Role, SendMessageRequest

from llm import chat

# The agents in our network - in production this could come from a registry
AGENT_URLS = [
    "http://127.0.0.1:10001",
    "http://127.0.0.1:10002",
]

EXAMPLE = ("Write a short brief for our board on Globex as a possible robotics "
           "supplier, including any recent news they should know about.")

INSTRUCTIONS = (
    "You coordinate a team of remote agents, which you can call as tools. "
    "Plan the steps, call the agents in a sensible order, and give each one "
    "everything it needs - including results from earlier agents. When the "
    "requested document is finished, reply with it in full.")


async def discover_agents(httpx_client):
    """Step 1: fetch every agent's card from its well-known URL."""
    # TODO: Lab 5 - fetch and return the Agent Cards


def cards_to_tools(cards):
    """Step 2: describe each agent's skills as tools the model can choose from."""
    # TODO: Lab 5 - build a tool for every skill, and remember which card owns it


async def delegate(httpx_client, card, text):
    """Step 3: send a task to an agent over A2A and collect its artifact."""
    # TODO: Lab 5 - create a client, send the message, collect artifacts


async def main(request: str) -> None:
    async with httpx.AsyncClient(timeout=300.0) as httpx_client:

        print("Discovering agents...")
        cards = await discover_agents(httpx_client)
        tools, owners = cards_to_tools(cards)
        for card in cards:
            print(f"  found: {card.name}  skills={[s.id for s in card.skills]}")
        print(f"\nREQUEST: {request}\n")

        # The model plans; every tool call it makes becomes an A2A delegation
        messages = [{"role": "system", "content": INSTRUCTIONS},
                    {"role": "user", "content": request}]
        for _ in range(8):
            reply = await chat(httpx_client, messages, tools)
            messages.append(reply)
            calls = reply.get("tool_calls") or []
            if not calls:
                print("=" * 60)
                print("FINAL RESULT (planned by the orchestrator's model):")
                print("=" * 60)
                print(reply.get("content") or "")
                return
            for call in calls:
                name = call["function"]["name"]
                args = call["function"].get("arguments") or "{}"
                ask = (json.loads(args) if isinstance(args, str) else args).get("request", "")
                card = owners.get(name)
                if card is None:
                    result = f"There is no agent with a skill named {name}."
                else:
                    print(f"ORCHESTRATOR -> {card.name}:\n  {ask}")
                    result = await delegate(httpx_client, card, ask)
                    print(f"  <- {result[:300]}\n")
                messages.append({"role": "tool", "tool_call_id": call["id"],
                                 "content": result})
        print("Stopped after 8 rounds without a final answer.")


def get_request() -> str:
    """Request from the command line, or ask for one (Enter = example)."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    print(f'Type a request, or press Enter for the example: "{EXAMPLE}"')
    return input("> ").strip() or EXAMPLE


if __name__ == "__main__":
    asyncio.run(main(get_request()))
