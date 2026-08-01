"""
content_crew.py - Lab 2: A role-based crew with CrewAI

Two agents with distinct roles - a researcher and a writer - collaborate
on a content pipeline. CrewAI runs the tasks in order and automatically
passes the researcher's output to the writer as context.

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import os
import sys

from crewai import LLM, Agent, Crew, Process, Task


def get_llm():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        return LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)
    return LLM(model="ollama/" + os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
               base_url="http://localhost:11434", temperature=0.3)


llm = get_llm()

# ---------------------------------------------------------------
# Agents - defined by role, goal, and backstory
# ---------------------------------------------------------------

# TODO: Lab 2 - define the researcher and writer agents


# ---------------------------------------------------------------
# Tasks - what each agent is asked to produce
# ---------------------------------------------------------------

# TODO: Lab 2 - define the research and writing tasks


# ---------------------------------------------------------------
# Crew - the team plus a process type
# ---------------------------------------------------------------

# TODO: Lab 2 - assemble the crew


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "GitHub Codespaces"
    print(f"TOPIC: {topic}\n")
    result = crew.kickoff(inputs={"topic": topic})
    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)
