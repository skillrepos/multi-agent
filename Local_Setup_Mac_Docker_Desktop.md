# Local Setup Guide: Mac with Docker Desktop

**Use this only if you can't use GitHub Codespaces. The Codespace (see [README.md](README.md)) is the recommended setup.**

This guide runs the workshop's ready-made environment (the same one the Codespace uses) on your Mac,
using Docker Desktop and VS Code. Because it's the same environment, the labs work exactly as written,
including `code -d`.

You do **not** need a GitHub account for this path.

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

It's ready when the terminal shows `Ollama is ready with model llama3.2:3b`. Later openings take
under a minute.

## 6. Check that it worked

Open a new terminal in VS Code (**Terminal → New Terminal**) and run:

```
ollama list
python -c "import a2a, crewai, langgraph; print('Python packages OK')"
```

You should see `llama3.2:3b` in the list, then `Python packages OK`.

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
- **`address already in use`** — another program on your Mac may be using port 9999, 10001, or 10002.
  Quit it, or stop a lab server you left running with `kill $(lsof -t -i:9999)` (use the port from the
  error message).

## When you're done

- To leave the container: press `Cmd+Shift+P` → **Dev Containers: Reopen Folder Locally**, or just
  close VS Code.
- To free up disk space later: in Docker Desktop, delete the container and image whose names include
  `multi-agent`.
