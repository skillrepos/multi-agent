# Instructions for AI assistants in this repo

This is a hands-on training repository for the workshop *Multi-Agent AI Systems & the A2A Protocol*.
Students are here to learn by doing. When a student asks you to explain a code file, use the
"Explain this app" format below. Do not write lab solutions for students — the completed versions
already exist in `extra/` and the labs walk students through merging them.

## Explain-this-app format

When asked to explain any Python file in this repo, structure the answer as:

1. **What it does** — one or two sentences on the file's purpose in plain language.
2. **High-level flow** — the main phases of execution, in order.
3. **Key building blocks** — the important classes/functions used (e.g., `create_agent`,
   `AgentExecutor`, `Crew`, `A2ACardResolver`) and what each contributes.
4. **Data flow** — what goes in, how it's transformed, what comes out.
5. **Safe experiments** — two or three small changes the student could try.
6. **Debug checklist** — the most likely reasons this file would fail and how to check each.

## Repo orientation

- `labs.md` — the lab document students follow.
- `agents/` — Labs 1-2: LangGraph supervisor team, CrewAI crew.
- `protocol/` — Labs 3-4: A2A server, executor, and client.
- `network/` — Lab 5: cross-framework A2A agent network.
- `extra/` — completed versions of skeleton files (students merge these in with `code -d`).
- Model selection: every lab file uses Ollama `llama3.2:3b` locally, or Groq automatically
  if `GROQ_API_KEY` is set.
