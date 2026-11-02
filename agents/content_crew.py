"""
content_crew.py - Lab 2: A role-based crew with CrewAI

Two agents with distinct roles work through a business request:
  - a Company Analyst gathers facts and figures, choosing which tools to use
  - a Business Writer checks the house style guide, then writes the piece
CrewAI runs the two tasks in a fixed order and passes the analyst's output
to the writer. Inside each task, the agent decides its own tool calls.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import os
import sys

from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool

import company_data as data


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


llm = get_llm()

# ---------------------------------------------------------------
# Tools - the agents' access to private business data
# ---------------------------------------------------------------

@tool("lookup_company")
def lookup_company(name: str) -> str:
    """Profile and financials for one company (Acme Corp, Globex, or Initech)."""
    return data.lookup_company(name)


@tool("get_news")
def get_news(company: str) -> str:
    """Recent news headlines for one company (Acme Corp, Globex, or Initech)."""
    return data.get_news(company)


@tool("calculate")
def calculate(expression: str) -> str:
    """Evaluate arithmetic exactly, e.g. '950000000 / 5400' or '(95 / 40) ** (1 / 3) - 1'."""
    return data.calculate(expression)


@tool("get_style_guide")
def get_style_guide(audience: str) -> str:
    """House writing rules for an audience: board, investor, or engineering."""
    return data.get_style_guide(audience)


# ---------------------------------------------------------------
# Agents - defined by role, goal, backstory, and tools
# ---------------------------------------------------------------

# TODO: Lab 2 - define the analyst and writer agents


# ---------------------------------------------------------------
# Tasks - what each agent is asked to produce
# ---------------------------------------------------------------

# TODO: Lab 2 - define the analysis and writing tasks


# ---------------------------------------------------------------
# Crew - the team plus a process type
# ---------------------------------------------------------------

# TODO: Lab 2 - assemble the crew


if __name__ == "__main__":
    example = "Brief our board on Initech as a possible acquisition target."
    if len(sys.argv) > 1:
        request = " ".join(sys.argv[1:])
    else:
        print(f'Type a request, or press Enter for the example: "{example}"')
        request = input("> ").strip() or example
    print(f"\nREQUEST: {request}\n")
    result = crew.kickoff(inputs={"request": request})
    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)
