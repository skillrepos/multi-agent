"""
llm.py - Lab 5: one call to a chat model over plain HTTP (provided - nothing to merge)

Groq and Ollama both accept the same "chat completions" request format, so
this works with either. You send the conversation plus a list of tools the
model may use; it replies with text, or with the tool calls it wants made.
No agent framework involved - just one web request.
"""

import os


async def chat(httpx_client, messages, tools):
    """Send the conversation and the available tools; return the model's reply."""
    if os.environ.get("GROQ_API_KEY"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = "openai/gpt-oss-120b"
        headers = {"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"}
    else:
        url = "http://localhost:11434/v1/chat/completions"
        model = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
        headers = {}

    response = await httpx_client.post(url, headers=headers, json={
        "model": model, "messages": messages, "tools": tools, "temperature": 0})
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]
    # Keep only the fields we send back to the model on the next turn
    return {k: v for k, v in reply.items() if k in ("role", "content", "tool_calls")}
