#!/usr/bin/env bash
# Install Ollama and pull the workshop model.
# Runs once as part of postCreateCommand.

MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start the Ollama server in the background if it isn't running
if ! pgrep -x ollama > /dev/null; then
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
fi

echo "Pulling model $MODEL (this can take a few minutes)..."
ollama pull "$MODEL"
echo "Ollama is ready with model $MODEL."
