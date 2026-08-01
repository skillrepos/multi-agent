#!/usr/bin/env bash
# Install Ollama and pull the workshop model.
# Runs once as part of postCreateCommand.
#
# Updated 08/01/26: install zstd before Ollama (the installer extracts a
# .tar.zst archive and the bookworm base image does not ship zstd), and
# verify each stage instead of unconditionally reporting success.

set -o pipefail

MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

# --- Prerequisite: the Ollama installer needs zstd to unpack its archive ---
if ! command -v zstd &> /dev/null; then
    echo "Installing zstd (required by the Ollama installer)..."
    sudo apt-get update -qq && sudo apt-get install -y zstd
fi

if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama installation failed - 'ollama' is not on PATH."
    echo "       The labs will not be able to use the local model."
    echo "       Try re-running: bash scripts/startup_ollama.sh"
    exit 1
fi

# Start the Ollama server in the background if it isn't running
if ! pgrep -x ollama > /dev/null; then
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
fi

echo "Pulling model $MODEL (this can take a few minutes)..."
if ! ollama pull "$MODEL"; then
    echo "ERROR: Failed to pull model $MODEL. See /tmp/ollama.log for details."
    exit 1
fi

echo "Ollama is ready with model $MODEL."
