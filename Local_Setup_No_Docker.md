# Local Setup Guide: No Docker (Mac, or Windows using WSL)

**Use this only if you can't use GitHub Codespaces or Docker Desktop. The Codespace (see
[README.md](README.md)) is the recommended setup. If you can install Docker Desktop, the
[Mac](Local_Setup_Mac_Docker_Desktop.md) and [Windows](Local_Setup_Windows_Docker_Desktop.md) Docker
guides give you the identical environment with fewer differences.**

In this guide you install the pieces yourself: Python, the workshop's Python packages, Ollama with the
local model, and VS Code. Then read **[What looks different from the Codespace](#what-looks-different-from-the-codespace)**
at the end before you start the labs.

You do **not** need a GitHub account for this path.

| Your computer | Follow |
|---|---|
| Mac | [Part A](#part-a-mac) |
| Windows | [Part B](#part-b-windows-using-wsl), which uses WSL, the Linux environment built into Windows. The lab commands are written for a Mac/Linux-style terminal, so plain PowerShell or Command Prompt won't work for the labs. |
| Linux | [Part B](#part-b-windows-using-wsl) from step B3 (use your distribution's package manager if it isn't Ubuntu/Debian) |

You'll need about **10 GB of free disk space** and at least **8 GB of memory** (16 GB recommended).

---

## Part A: Mac

### A1. Install Python 3.12

The workshop needs Python **3.10 to 3.13**. (One of the packages, CrewAI, doesn't support 3.14
yet.) The `python3` that comes with macOS is usually 3.9, which is **too old**, so install 3.12:

- Download the **macOS 64-bit universal2 installer** for Python 3.12 from
  https://www.python.org/downloads/macos/ and run it.
- Or, if you use Homebrew: `brew install python@3.12`

Check it in the **Terminal** app:

```
python3.12 --version
```

### A2. Install Git

```
git --version
```

If macOS offers to install the command line developer tools, click **Install** and wait for it to finish.

### A3. Install VS Code and its `code` command

- Download from https://code.visualstudio.com/, open the .zip, and drag **Visual Studio Code** to
  **Applications**. Launch it.
- Press `Cmd+Shift+P`, type **Shell Command: Install 'code' command in PATH**, and press Enter.
  The labs use `code` to open files and to merge code (`code -d`).

### A4. Install Ollama and the local model

- Download the Mac app from https://ollama.com/download, drag **Ollama** to **Applications**, and open it.
  It runs in the background (look for the llama icon in the menu bar) and starts automatically after you log in.
- In a **new** Terminal window, download the model the labs use (about 2 GB):

```
ollama pull llama3.2:3b
```

### A5. Get the workshop files and install the Python packages

```
cd ~
git clone https://github.com/skillrepos/multi-agent.git
cd multi-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The install takes a few minutes. Your prompt now starts with `(.venv)`. That means the workshop's Python
environment is turned on in this terminal.

### A6. Check that it worked

```
code .
```

VS Code opens the `multi-agent` folder. Open a terminal in VS Code (**Terminal → New Terminal**) and run:

```
source .venv/bin/activate
python --version
python -c "import a2a, crewai, langgraph; print('Python packages OK')"
ollama list
code --version
```

You should see Python 3.12, `Python packages OK`, `llama3.2:3b` in the model list, and a VS Code version number.

### A7. Set up your Groq key

Go back to [README.md](README.md) and do **steps 4 and 5**. The `source scripts/setup-key.sh` command
works in the Mac terminal and saves the key so new terminals get it too.

Then read [What looks different](#what-looks-different-from-the-codespace) below and start Lab 1.

---

## Part B: Windows (using WSL)

### B1. Install WSL with Ubuntu

Right-click the **Start** button, choose **Terminal (Admin)** or **Windows PowerShell (Admin)**, and run:

```
wsl --install
```

Restart your PC when it finishes. After the restart an **Ubuntu** window opens and asks you to create a
Linux username and password. Pick anything you'll remember; you'll need the password for `sudo`.

From now on, run every workshop command in the **Ubuntu** window (open it from the Start menu) or in
VS Code's terminal once it's connected to Ubuntu (step B4). Don't use PowerShell for them.

### B2. Install VS Code and the WSL extension (on Windows)

- Download VS Code from https://code.visualstudio.com/ and run the installer. Leave **Add to PATH** checked.
- In VS Code, press `Ctrl+Shift+X`, search for **WSL** (published by Microsoft), and click **Install**.

### B3. Install Python, Git, and helpers (in Ubuntu)

```
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl zstd
python3 --version
```

The version must be **3.10 to 3.13**. Current Ubuntu gives you 3.12.

### B4. Get the workshop files and install the Python packages (in Ubuntu)

```
cd ~
git clone https://github.com/skillrepos/multi-agent.git
cd multi-agent
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Clone into your Ubuntu home folder (`~`), **not** a Windows folder like `/mnt/c/Users/...`. It's much
faster, and it avoids Windows line-ending problems with the setup scripts.

### B5. Install Ollama and the local model (in Ubuntu)

The workshop's own setup script does this. It installs Ollama, starts it, and downloads the model
(about 2 GB):

```
bash scripts/startup_ollama.sh
```

It's finished when you see `Ollama is ready with model llama3.2:3b`.

If you already have the **Windows** version of Ollama installed, quit it (right-click the llama icon by the
clock → Quit) so the two don't get in each other's way.

After you restart Windows or close Ubuntu, start the model server again before the labs:

```
bash scripts/startOllama.sh
```

### B6. Open VS Code and check that it worked

```
code .
```

VS Code opens on Windows, connected to your Ubuntu folder (the first time it installs a small helper,
which takes a minute). The lower-left corner says **WSL: Ubuntu**. Open a terminal in VS Code
(**Terminal → New Terminal**) and run:

```
source .venv/bin/activate
python --version
python -c "import a2a, crewai, langgraph; print('Python packages OK')"
ollama list
```

You should see Python 3.10-3.13, `Python packages OK`, and `llama3.2:3b` in the model list.

### B7. Set up your Groq key

Go back to [README.md](README.md) and do **steps 4 and 5**, running `source scripts/setup-key.sh` in the
VS Code terminal. Then read [What looks different](#what-looks-different-from-the-codespace) below and
start Lab 1.

---

## What looks different from the Codespace

The labs are written for the Codespace. On your own machine, these are the things that change:

### 1. Turn on the Python environment in every new terminal

The Codespace does this automatically. You don't get that, so **every time you open a terminal**
(the labs open a second one in Labs 3 and 5), first run this from the `multi-agent` folder:

```
source .venv/bin/activate
```

Your prompt shows `(.venv)` when it's on. (In the lab screenshots it shows `(a)`. That's the Codespace's
name for the same thing.) If a lab command fails with `ModuleNotFoundError`, this is almost always why.

New terminals in VS Code open in the `multi-agent` folder, just like in the Codespace. In the Mac
Terminal app, `cd ~/multi-agent` first.

### 2. Merging code: if `code -d` doesn't work for you

The labs complete each starter file by running `code -d` and clicking arrows in VS Code's side-by-side
view. If you installed VS Code and its `code` command (steps A3 / B2), this works exactly as in the labs.

If you use a different editor, or `code -d` won't work, you have two options:

- **Do the merge by hand.** Open both files named in the `code -d` command side by side, for example
  `../extra/supervisor_team.txt` (finished) and `supervisor_team.py` (starter). In the starter, find each
  `# TODO` line and replace it with the matching block from the finished file. Many editors and tools
  can compare two files and show the missing blocks, for example PyCharm (*Compare With...*), Meld,
  WinMerge, Beyond Compare, or `git diff --no-index <finished> <starter>`.
- **Copy the finished file over the starter.** The finished file is exactly what you'd have after
  merging every block. You skip the hands-on merge, but the rest of the lab works the same. Run the
  command from the same folder the lab's `code -d` step runs in:

| Lab | Instead of `code -d ...`, run |
|---|---|
| Lab 1 (in `agents`) | `cp ../extra/supervisor_team.txt supervisor_team.py` |
| Lab 2 (in `agents`) | `cp ../extra/content_crew.txt content_crew.py` |
| Lab 3, step 2 (in `protocol`) | `cp ../extra/stats_executor.txt stats_executor.py` |
| Lab 3, step 5 (in `protocol`) | `cp ../extra/stats_server.txt stats_server.py` |
| Lab 4 (in `protocol`) | `cp ../extra/stats_client.txt stats_client.py` |
| Lab 5 (in `network`) | `cp ../extra/orchestrator.txt orchestrator.py` |

Either way, still read the code the lab step asks you to look at. That's where the learning is.

Other places the labs say `code <file>` just open a file to read or edit. Open it in any editor.

### 3. Setup messages

- **Mac:** you won't see `Ollama is ready with model llama3.2:3b` (that message comes from the setup
  script). Ollama is ready when the llama icon is in your menu bar and `ollama list` shows the model.
- **WSL:** you see the message when you run `bash scripts/startup_ollama.sh` (step B5).

### 4. Speed of the local model

Without a Groq key, Labs 1, 2, and 5 run on your own computer. A recent Mac (Apple Silicon) is often
**faster** than the Codespace. A Windows laptop running the model through WSL may be faster or slower.
With a Groq key, speed is the same everywhere.

### 5. Ports the lab servers use

Lab 3 starts a server on port **9999**, and Lab 5 starts two on **10001** and **10002**. If another
program on your computer already uses one of those, you'll see `address already in use`. To find what's
using a port: `lsof -i :9999`. If it's a lab server you left running, stop it with `kill $(lsof -t -i:9999)`.

### 6. What your screen looks like

The lab screenshots show the Codespace in a browser, with a prompt like
`(a) @brentlaster ➜ /workspaces/multi-agent/agents (main) $`. Your prompt and folder path look different
(for example `(.venv) yourname@yourmac agents %`), but the commands and their output are the same.

On a Mac, copy and paste in the terminal with `Cmd+C` / `Cmd+V`.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named ...`** — the Python environment isn't on in this terminal. Run
  `source .venv/bin/activate` from the `multi-agent` folder.
- **`pip install` fails mentioning your Python version** — check `python --version` inside the environment.
  It must be 3.10 to 3.13. Delete the `.venv` folder and create it again with the right Python (step A5 / B4).
- **`code: command not found`** — Mac: redo step A3. Windows: make sure you're in the Ubuntu terminal or a
  VS Code terminal connected to WSL, and that the WSL extension is installed (step B2). Or use the
  copy commands in [What looks different](#2-merging-code-if-code--d-doesnt-work-for-you).
- **Lab hangs or says it can't connect to the model** — Mac: open the Ollama app. WSL: run
  `bash scripts/startOllama.sh`. Then check `ollama list` shows `llama3.2:3b`. If not, run
  `ollama pull llama3.2:3b`.
- **First request is very slow** — the model loads into memory on its first use (up to a few minutes).
  Later requests are faster.
- **`$'\r': command not found` from a script (Windows)** — the files were cloned into a Windows folder.
  Clone again inside your Ubuntu home folder (step B4).

## Clean up afterwards

```
# from the folder that contains multi-agent
rm -rf multi-agent          # removes the workshop files and its Python environment
ollama rm llama3.2:3b       # frees about 2 GB
```
