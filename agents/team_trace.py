"""
team_trace.py - helper for Lab 1 (you don't need to edit or study this file)

Two conveniences for supervisor_team.py:
  - get_question(): take the question from the command line, or ask for one
  - TeamTracer:     record every tool call made while the team works - including
                    the calls the specialists make *inside* the delegation tools -
                    and print them as a readable "who did what" trace
"""

import sys
import threading

from langchain_core.callbacks import BaseCallbackHandler


def get_question(example):
    """Question from the command line if given; otherwise ask (Enter = example)."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    print("Ask the team a question about Acme Corp, Globex, or Initech.")
    print(f'Press Enter to use the example: "{example}"')
    try:
        typed = input("> ").strip()
    except EOFError:
        typed = ""
    return typed or example


def _one_line(value, limit=160):
    text = getattr(value, "content", value)          # ToolMessage -> its text
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def _args(inputs, input_str):
    if isinstance(inputs, dict) and inputs:
        return ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in inputs.values())
    return input_str


class TeamTracer(BaseCallbackHandler):
    """Collects tool calls from the supervisor AND from inside each specialist.

    LangChain passes this tracer down into every agent the supervisor's tools
    run, so a specialist's own tool calls (lookup_company, calculate) are seen
    too. Each call is filed under the delegation tool it happened inside.
    """

    def __init__(self, delegations):
        # delegations: {"research": "RESEARCHER", "analyze": "ANALYST"}
        self.delegations = delegations
        self.parent = {}          # run id -> parent run id (every step the team takes)
        self.tools = {}           # run id -> {"name", "args", "output"}
        self.order = []           # tool run ids in the order they started
        self.lock = threading.Lock()

    # Remember who started what, so nested calls can be traced back to a delegation
    def _note(self, run_id, parent_run_id):
        with self.lock:
            self.parent[run_id] = parent_run_id

    def on_chain_start(self, serialized, inputs, *, run_id, parent_run_id=None, **kw):
        self._note(run_id, parent_run_id)

    def on_chat_model_start(self, serialized, messages, *, run_id, parent_run_id=None, **kw):
        self._note(run_id, parent_run_id)

    def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id=None, **kw):
        self._note(run_id, parent_run_id)

    def on_tool_start(self, serialized, input_str, *, run_id, parent_run_id=None,
                      inputs=None, **kw):
        name = (serialized or {}).get("name") or kw.get("name") or "tool"
        with self.lock:
            self.parent[run_id] = parent_run_id
            self.tools[run_id] = {"name": name, "args": _args(inputs, input_str), "output": None}
            self.order.append(run_id)

    def on_tool_end(self, output, *, run_id, **kw):
        with self.lock:
            if run_id in self.tools:
                self.tools[run_id]["output"] = output

    def _delegation_above(self, run_id):
        """The delegation tool run this call happened inside, if any."""
        seen = set()
        node = self.parent.get(run_id)
        while node is not None and node not in seen:
            seen.add(node)
            if node in self.tools and self.tools[node]["name"] in self.delegations:
                return node
            node = self.parent.get(node)
        return None

    def print_trace(self, question):
        line = "=" * 60
        print(line)
        print("MESSAGE TRACE (who did what):")
        print(line)
        print(f"USER asks the SUPERVISOR: {_one_line(question)}\n")

        supervisor_tools, specialist_tools = [], []
        for rid in self.order:
            call = self.tools[rid]
            if self._delegation_above(rid) is not None:
                continue                                  # printed under its delegation
            supervisor_tools.append(call["name"])
            who = self.delegations.get(call["name"])
            if who is None:
                print(f"SUPERVISOR uses {call['name']}({call['args']})")
                print(f"    -> {_one_line(call['output'])}\n")
                continue

            print(f"SUPERVISOR delegates to the {who} (through the '{call['name']}' tool): {call['args']}")
            inner = [r for r in self.order if self._delegation_above(r) == rid]
            if not inner:
                print(f"    {who} answered WITHOUT using any of its tools")
            for r in inner:
                sub = self.tools[r]
                specialist_tools.append(sub["name"])
                print(f"    {who} uses {sub['name']}({sub['args']})")
                print(f"        -> {_one_line(sub['output'])}")
            print(f"    {who} reports back: {_one_line(call['output'])}\n")

        print("SUPERVISOR combines the reports into one final answer.")
        print(line)
        unique = lambda names: ", ".join(dict.fromkeys(names)) or "(none)"
        print(f"Tools the SUPERVISOR called itself:  {unique(supervisor_tools)}")
        print(f"Tools only the specialists called:  {unique(specialist_tools)}")
        print(line)
