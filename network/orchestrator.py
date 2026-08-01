"""
orchestrator.py - Lab 5: A cross-framework agent network

The orchestrator knows NOTHING about LangGraph or CrewAI. It:
  1. discovers the available agents by fetching their Agent Cards
  2. picks agents for each step by matching skill tags
  3. delegates work over A2A and chains the results together

This is the payoff of a protocol: any framework behind the card,
one way to talk to all of them.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import asyncio

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import get_stream_response_text, new_text_message
from a2a.types import Role, SendMessageRequest

# The agents in our network - in production this could come from a registry
AGENT_URLS = [
    "http://127.0.0.1:10001",
    "http://127.0.0.1:10002",
]


async def discover_agents(httpx_client):
    """Step 1: fetch every agent's card from its well-known URL."""
    # TODO: Lab 5 - fetch and return the Agent Cards


def find_agent_with_tag(cards, tag):
    """Step 2: capability matching - find an agent whose skills carry a tag."""
    # TODO: Lab 5 - return the first card with a matching skill tag


async def delegate(httpx_client, card, text):
    """Step 3: send a task to an agent over A2A and collect its artifact."""
    # TODO: Lab 5 - create a client, send the message, collect artifacts


async def main() -> None:
    async with httpx.AsyncClient(timeout=300.0) as httpx_client:

        print("Discovering agents...")
        cards = await discover_agents(httpx_client)
        for card in cards:
            tags = sorted({t for s in card.skills for t in s.tags})
            print(f"  found: {card.name}  tags={tags}")
        print()

        researcher = find_agent_with_tag(cards, "research")
        writer = find_agent_with_tag(cards, "writing")

        print(f"Delegating research to: {researcher.name}")
        facts = await delegate(httpx_client, researcher,
                               "Tell me about the company Globex.")
        print(f"  facts: {facts}\n")

        print(f"Delegating writing to:  {writer.name}")
        brief = await delegate(httpx_client, writer,
                               f"Write a brief from these notes: {facts}")

        print("\n" + "=" * 60)
        print("EXECUTIVE BRIEF (research by LangGraph, writing by CrewAI):")
        print("=" * 60)
        print(brief)


if __name__ == "__main__":
    asyncio.run(main())
