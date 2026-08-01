# Multi-Agent AI Systems & the A2A Protocol

**Hands-on workshop — Revision 1.2 — 08/01/26**

This repository contains the labs, code, and setup for the *Multi-Agent AI Systems & the A2A Protocol*
workshop. In it, you'll build multi-agent systems with LangGraph and CrewAI, learn Google's A2A
(Agent2Agent) protocol v1.0, and connect agents built in different frameworks into a single
cross-framework agent network.

**Prerequisite**: Experience building single AI agents (via the AI Accelerator, ai-aip workshop, or
equivalent). Comfort with Python and LLM APIs.

---

## Setup — GitHub Codespaces (recommended)

1. Click the button below, or use the green **Code** button → **Codespaces** tab → **Create codespace on main**.

   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/multi-agent)

2. **Wait for setup to finish.** The codespace installs Python dependencies, installs Ollama, and pulls
   the `llama3.2:3b` model. This takes **3-5 minutes** after the codespace opens. When the terminal
   shows `Ollama is ready with model llama3.2:3b`, you're good to go.

3. **Set up a free Groq API key** (recommended — see below).

4. Open `labs.md` and start with **Lab 1**.

### System requirements (Codespace machine type)

- 4 cores / 16 GB RAM / 32 GB storage (the default machine type configured for this repo)

## Recommended: a free Groq API key

Every lab runs two ways, and the lab steps are identical either way:

| | Setup | Speed | Answer quality |
|---|---|---|---|
| **Groq** (recommended) | free API key | **seconds** | reliable |
| **Local Ollama** (fallback) | nothing — works out of the box | 30s to 2+ minutes | small model; often approximate |

The labs default to the local `llama3.2:3b` model so they work with no account and no key. That model
is only 3 billion parameters, though, and it shows: it will sometimes pass a sloppy argument to a tool,
or ignore what a tool returned and answer from imagination. The lab still *works* — you'll see the
agents delegate and the protocol do its job — but the answers are often wrong.

With a Groq key the same labs run in seconds and return correct answers, which makes the multi-agent
behavior much easier to follow. Grab a free key (no credit card) at https://console.groq.com and set it
in **each terminal you use**:

```
export GROQ_API_KEY=<your key>
```

Every lab file checks for that variable and switches automatically — there is nothing else to change.

**Instructors:** add `GROQ_API_KEY` as a Codespaces secret
(github.com → Settings → Codespaces → Secrets, with access granted to this repo) and it will be present
in every student codespace with no per-terminal export.

## Alternative: local dev container

If you prefer to run locally in VS Code with Docker installed, use **Dev Containers: Clone Repository
in Container Volume...** from the command palette and point it at this repo. The same setup scripts run.

## Troubleshooting

- **`ollama: command not found`** — the setup script didn't finish. Run `bash scripts/startup_ollama.sh`
  and watch for errors; it needs `zstd` installed (the script installs it for you).
- **Model responses hang** — first query after startup loads the model into memory (1-3 minutes).
  Subsequent queries are faster.
- **`address already in use` when starting an A2A server** — a server from a previous lab is still
  running. Find and stop it: `kill $(lsof -t -i:9999)` (substitute the port from the error message).
- **Package errors** — re-run `pip install -r requirements.txt` inside the activated environment.

## License

Materials in this repository are for educational use only by attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
