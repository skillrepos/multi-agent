#!/usr/bin/env bash
# Re-attach script: make sure the Ollama server is running.
# Runs on every attach as part of postAttachCommand.

if ! pgrep -x ollama > /dev/null; then
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "Ollama server restarted."
else
    echo "Ollama server already running."
fi
