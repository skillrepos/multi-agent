# Local Setup Guide: Mac with Docker Desktop

**Use this only if you can't use GitHub Codespaces. The Codespace (see [README.md](README.md)) is the recommended setup.**

This guide runs the workshop's ready-made environment (the same one the Codespace uses) on your Mac,
using Docker Desktop and VS Code. Because it's the same environment, the labs work exactly as written,
including `code -d`.

You do **not** need a GitHub account for this path.

## What you'll need

| | What | Where it's covered |
|---|---|---|
| **Computer** | Mac (Apple Silicon or Intel), 4+ CPU cores, **16 GB** memory, about **32 GB** free disk | Step 1 |
| **Software** (all free) | Docker Desktop, VS Code with the Dev Containers extension, Git | Step 2 |
| **Groq API key** | Recommended, free (the labs run without it, just slowly) | Step 7 |
| **Internet access during setup** | github.com, mcr.microsoft.com, and ghcr.io (the workshop environment); pypi.org and files.pythonhosted.org (Python packages); ollama.com and registry.ollama.ai (the local model); console.groq.com and api.groq.com (Groq). If your company network blocks downloads from any of these, do the setup on another network or ask your IT team. | |

Everything else is installed for you inside the container, including the Python packages for
LangGraph, CrewAI, and **A2A**. A2A needs no account and no separate download: it's the `a2a-sdk`
Python package, and the A2A agents you build in Labs 3-5 run inside the container on your own
computer, on ports **9999**, **10001**, and **10002**.

---

## 1. Check your Mac

- macOS on Apple Silicon (M1 or later) or Intel
- At least 4 CPU cores and **16 GB of memory**
- About **32 GB of free disk space** (the amount the workshop environment is configured for)

## 2. Install the software (one time)

**a. Docker Desktop**
- Download from https://www.docker.com/products/docker-desktop. Choose **Mac with Apple chip** or
  **Mac with Intel chip** to match your Mac (Apple menu → *About This Mac* tells you which).
- Open the download, drag **Docker** to **Applications**, and launch it.
- Finish the setup screens. When Docker is running you'll see the whale icon in your menu bar.
- Give Docker enough memory: Docker Desktop → **Settings** (gear icon) → **Resources**. Set **Memory**
  to at least **8 GB** and **CPUs** to at least **4**, then click **Apply & restart**.

**b. Visual Studio Code**
- Download from https://code.visualstudio.com/, open the .zip, and drag **Visual Studio Code** to
  **Applications**. Launch it.

**c. The Dev Containers extension for VS Code**
- In VS Code, press `Cmd+Shift+X` to open Extensions.
- Search for **Dev Containers** (published by Microsoft) and click **Install**.

**d. Git**
- Open the **Terminal** app and run `git --version`. If macOS offers to install the command line
  developer tools, click **Install** and wait for it to finish.

## 3. Get the workshop files

In the Terminal app:

```
cd ~
git clone https://github.com/skillrepos/multi-agent.git
cd multi-agent
code .
```

If `code .` says *command not found*, open VS Code, press `Cmd+Shift+P`, run
**Shell Command: Install 'code' command in PATH**, then try `code .` again (or use
**File → Open Folder...** and pick the `multi-agent` folder).

## 4. Open the folder in the container

When VS Code opens the folder, a notification asks whether to **Reopen in Container**. Click it.

If you miss the notification: press `Cmd+Shift+P`, type **Dev Containers: Reopen in Container**,
and press Enter.

## 5. Wait for the first-time setup

The first time takes about **10-15 minutes**. VS Code downloads the base environment, installs the
Python packages, installs Ollama, and downloads the local `llama3.2:3b` model. You can watch the
progress in the terminal panel.

The last setup message is `Ollama is ready with model llama3.2:3b`. That terminal may close before you
see it - that's fine, step 6 checks that everything is in place. Later openings take under a minute.

## 6. Check that it worked

Open a new terminal in VS Code (**Terminal → New Terminal**) and run:

```
ollama list
python -c "from a2a.server.routes import create_jsonrpc_routes; from a2a.client import create_client; import crewai, langgraph, uvicorn; print('Python packages OK')"
```

You should see `llama3.2:3b` in the list, then `Python packages OK`. (The second command checks the
A2A server and client pieces as well as LangGraph and CrewAI.)

## 7. Set up your Groq key

Go back to [README.md](README.md) and do **steps 4 and 5** (get a free Groq key, then run
`source scripts/setup-key.sh` in the VS Code terminal). Then open `labs.md` and start Lab 1.

---

## What looks different from the Codespace

Very little, because this is the same environment:

- **`code -d` works the same way.** Run lab commands in the VS Code terminal (inside the container),
  not in the Mac Terminal app.
- **Speed.** The local model runs on your Mac's processor inside Docker. It may be faster or slower
  than the Codespace. With a Groq key, speed is the same as in the Codespace.
- **"Port forwarded" pop-ups.** When the Lab 3 and Lab 5 servers start, VS Code may show a pop-up
  about forwarding the port to your Mac. You can ignore or close it.
- **Screenshots in the labs** show the Codespace in a browser. You're in the VS Code app, so the
  window around the terminal looks different, but the commands and their output are the same.

## Troubleshooting

- **"Docker is not running"** — start Docker Desktop and wait for the whale icon in the menu bar to stop
  animating, then retry *Reopen in Container*.
- **Setup fails or the model is very slow** — check Docker Desktop → Settings → Resources (at least
  8 GB memory, 4 CPUs) and that you have about 32 GB of free disk space.
- **Model missing** — run `ollama pull llama3.2:3b` in the VS Code terminal.
- **`ollama` not responding after you reopen the folder** — run `bash scripts/startOllama.sh`.
- **`address already in use`** — a lab server you started earlier is still running in the container.
  Stop it with `kill $(lsof -t -i:9999)` (use the port from the error message).

- **`curl` or a lab script can't reach `127.0.0.1` (connection refused, or an error page from your
  company's network) while the lab server is running** — your company sends web traffic through a
  proxy server, and the labs' requests to your own computer are being sent there too. In each terminal
  you use for the labs, run `export NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1`. To make
  that permanent inside the container, run
  `echo 'export NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1' >> ~/.bashrc` once.

## When you're done

- To leave the container: press `Cmd+Shift+P` → **Dev Containers: Reopen Folder Locally**, or just
  close VS Code.
- To free up disk space later: in Docker Desktop, delete the container and image whose names include
  `multi-agent`.
