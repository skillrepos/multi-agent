"""
llm.py - Lab 5: one call to a chat model over plain HTTP (provided - nothing to merge)

Groq and Ollama both accept the same "chat completions" request format, so
this works with either. You send the conversation plus a list of tools the
model may use; it replies with text, or with the tool calls it wants made.
No agent framework involved - just one web request.

Groq's free plan limits how many tokens you can send per minute. If a request
goes over, Groq answers "429 Too Many Requests" and says how long to wait, so
chat() waits that long and tries again (up to 6 times).
"""

import asyncio
import os

MAX_TRIES = 6


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

    for attempt in range(1, MAX_TRIES + 1):
        response = await httpx_client.post(url, headers=headers, json={
            "model": model, "messages": messages, "tools": tools, "temperature": 0})
        if response.status_code != 429 or attempt == MAX_TRIES:
            break
        try:
            wait = float(response.headers.get("retry-after", "10"))
        except ValueError:
            wait = 10.0
        wait = min(max(wait, 1.0), 60.0)
        print(f"  (rate limit reached - waiting {wait:.0f}s, then retrying...)")
        await asyncio.sleep(wait)

    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]
    # Keep only the fields we send back to the model on the next turn
    return {k: v for k, v in reply.items() if k in ("role", "content", "tool_calls")}
