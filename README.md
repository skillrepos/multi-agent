# Multi-Agent AI Systems & the A2A Protocol

**Hands-on workshop — Revision 1.0 — 07/31/26**

This repository contains the labs, code, and setup for the *Multi-Agent AI Systems & the A2A Protocol*
workshop. In it, you'll build multi-agent systems with LangGraph and CrewAI, learn Google's A2A
(Agent2Agent) protocol v1.0, and connect agents built in different frameworks into a single
cross-framework agent network.

**Prerequisite**: Experience building single AI agents (via the AI Accelerator, ai-aip workshop, or
equivalent). Comfort with Python and LLM APIs.

---

## Setup — GitHub Codespaces (recommended)

1. Click the button below (or the green **Code** button → **Codespaces** tab → **Create codespace on main**).

2. **Wait for setup to finish.** The codespace installs Python dependencies, installs Ollama, and pulls
   the `llama3.2:3b` model. This takes **3-5 minutes** after the codespace opens. When the terminal
   shows `Ollama is ready with model llama3.2:3b`, you're good to go.

3. Open `labs.md` and start with **Lab 1**.

### System requirements (Codespace machine type)

- 4 cores / 16 GB RAM / 32 GB storage (the default machine type configured for this repo)

## Optional: faster responses with Groq

The labs run entirely on the local `llama3.2:3b` model by default — no API keys needed. Local
responses on a 4-core codespace can take 30 seconds to 2+ minutes. If you have a (free) Groq API
key, the lab code will automatically use Groq's much faster hosted models instead:

```
export GROQ_API_KEY=<your key>
```

Get a free key at https://console.groq.com. Either path works for every lab.

## Alternative: local dev container

If you prefer to run locally in VS Code with Docker installed, use **Dev Containers: Clone Repository
in Container Volume...** from the command palette and point it at this repo. The same setup scripts run.

## Troubleshooting

- **`ollama: command not found`** — the setup script didn't finish. Run `bash scripts/startup_ollama.sh`.
- **Model responses hang** — first query after startup loads the model into memory (1-3 minutes).
  Subsequent queries are faster.
- **`address already in use` when starting an A2A server** — a server from a previous lab is still
  running. Find and stop it: `kill $(lsof -t -i:9999)` (substitute the port from the error message).
- **Package errors** — re-run `pip install -r requirements.txt` inside the activated environment.

## License

Materials in this repository are for educational use only by attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
