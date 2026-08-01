#!/usr/bin/env bash
# Re-attach script: make sure the Ollama server is running.
# Runs on every attach as part of postAttachCommand.
#
# Updated 08/01/26: check that Ollama is actually installed before
# claiming the server was started.

if ! command -v ollama &> /dev/null; then
    echo "WARNING: Ollama is not installed - the local model is unavailable."
    echo "         Run: bash scripts/startup_ollama.sh"
    exit 0
fi

if ! pgrep -x ollama > /dev/null; then
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "Ollama server restarted."
else
    echo "Ollama server already running."
fi
