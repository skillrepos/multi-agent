# Multi-Agent AI Systems & the A2A Protocol
## Hands-on labs
## Revision 1.2 - 08/01/26

**Startup: If you haven't already, follow the steps in the README to start your codespace. Wait until you see "Ollama is ready with model llama3.2:3b" in the terminal before starting Lab 1 (setup takes 3-5 minutes).**

**Notes:**
1. To copy and paste in the codespace, you may need to use keyboard commands - CTRL+C and CTRL+V (CMD+C and CMD+V on Mac).
2. Some lab files are *skeletons* - they have TODO markers where code is missing. You'll complete them by merging in code from the completed versions in the **extra** directory using VS Code's diff view (`code -d`). In the diff view, hover over the middle bar between the two files and click the **arrow** next to each highlighted block to copy it into your file. When all blocks are merged, **save the file** (CTRL+S / CMD+S) and close the diff tab.
3. **Recommended: use a free Groq API key.** Labs 1, 2, and 5 call an LLM. Out of the box they use the local llama3.2:3b model via Ollama, which needs no account - but it's a 3B model, so responses take **30 seconds to 2+ minutes** and the answers are often approximate (it may pass a sloppy argument to a tool, or ignore what the tool returned). With a free Groq key those same labs run in **seconds** with reliable answers, which makes the agent behavior far easier to follow. Get a key (no credit card) at https://console.groq.com and run this in **each terminal you use**:

```
export GROQ_API_KEY=<your key>
```

