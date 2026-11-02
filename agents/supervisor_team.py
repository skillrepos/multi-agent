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
        return ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                      temperature=0)


model = get_model()

# ---------------------------------------------------------------
# Low-level tools - the specialists' actual capabilities
# ---------------------------------------------------------------

# A small private knowledge base - facts the model can't know on its own
COMPANY_FACTS = {
    "acme corp": ("Acme Corp is headquartered in Portland, Oregon and makes outdoor "
                  "camping gear. It has 1200 employees. Revenue: $120 million in 2022, "
                  "$180 million in 2025."),
    "globex": ("Globex is headquartered in Berlin, Germany and makes industrial "
               "robots. It has 5400 employees. Revenue: $820 million in 2022, "
               "$950 million in 2025."),
    "initech": ("Initech is headquartered in Austin, Texas and makes payroll "
                "software. It has 350 employees. Revenue: $40 million in 2022, "
                "$95 million in 2025."),
}


@tool
def lookup_company(name: str) -> str:
    """Look up facts about a company by name."""
    return COMPANY_FACTS.get(name.strip().lower(),
                             f"No information found for {name}.")


@tool
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression exactly, e.g. '180000000 / 1200' or a
    yearly growth rate like '(180 / 120) ** (1 / 3) - 1'."""
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
    # The question comes from the command line, or you're asked for one.
    # (team_trace.py is a small helper - it prints the "who did what" trace.)
    from team_trace import TeamTracer, get_question

    question = get_question("Compare Acme Corp and Globex: which one brings in "
                            "more revenue per employee, and by how much?")
    print(f"\nQUESTION: {question}\n")
    print("The supervisor is delegating to its team (a few seconds with Groq, "
          "a minute or two with the local model)...\n")

    tracer = TeamTracer({"research": "RESEARCHER", "analyze": "ANALYST"})
    result = supervisor.invoke({"messages": [{"role": "user", "content": question}]},
                               config={"callbacks": [tracer]})

    tracer.print_trace(question)
    print("\nFINAL ANSWER:\n" + result["messages"][-1].content)
