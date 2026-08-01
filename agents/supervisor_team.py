"""
supervisor_team.py - Lab 1: A multi-agent team with a supervisor

A supervisor agent coordinates two specialist agents:
  - a researcher that can look up company facts
  - an analyst that can do arithmetic
Each specialist is a full agent with its own tools, wrapped as a tool
the supervisor can call. This is the "supervisor" (subagents) pattern.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import os

from langchain.agents import create_agent
from langchain.tools import tool


def get_model():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                      temperature=0)


model = get_model()

# ---------------------------------------------------------------
# Low-level tools - the specialists' actual capabilities
# ---------------------------------------------------------------

COMPANY_FACTS = {
    "acme corp": "Acme Corp is headquartered in Portland, Oregon and has 1200 employees.",
    "globex": "Globex is headquartered in Berlin, Germany and has 5400 employees.",
    "initech": "Initech is headquartered in Austin, Texas and has 350 employees.",
}


@tool
def lookup_company(name: str) -> str:
    """Look up facts about a company by name."""
    return COMPANY_FACTS.get(name.strip().lower(),
                             f"No information found for {name}.")


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression like '1200 * 3'."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Only basic arithmetic is supported."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Could not evaluate: {e}"


# ---------------------------------------------------------------
# Specialist agents - each is a complete agent with its own tools
# ---------------------------------------------------------------

# TODO: Lab 1 - create the researcher and analyst specialist agents


# ---------------------------------------------------------------
# Delegation tools - each wraps a specialist agent as a tool
# ---------------------------------------------------------------

# TODO: Lab 1 - create the research and analyze delegation tools


# ---------------------------------------------------------------
# Supervisor - coordinates the team by calling delegation tools
# ---------------------------------------------------------------

# TODO: Lab 1 - create the supervisor agent


if __name__ == "__main__":
    question = ("Where is Acme Corp headquartered, and how many employees "
                "would it have if it tripled in size?")
    print(f"QUESTION: {question}\n")
    print("The supervisor is delegating to its team (this can take a minute "
          "or two with a local model)...\n")

    result = supervisor.invoke({"messages": [{"role": "user", "content": question}]})

    print("=" * 60)
    print("MESSAGE TRACE (who did what):")
    print("=" * 60)
    for msg in result["messages"]:
        who = type(msg).__name__.replace("Message", "").upper()
        calls = getattr(msg, "tool_calls", None)
        if calls:
            for c in calls:
                print(f"[{who}] -> called tool '{c['name']}' with {c['args']}")
        elif msg.content:
            text = msg.content if isinstance(msg.content, str) else str(msg.content)
            print(f"[{who}] {text[:200]}")
    print("=" * 60)
    print("\nFINAL ANSWER:\n" + result["messages"][-1].content)
