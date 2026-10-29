# Local Setup Guide: Windows with Docker Desktop

**Use this only if you can't use GitHub Codespaces. The Codespace (see [README.md](README.md)) is the recommended setup.**

This guide runs the workshop's ready-made environment (the same one the Codespace uses) on your
Windows PC, using Docker Desktop, WSL (Windows Subsystem for Linux), and VS Code. Because it's the same
environment, the labs work exactly as written, including `code -d`.

You do **not** need a GitHub account for this path.

---

## 1. Check your PC

- Windows 11 version 23H2 or later, or Windows 10 version 22H2 (64-bit). These are Docker Desktop's
  current minimums; see its [system requirements](https://docs.docker.com/desktop/setup/install/windows-install/).
- Hardware virtualization turned on in your PC's BIOS/UEFI settings (it usually is already)
- At least 4 CPU cores and **16 GB of memory**
- About **32 GB of free disk space** (the amount the workshop environment is configured for)
- Permission to install software as an administrator

## 2. Install the software (one time)

**a. WSL with Ubuntu**

Right-click the **Start** button, choose **Terminal (Admin)** or **Windows PowerShell (Admin)**, and run:

```
wsl --install
```

Restart your PC when it finishes. After the restart an **Ubuntu** window opens and asks you to create
a Linux username and password. Pick anything you'll remember; you'll need the password for `sudo`.

To confirm, run this in PowerShell. You should see **Ubuntu** with **VERSION 2**:

```
wsl --list --verbose
```

**b. Docker Desktop**
- Download from https://www.docker.com/products/docker-desktop and run the installer.
- When asked, keep **Use WSL 2 instead of Hyper-V** selected.
- Restart if asked, launch Docker Desktop, and finish the setup screens.
- In Docker Desktop, open **Settings** (gear icon):
  - **General**: make sure **Use the WSL 2 based engine** is checked.
  - **Resources → WSL integration**: turn on **Ubuntu**. Click **Apply & restart**.

**c. Visual Studio Code**
- Download from https://code.visualstudio.com/ and run the installer.
- Leave **Add to PATH** checked.

**d. Two VS Code extensions**
- In VS Code, press `Ctrl+Shift+X` to open Extensions.
- Install **Dev Containers** (published by Microsoft).
- Install **WSL** (published by Microsoft).

## 3. Get the workshop files (inside Ubuntu)

Open **Ubuntu** from the Start menu and run:

```
cd ~
git clone https://github.com/skillrepos/multi-agent.git
cd multi-agent
code .
```

Cloning inside Ubuntu (not into a `C:\Users\...` folder) keeps things fast and avoids Windows
line-ending problems with the setup scripts. If `git` isn't found, run `sudo apt update && sudo apt install -y git`
first.

`code .` opens VS Code on Windows, connected to your Ubuntu folder. The first time, it installs a
small VS Code helper inside Ubuntu, which takes a minute.

## 4. Open the folder in the container

When VS Code opens the folder, a notification asks whether to **Reopen in Container**. Click it.

If you miss the notification: press `Ctrl+Shift+P`, type **Dev Containers: Reopen in Container**,
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

- **Run lab commands in the VS Code terminal.** That terminal is inside the container, so `code -d`,
  `curl`, `&`, `kill %1`, and the other lab commands work exactly as written. Don't use PowerShell or
  Command Prompt for the labs, because those commands are written for a Linux-style terminal.
- **Copy and paste** use `Ctrl+C` / `Ctrl+V` (in the VS Code terminal, `Ctrl+Shift+C` / `Ctrl+Shift+V`
  also work).
- **Speed.** The local model runs on your PC's processor inside Docker. It may be faster or slower than
  the Codespace. With a Groq key, speed is the same as in the Codespace.
- **"Port forwarded" pop-ups.** When the Lab 3 and Lab 5 servers start, VS Code may show a pop-up
  about forwarding the port to Windows. You can ignore or close it.
- **Screenshots in the labs** show the Codespace in a browser. You're in the VS Code app, so the window
  around the terminal looks different, but the commands and their output are the same.

## Troubleshooting

- **"Docker is not running" / "Cannot connect to the Docker daemon"** — start Docker Desktop and wait
  until it says it's running. Check **Settings → Resources → WSL integration** has **Ubuntu** turned on.
  If it still fails, run `wsl --shutdown` in PowerShell, then restart Docker Desktop.
- **Ubuntu shows VERSION 1** — in PowerShell run `wsl --set-version Ubuntu 2`.
- **Setup script errors mentioning `$'\r'`** — the files were cloned on the Windows side. Delete that
  copy and clone again inside Ubuntu (step 3).
- **Setup fails or the model is very slow** — close other large programs, make sure you have about
  32 GB of free disk space, and check that antivirus software isn't blocking Docker.
- **Model missing** — run `ollama pull llama3.2:3b` in the VS Code terminal.
- **`ollama` not responding after you reopen the folder** — run `bash scripts/startOllama.sh`.
- **`address already in use`** — a lab server may still be running. Stop it with
  `kill $(lsof -t -i:9999)` (use the port from the error message).

## When you're done

- To leave the container: press `Ctrl+Shift+P` → **Dev Containers: Reopen Folder in WSL**, or just
  close VS Code.
- To free up disk space later: in Docker Desktop, delete the container and image whose names include
  `multi-agent`.

## More help

- [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/)
- [Developing in WSL with VS Code](https://code.visualstudio.com/docs/remote/wsl)
- [Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers)
