# Multi-Agent AI Systems & the A2A Protocol

**Hands-on workshop — Revision 1.4 — 10/29/26**

This repository contains the labs, code, and setup for the *Multi-Agent AI Systems & the A2A Protocol*
workshop. In it, you'll build multi-agent systems with LangGraph and CrewAI, learn the A2A
(Agent2Agent) protocol v1.0, and connect agents built in different frameworks into a single
cross-framework agent network.

**Prerequisite**: Experience building single AI agents (via the AI Accelerator, ai-aip workshop, or
equivalent). Comfort with Python and LLM APIs.

---

## What you need before the workshop

| | Needed? | Cost | Where it's covered |
|---|---|---|---|
| **GitHub account** (signed in) | **Required** for the Codespace | Free | Step 1 below |
| **Groq API key** | Recommended (labs run without it, just slowly) | Free | Steps 4 and 5 below |

That's all. You do **not** need any account for A2A, LangGraph, or CrewAI. They are open-source
libraries the Codespace installs for you, and the A2A agents you build run inside your own
Codespace. The local AI model is downloaded for you too.

The Codespace runs on a 4-core machine, which uses your free monthly Codespaces hours 4x as fast
as the smallest machine. The free allowance comfortably covers this workshop. When you're done,
delete the codespace at https://github.com/codespaces.

**Can't use GitHub Codespaces** (blocked at work, no GitHub account, etc.)? Use one of the manual
setup guides instead. Each one ends by sending you back here for steps 4 and 5 (the Groq key):

- [Mac with Docker Desktop](Local_Setup_Mac_Docker_Desktop.md) — the same environment as the Codespace, on your machine
- [Windows with Docker Desktop](Local_Setup_Windows_Docker_Desktop.md) — the same environment as the Codespace, on your machine
- [No Docker (Mac, or Windows using WSL)](Local_Setup_No_Docker.md) — install the pieces yourself

<br>

---

## Setup — GitHub Codespaces (recommended)

**1. Change your codespace's default timeout from 30 minutes to longer.**
Signed in to GitHub, go to https://github.com/settings/codespaces and scroll down to the
*Default idle timeout* section. Raise the value (for example, to 120 minutes) and click **Save**.

![Changing codespace idle timeout value](./images/maa2a-0-1.png?raw=true "Changing codespace idle timeout value")

<br>

**2. Click the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/multi-agent?quickstart=1)

<br>

**3. Click *Create new codespace*, then wait for setup to finish.**

<!-- SCREENSHOT TO CAPTURE: images/maa2a-0-2.png - the "Create codespace" page for skillrepos/multi-agent with the "Create new codespace" button -->

The codespace opens in your browser, then runs a setup script that installs the Python packages,
installs Ollama, and downloads the local `llama3.2:3b` model. This takes **3-5 minutes**. You can
watch it in the terminal at the bottom of the screen.

<!-- SCREENSHOT TO CAPTURE: images/maa2a-0-3.png - terminal while postCreateCommand is running -->

The codespace is ready when the terminal shows `Ollama is ready with model llama3.2:3b`.

<!-- SCREENSHOT TO CAPTURE: images/maa2a-0-4.png - terminal showing "Ollama is ready with model llama3.2:3b" -->

<br>

**4. Get a free Groq API key (recommended).**

Labs 1, 2, and 5 call an AI model. Without a key they use the small local model, which works but
is slow and often gets details wrong. With a free Groq key the same labs run in seconds and give
correct answers, which makes the agents' behavior much easier to follow. The lab steps are the
same either way.

| | Setup | Speed | Answer quality |
|---|---|---|---|
| **Groq** (recommended) | free API key | **seconds** | reliable |
| **Local model** (no key) | nothing | 30 seconds to 2+ minutes | often approximate |

a. In a browser, go to https://console.groq.com and create an account (no credit card needed). If
you get an email with a confirmation button, make sure the link opens in the same browser you used
for Groq. If it doesn't, copy the link and paste it into that browser.

b. In the top right of the Groq screen, click **API Keys**.

![API keys](./images/maa2a-0-5.png?raw=true "API keys")

c. Click the **Create API Key** button.

![Create API Key](./images/maa2a-0-6.png?raw=true "Create API Key")

d. Give the key a name, and pick an **Expiration** later than your workshop date. Verify you're
human if asked, and click **Submit**.

![Name the key](./images/maa2a-0-7.png?raw=true "Name the key")

e. **Copy the key now.** Groq shows it only once. Keep it somewhere handy until step 5.

![Copy the key](./images/maa2a-0-8.png?raw=true "Copy the key")

<br>

**5. Set your Groq key in the codespace.**

Back in the codespace **TERMINAL**, run the command below. Paste your key when asked (it won't be
shown as you paste), then press *Enter*:

```
source scripts/setup-key.sh
```

This sets the key in this terminal *and* in every terminal you open later, so you only do it once.

<!-- SCREENSHOT TO CAPTURE: images/maa2a-0-9.png - output of "source scripts/setup-key.sh" -->

Then confirm the key works:

```
bash scripts/check-groq.sh
```

You should see a line starting with `OK`. If you see `FAIL`, the message tells you what to do next.

<!-- SCREENSHOT TO CAPTURE: images/maa2a-0-10.png - output of "bash scripts/check-groq.sh" showing OK -->

<br>

**6. Open `labs.md` and start with Lab 1.**
You can open it in the codespace (click it in the file list on the left) or in a separate browser
tab on GitHub.

**Now you're ready for the labs!**

<br>

**If your codespace times out and you need to reopen it:**
go to https://github.com/codespaces, find the codespace, click the **...** menu next to it, and
choose *Open in browser*. Your Groq key is remembered. If `bash scripts/check-groq.sh` says it
isn't set, repeat step 5.

<br>

---

## Troubleshooting

- **`ollama: command not found`** — the setup script didn't finish. Run `bash scripts/startup_ollama.sh`
  and watch for errors.
- **Lab says it can't reach the local model** after reopening a codespace — restart the model server:
  `bash scripts/startOllama.sh`
- **Model responses hang** — the first request after startup loads the model into memory (1-3 minutes).
  Later requests are faster.
- **`address already in use` when starting an A2A server** — a server from a previous lab is still
  running. Find and stop it: `kill $(lsof -t -i:9999)` (use the port number from the error message).
- **Package errors** — re-run `pip install -r requirements.txt`.
- **`401 Invalid API Key` / `expired_api_key` from Groq** — the key is wrong or has expired. Create a
  new one (step 4) and run `source scripts/setup-key.sh` again. To skip Groq and use the local model
  instead, run `unset GROQ_API_KEY` (lasts for that terminal only).
- **`model_decommissioned` from Groq** — Groq retires models from time to time. The labs use
  `openai/gpt-oss-120b`; if that is ever retired, pick a current tool-calling model from
  https://console.groq.com/docs/models and change the model name in `get_model()` / `get_llm()`.

## License

Materials in this repository are for educational use only by attendees of our workshops.

(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
