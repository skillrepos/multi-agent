"""
analyst_agent.py - Labs 3 and 4: the Company Analyst agent (provided - nothing to merge)

A LangGraph agent like the ones you built in Lab 1. Given a question, it
decides which tools to call - company profiles, news, a calculator - how
many times, and in what order, then writes the answer.

In Lab 3 you'll serve this agent over A2A. Nothing in this file knows
anything about A2A.
"""

import os

from langchain.agents import create_agent
from langchain.tools import tool

import company_data as data


def get_model():
    """Use Groq if GROQ_API_KEY is set; otherwise use local Ollama."""
    if os.environ.get("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                      temperature=0)


@tool
def lookup_company(name: str) -> str:
    """Profile and financials for one company (Acme Corp, Globex, or Initech)."""
    return data.lookup_company(name)


@tool
def get_news(company: str) -> str:
    """Recent news headlines for one company (Acme Corp, Globex, or Initech)."""
    return data.get_news(company)


@tool
def calculate(expression: str) -> str:
    """Evaluate arithmetic exactly, e.g. '950000000 / 5400' or '(95 / 40) ** (1 / 3) - 1'."""
    return data.calculate(expression)


analyst_agent = create_agent(
    get_model(),
    tools=[lookup_company, get_news, calculate],
    system_prompt=(
        "You are a company analyst. Use lookup_company for profiles and "
        "financials, get_news for recent events, and calculate for ALL math - "
        "never do arithmetic yourself. Use only facts your tools return. "
        "Answer in 2-4 sentences with the key numbers."
    ),
)