Every lab file checks for that variable and switches automatically. **The lab steps are identical either way** - if your instructor has already set it up as a codespace secret, it is set for you and there is nothing to do.
4. When you need a second terminal, click the **+** icon in the upper right of the terminal panel (or use CTRL+SHIFT+`). New terminals open at the repo root, so `cd` to the right directory.

<br><br>

**Lab 1 - Multi-Agent Foundations: A Supervisor and Its Team (LangGraph)**

**Purpose: To see how a multi-agent system is put together in LangGraph using the *supervisor* pattern - specialist agents wrapped as tools that a coordinating agent can call. (Estimated time: 10-12 minutes)**

**Steps:**

1. In a terminal, change into the directory for this lab and take a look at the skeleton file for our multi-agent team.

```
cd agents
code supervisor_team.py
```

<br>

2. Scroll through the file. Notice what's already there: a `get_model()` function that picks Groq or local Ollama, and two plain tools - `lookup_company` (a small knowledge base) and `calculate` (arithmetic). What's *missing* (the TODO sections) are the agents themselves. Close the file when done. **Note: this file is incomplete - we'll merge in the working code in the next step.**

<br>

3. Open a diff view against the completed version and merge in each block of missing code. There are three blocks: the **specialist agents** (researcher + analyst, each a full agent with its own tools), the **delegation tools** (`research` and `analyze` - each wraps a specialist so the supervisor can call it like any other tool), and the **supervisor** agent itself. Click the arrow next to each highlighted block to merge it, then **save** and close the diff tab.

```
code -d ../extra/supervisor_team.txt supervisor_team.py
```

![Merging code for the supervisor team](./images/maa2a-1-1.png?raw=true "Merging code for the supervisor team")

<br>

4. Look at the merged code for the delegation tools. This is the heart of the supervisor pattern: `research` is just a function with the `@tool` decorator, but inside it *invokes a complete agent* and returns that agent's final message. The supervisor can't tell the difference between a simple tool and a whole team member.

<br>

5. Now run the team. The supervisor gets a question that needs both specialists: a research part ("where is Acme Corp headquartered") and a math part ("how many employees if it tripled").

```
python supervisor_team.py
```

**A few seconds on Groq; a minute or two on the local model - the supervisor makes several LLM calls to plan, delegate, and combine results.**

<br>

6. When it finishes, look at the **MESSAGE TRACE** section of the output. You should see the supervisor calling the `research` tool, then the `analyze` tool, with a `[TOOL]` result after each call.

![Supervisor message trace](./images/maa2a-1-2.png?raw=true "Supervisor message trace")

<br>

7. Look at the **FINAL ANSWER**. The supervisor combined what its two specialists returned into a single response. Note that the supervisor itself never called `lookup_company` or `calculate` directly - those belong to the specialists.

**Focus on the routing, not the facts.** On Groq the answer should be exactly right (Portland, Oregon and 3600 employees). On the local 3B model the city or the numbers are often wrong - it may pass a sloppy argument to a tool, or ignore what the tool returned and fill the gap from imagination. That's a model-size limitation, not a flaw in the pattern, and it's precisely why production systems validate what comes back from a delegated agent.

<br>

8. Let's change the question and watch the delegation change. Open the file and find the `question =` line near the bottom, then change it to ask about a different company - for example:

```
code supervisor_team.py
```

Change the question to:

```
    question = ("Where is Globex headquartered, and how many employees "
                "would it have if it doubled?")
```

Save the file (CTRL+S).

<br>

9. Run it again and check the message trace - the supervisor should delegate research about *Globex* this time and hand the doubling math to the analyst.

```
python supervisor_team.py
```

**Small local models occasionally mis-route a step or skip a tool call - if that happens, just run it again. This flakiness is exactly why production multi-agent systems add routing rules and validation, which we'll talk about in the slides.**

<br>

10. Before moving on, notice what this pattern gives us: each specialist has a narrow job and a small toolset (easier to test, less prompt confusion), and the supervisor only makes *routing* decisions. The tradeoff: every hop is another LLM call, so latency and cost grow with team size. In Lab 2, we'll see a different framework's take on the same idea.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 2 - Role-Based Crews (CrewAI)**

**Purpose: To build the same kind of multi-agent collaboration with CrewAI's role/goal/backstory model and see how a process type (sequential) moves work between agents automatically. (Estimated time: 10-12 minutes)**

**Steps:**

1. You should still be in the **agents** directory. Take a look at the skeleton for our content crew. Notice the TODO sections for agents, tasks, and the crew itself. **This file won't run yet.**

```
code content_crew.py
```

<br>

2. Merge in the completed code. There are three blocks: the **agents** (a researcher and a writer - notice there's no code for *how* they work, just role, goal, and backstory text), the **tasks** (each with a description, an `expected_output`, and an assigned agent), and the **crew** (agents + tasks + `Process.sequential`). Merge each block, **save**, and close the diff tab.

```
code -d ../extra/content_crew.txt content_crew.py
```

<br>

3. Look at the merged `writing_task`. The key line is `context=[research_task]` - that's what pipes the researcher's output into the writer's prompt. In a sequential process, CrewAI runs the tasks in list order and handles that handoff for you.

<br>

4. Run the crew with its default topic (GitHub Codespaces - a topic even the small local model knows well, so we can focus on the *handoff* rather than the content):

```
python content_crew.py
```

**CrewAI prints banners as each agent starts and finishes. About 5 seconds on Groq; a couple of minutes on the local model. When the run ends, CrewAI asks "Would you like to view your execution traces? [y/N]" - just press ENTER (or wait 20 seconds) to skip it and get your prompt back.**

<br>

5. Watch the output as it runs. You'll see the **Technology Researcher** agent execute first, producing its bullet list of facts.

![Crew execution output](./images/maa2a-2-1.png?raw=true "Crew execution output")

<br>

6. Then the **Technical Writer** runs. Its task prompt includes the researcher's bullets as context - that's the `context=[research_task]` line doing its job.

<br>

7. When the run completes, look at the **FINAL OUTPUT** section - a short paragraph built from the researcher's facts.

<br>

8. Now run it with a topic of your own. The script takes the topic as a command-line argument:

```
python content_crew.py "Docker containers"
```

**Pick a topic the model is likely to know. A small local model has no web access and no knowledge of very recent technology - ask it about something obscure (or about A2A itself, which postdates its training) and the researcher will honestly report that it found nothing.**

<br>

9. Compare the researcher's bullets to the writer's paragraph in this run - you should be able to trace each sentence back to a bullet. That traceability between agents is one of the first things to check when debugging any multi-agent pipeline.

<br>

10. Compare this lab to Lab 1. LangGraph gave us *explicit* control flow - we wrote the delegation tools ourselves. CrewAI gave us *declarative* collaboration - we described who the agents are and what the tasks produce, and the process type decided the flow. Also note `Process.sequential` in the crew: CrewAI's other process type, `Process.hierarchical`, adds a manager agent that decides task order dynamically - it needs a stronger model than our local 3B, which is why we're using sequential today.

<br>

11. Both labs so far share one big limitation: everything lives in **one process, one framework, one codebase**. The researcher can't be reused by a team written in another framework, and nothing outside this script can even find out these agents exist. That's the problem the A2A protocol solves - and it's where we go next.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 3 - Your First A2A Agent: Cards, Servers, and Tasks**

**Purpose: To build and run a real A2A (spec v1.0) agent server - an AgentExecutor that does the work, an Agent Card that advertises it, and a JSON-RPC endpoint we can hit with nothing but curl. (Estimated time: 10-12 minutes)**

**Steps:**

1. Change into the protocol directory and look at the skeleton for the agent's "brain" - the executor. Note the flow in the comments: get the task, report progress, do the work, publish an artifact. **This file won't run yet.**

```
cd ../protocol
code stats_executor.py
```

<br>

2. Merge in the completed executor code, **save**, and close the diff tab. This agent deliberately doesn't use an LLM - it computes text statistics - so we can watch the *protocol* without waiting on a model.

```
code -d ../extra/stats_executor.txt stats_executor.py
```

<br>

3. In the merged code, find the three protocol moments every A2A agent goes through: `update_status(...TASK_STATE_WORKING...)` (progress), `add_artifact(...)` (the deliverable), and `update_status(...TASK_STATE_COMPLETED)` (done). Task states are the heartbeat of A2A - clients see each of these as it happens.

<br>

4. Now look at the server skeleton, which will publish this executor to the world:

```
code stats_server.py
```

<br>

5. Merge in the completed server code, **save**, and close the diff tab. There are two blocks: the **Agent Card** (an `AgentSkill` describing *what* it can do, and an `AgentCard` describing *how* to reach it - note the `supported_interfaces` entry saying "JSON-RPC at http://127.0.0.1:9999"), and the **server wiring** (the SDK's request handler plus two sets of routes: one that serves the card, one that serves the JSON-RPC methods).

```
code -d ../extra/stats_server.txt stats_server.py
```

<br>

6. Start the agent server. Leave it running in this terminal - we'll call this **Terminal 1 (server)** for the rest of this lab and Lab 4.

```
python stats_server.py
```

You should see uvicorn report: `Uvicorn running on http://127.0.0.1:9999`.

![A2A server running](./images/maa2a-3-1.png?raw=true "A2A server running")

<br>

7. Open a **new terminal** (click **+** in the terminal panel) - **Terminal 2 (client)**. Discover the agent the way any A2A client would - by fetching its Agent Card from the well-known URL:

```
cd protocol
curl -s http://127.0.0.1:9999/.well-known/agent-card.json | python3 -m json.tool
```

Look at the JSON: `name`, `version`, `capabilities.streaming`, the `skills` list with its `tags` and `examples`, and `supportedInterfaces` with `protocolBinding: "JSONRPC"`. This card is the *entire* public contract of the agent.

![Agent Card JSON](./images/maa2a-3-2.png?raw=true "Agent Card JSON")

<br>

8. Now send the agent a message using raw JSON-RPC 2.0 - no SDK, just curl. Note the `A2A-Version: 1.0` header and the v1.0 method name `SendMessage`:

```
curl -s -X POST http://127.0.0.1:9999/ \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
      "message": {
        "messageId": "msg-001",
        "role": "ROLE_USER",
        "parts": [ { "text": "Hello A2A world from curl" } ]
      }
    }
  }' | python3 -m json.tool
```

<br>

9. Examine the response. It's a complete **Task** object: an `id`, a `contextId`, a `status` of `TASK_STATE_COMPLETED`, an `artifacts` list holding our text statistics, and a `history` showing both our message and the agent's "Analyzing your text..." progress message. This is the A2A task lifecycle in one screenshot.

![Task response JSON](./images/maa2a-3-3.png?raw=true "Task response JSON")

<br>

10. Tasks persist after they finish. Copy the `id` value from the response in the previous step and fetch the task again with the `GetTask` method (replace `<TASK-ID>` with your actual id):

```
curl -s -X POST http://127.0.0.1:9999/ \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{"jsonrpc":"2.0","id":2,"method":"GetTask","params":{"id":"<TASK-ID>"}}' | python3 -m json.tool
```

<br>

11. One more experiment: run the same `SendMessage` curl from step 8 again, but **delete the `A2A-Version: 1.0` header line**. You'll get back a structured error: `A2A version '0.3' is not supported by this handler`. The server assumes the older 0.3 spec when the header is missing - version negotiation is built into the protocol.

<br>

12. **Leave the server running in Terminal 1** - Lab 4 talks to this same agent, this time with the real client SDK.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 4 - Speaking A2A: The Client Side, Streaming, and Task Retrieval**

**Purpose: To write an A2A client that discovers an agent from its card, sends it work, streams the task lifecycle events in real time, and retrieves the finished task afterward. (Estimated time: 10-12 minutes)**

**Steps:**

1. Your Text Stats server from Lab 3 should still be running in Terminal 1. Verify from **Terminal 2**:

```
curl -s http://127.0.0.1:9999/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
```

You should see `Text Stats Agent`. (If not, go to Terminal 1, `cd protocol`, and run `python stats_server.py` again.)

<br>

2. In Terminal 2, make sure you are in the **protocol** directory, and look at the client skeleton. The four numbered TODO sections mirror the lifecycle of every A2A client interaction: discover, connect, send/stream, retrieve. **This file won't run yet.**

```
code stats_client.py
```

<br>

3. Merge in the completed client code, **save**, and close the diff tab:

```
code -d ../extra/stats_client.txt stats_client.py
```

<br>

4. Walk through what you merged. **Discovery**: `A2ACardResolver` fetches the same card you curled in Lab 3. **Connect**: `create_client(card, ...)` reads the card's `supportedInterfaces` and picks the transport - our code never mentions JSON-RPC. **Send/stream**: `client.send_message(...)` returns an async stream of events. **Retrieve**: `client.get_task(GetTaskRequest(id=...))` fetches the task after the fact.

<br>

5. Run the client:

```
python stats_client.py
```

<br>

6. Look at the output. First, discovery: the agent's name, version, and skills - printed from the card, not hardcoded. Then the streamed events in order: `[task]` with the new task's id, `[status] WORKING`, `[artifact]` with the text statistics, and `[status] COMPLETED`. That's the same lifecycle you saw as one JSON blob in Lab 3, arriving event by event over Server-Sent Events.

![Client streaming output](./images/maa2a-4-1.png?raw=true "Client streaming output")

<br>

7. After the stream ends, the client fetches the task by id - you should see `final state: COMPLETED`, one artifact, and a two-message history. Anything that holds the task id can check on this task later - that's what makes long-running agent work possible.

<br>

8. Edit the message the client sends (find the `new_text_message(` call in step 3's merged code) and change the sentence to anything you like. Save, and run the client again - the artifact statistics should change to match your text.

```
python stats_client.py
```

<br>

9. Notice the `streaming=True` in `ClientConfig`. Set it to `False`, save, and run the client once more. The task and artifact still arrive (the SDK falls back to a single request/response) but there are no incremental `WORKING` events to print - the result comes back in one shot. Set it back to `True` and save when you're done experimenting.

<br>

10. We're done with the Text Stats agent. Go to **Terminal 1** and stop the server with **CTRL+C**. (Lab 5 starts fresh servers on different ports.)

<br>

11. Think about what you did NOT have to write in this lab: no HTTP routes, no JSON-RPC envelopes, no SSE parsing, no task storage. The card told the client everything it needed. In Lab 5, that's what lets one client drive agents from *different frameworks* without caring what's inside them.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 5 - The Payoff: A Cross-Framework Agent Network**

**Purpose: To connect a LangGraph agent and a CrewAI agent into one network over A2A, then build an orchestrator that discovers them by capability and chains their work - without knowing which framework is behind either one. (Estimated time: 12 minutes)**

**Steps:**

1. Change into the network directory and look at the first provided server - our Lab 1-style LangGraph research agent, now wrapped in an A2A executor. **This file is complete - no merge needed.**

```
cd ../network
code langgraph_server.py
```

Find the `LangGraphResearchExecutor` class: inside `execute()`, it calls `research_agent.invoke(...)` and publishes the agent's answer as an A2A artifact. The card at the bottom advertises the skill with tags `["research", "companies", "facts"]` on port 10001.

<br>

2. Now look at the second provided server - a CrewAI writing crew behind the *exact same* protocol plumbing, on port 10002, with tags `["writing", "summarize", "briefs"]`. Compare its `execute()` method to the LangGraph one: different framework call inside, identical A2A protocol outside.

```
code crewai_server.py
```

<br>

3. Start both agent servers in the background from this one terminal:

```
python langgraph_server.py < /dev/null > /tmp/lg.log 2>&1 &
python crewai_server.py < /dev/null > /tmp/crew.log 2>&1 &
sleep 12
```

**The `sleep` gives the servers time to import their frameworks and start up (about 10-15 seconds). The `< /dev/null` matters: after a crew finishes, CrewAI prints an interactive prompt asking whether you want to view execution traces. A background job that tries to read your keyboard gets suspended by the shell, which would silently kill the CrewAI agent after its first request.**

<br>

4. Verify both agents are up and advertising their cards:

```
curl -s http://127.0.0.1:10001/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
curl -s http://127.0.0.1:10002/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
```

You should see `Company Research Agent (LangGraph)` and `Executive Brief Writer (CrewAI)`.

![Both agent cards live](./images/maa2a-5-1.png?raw=true "Both agent cards live")

<br>

5. Open the orchestrator skeleton. Read `main()` first - it's already written, and it tells the story: discover the agents, find one by the `research` tag and one by the `writing` tag, delegate to each in turn, print the final brief. The three helper functions are the TODOs. **This file won't run yet.**

```
code orchestrator.py
```

<br>

6. Merge in the three helper functions, **save**, and close the diff tab: `discover_agents` (fetch every card), `find_agent_with_tag` (capability matching on skill tags), and `delegate` (create a client from a card, send the message, collect artifact text from the stream).

```
code -d ../extra/orchestrator.txt orchestrator.py
```

<br>

7. Check the orchestrator's imports for a moment: `a2a.client`, `httpx`, `asyncio` - and **no LangGraph, no CrewAI**. The orchestrator is pure protocol.

<br>

8. Run the network:

```
python orchestrator.py
```

**Both delegations call an LLM: about 2 seconds total on Groq, or 1-3 minutes on the local model. Watch the progress as it prints.**

<br>

9. Watch the sequence: the roster of discovered agents with their tags, then research delegated to the LangGraph agent (facts about Globex come back), then those facts sent on to the CrewAI agent, and finally the **EXECUTIVE BRIEF** - researched by one framework, written by another, coordinated by neither.

![Cross-framework orchestration output](./images/maa2a-5-2.png?raw=true "Cross-framework orchestration output")

<br>

10. This routing was *declarative*: the orchestrator picked agents by skill tags from their cards. Swap either server for any other A2A agent with matching tags - written in Google ADK, Microsoft Agent Framework, or anything else - and the orchestrator runs unchanged. That is the entire point of the protocol.

<br>

11. Clean up the background servers:

```
kill %1 %2
```

<br>

12. (Optional - if time permits) Add a third URL to `AGENT_URLS` in the orchestrator pointing at a port with no server (e.g. `http://127.0.0.1:10003`) and run it to see how discovery fails. Production networks wrap discovery in retries and health checks - one of the operational concerns we cover in the closing slides. Remove the URL again when done.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

<p align="center">
<b>THANKS FOR ATTENDING! PLEASE FILL OUT THE SURVEY!</b>
</p>

<p align="center">
<b>For educational use only by the attendees of our workshops.</b>
</p>
<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>
