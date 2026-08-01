"""
stats_server.py - Lab 3: Serving an agent over A2A

This publishes our TextStatsExecutor as a real A2A agent:
  - an Agent Card at /.well-known/agent-card.json (discovery)
  - a JSON-RPC 2.0 endpoint at / (communication)

NOTE: This file is incomplete - you'll merge in the working code
during the lab. It won't run until then.
"""

import uvicorn
from starlette.applications import Starlette

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill

from stats_executor import TextStatsExecutor

# ---------------------------------------------------------------
# The Agent Card - how other agents discover what this agent can do
# ---------------------------------------------------------------

# TODO: Lab 3 - define the AgentSkill and AgentCard


# ---------------------------------------------------------------
# The server - SDK request handler + routes on a Starlette app
# ---------------------------------------------------------------

# TODO: Lab 3 - create the request handler, routes, and app


if __name__ == "__main__":
    print("Starting Text Stats Agent on http://127.0.0.1:9999")
    print("Agent Card: http://127.0.0.1:9999/.well-known/agent-card.json")
    uvicorn.run(app, host="127.0.0.1", port=9999)
