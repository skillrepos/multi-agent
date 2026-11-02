# Multi-Agent AI Systems & the A2A Protocol
## Hands-on labs
## Revision 1.5 - 10/30/26

**Startup: If you haven't already, follow the steps in the README to start your codespace. Wait until you see "Ollama is ready with model llama3.2:3b" in the terminal before starting Lab 1 (setup takes 3-5 minutes).**

**Notes:**
1. To copy and paste in the codespace, you may need to use keyboard commands - CTRL+C and CTRL+V (CMD+C and CMD+V on Mac).
2. Some lab files are *skeletons* - they have TODO markers where code is missing. You'll complete them by merging in code from the completed versions in the **extra** directory using VS Code's diff view (`code -d`). In the diff view, hover over the middle bar between the two files and click the **arrow** next to each highlighted block to copy it into your file. When all blocks are merged, **save the file** (CTRL+S / CMD+S) and close the diff tab.
3. **Recommended: a free Groq API key.** Labs 1, 2, and 5 call an AI model. If you set up a Groq key (README steps 4 and 5), they use it automatically in every terminal and answer in **seconds**. Without one they use the local llama3.2:3b model, which needs no account but takes **30 seconds to 2+ minutes** per run and often gets details wrong (it may pass a sloppy argument to a tool, or ignore what the tool returned). **The lab steps are identical either way.** To add a key later, run `source scripts/setup-key.sh` in any terminal.
4. When you need a second terminal, click the **+** icon in the upper right of the terminal panel (or use CTRL+SHIFT+`). New terminals open at the repo root, so `cd` to the right directory.
5. **Not using the codespace?** If you set up your own machine with one of the manual setup guides, read the *What looks different* section of that guide first - it covers what to use instead of `code -d` and what you need to do in each new terminal.

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

2. Scroll through the file. Already there: a `get_model()` function that picks Groq or local Ollama, and two plain tools - `lookup_company` (a small private knowledge base) and `calculate`. *Missing* (the TODO sections) are the agents themselves. (`team_trace.py` next to it just prints the trace - no need to open it.) Close the file. **This file won't run yet.**

<br>

3. Open a diff view against the completed version and merge in each block of missing code. There are three blocks: the **specialist agents** (researcher + analyst, each a full agent with its own tools), the **delegation tools** (`research` and `analyze` - each wraps a specialist so the supervisor can call it like any other tool), and the **supervisor** agent itself. Click the arrow next to each highlighted block to merge it, then **save** and close the diff tab.

```
code -d ../extra/supervisor_team.txt supervisor_team.py
```

![Merging code for the supervisor team](./images/maa2a-1-1.png?raw=true "Merging code for the supervisor team")

<br>

4. Look at the merged code for the delegation tools. This is the heart of the supervisor pattern: `research` is just a function with the `@tool` decorator, but inside it *invokes a complete agent* and returns that agent's final message. The supervisor can't tell the difference between a simple tool and a whole team member.

<br>

5. Run the team and press **Enter** to use the example question: *"Compare Acme Corp and Globex: which one brings in more revenue per employee, and by how much?"* The supervisor has to plan: get each company's figures from the researcher, then hand the numbers to the analyst.

```
python supervisor_team.py
```

**A few seconds on Groq; a minute or two on the local model.**

<br>

6. Look at the **MESSAGE TRACE**. The SUPERVISOR delegates to the RESEARCHER (usually once per company); the indented lines are the researcher's own work - it uses `lookup_company`, then reports back. Then the SUPERVISOR sends the numbers to the ANALYST, which uses `calculate`.

<!-- SCREENSHOT TO RETAKE: images/maa2a-1-2.png - new MESSAGE TRACE format (example question, Groq) -->

<br>

7. Check the two summary lines under the trace: the supervisor called only `research` and `analyze`; only the specialists used `lookup_company` and `calculate`. The supervisor routes - it never touches the low-level tools. Then read the **FINAL ANSWER**.

**Focus on the routing, not the facts.** On Groq the answer should be right: Globex earns about $175,926 per employee versus Acme Corp's $150,000. The analyst used a tool for that division because models are unreliable at exact arithmetic. The local 3B model often gets details wrong, or skips a tool and makes something up (the trace then says the specialist *answered WITHOUT using any of its tools*) - a model-size limit, and exactly why production systems validate what delegated agents return.

<br>

8. Ask a different question - typed at the prompt, or on the command line:

```
python supervisor_team.py "Which grew revenue faster from 2022 to 2025, Acme Corp or Initech? Give each one's yearly growth rate."
```

The researcher should look up both companies, and the analyst should calculate a compound growth rate for each (on Groq: about 14.5% a year for Acme Corp, 33.4% for Initech). **If the local model mis-routes a step, just run it again.**

<br>

9. Try a question that needs only **one** specialist:

```
python supervisor_team.py "What does Initech make, and where is it based?"
```

The trace should show only the RESEARCHER - no math, no analyst. (The knowledge base knows Acme Corp, Globex, and Initech - try your own questions.)

<br>

10. Notice what this pattern gives us: each specialist has a narrow job and a small toolset (easier to test, less prompt confusion), and the supervisor only makes *routing* decisions. The tradeoff: every hop is another LLM call, so latency and cost grow with team size. In Lab 2, we'll see a different framework's take on the same idea.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 2 - Role-Based Crews with Tools (CrewAI)**

**Purpose: To build a CrewAI crew whose agents use tools - an analyst that decides what to look up and calculate, and a writer that checks the house style guide before writing - while CrewAI moves the work between them. (Estimated time: 10-12 minutes)**

**Steps:**

1. You should still be in the **agents** directory. Look at the skeleton for our crew. At the top are four tools, each wrapping a function in `company_data.py`: company profiles, news, a calculator, and a house style guide. The TODO sections are for the agents, tasks, and crew. **This file won't run yet.**

```
code content_crew.py
```

<br>

2. Merge in the completed code. There are three blocks: the **agents** (a Company Analyst and a Business Writer, each with a role, goal, backstory, and its own `tools` list), the **tasks** (each with a description, an `expected_output`, and an assigned agent), and the **crew** (agents + tasks + `Process.sequential`). Merge each block, **save**, and close the diff tab.

```
code -d ../extra/content_crew.txt content_crew.py
```

<br>

3. Look at the merged agents. The `tools=[...]` list is what each agent *may* use - which tools it calls, and how many times, is up to the agent. Then find `context=[analysis_task]` on the writing task: that's what pipes the analyst's findings into the writer's prompt.

<br>

4. Run the crew. Press **Enter** at the prompt to use the example request: *"Brief our board on Initech as a possible acquisition target."*

```
python content_crew.py
```

**Several model calls happen here: under a minute on Groq; a few minutes on the local model. At the end CrewAI prints a "Tracing Status" box saying tracing is disabled - that's informational, nothing to do.**

<br>

5. Watch the **Company Analyst** work. CrewAI shows a *Tool Execution* box for each tool the analyst chooses - expect `lookup_company` and `get_news` for Initech, and `calculate` for a figure like yearly revenue growth. Then it prints its bullet list.

<!-- SCREENSHOT TO RETAKE: images/maa2a-2-1.png - analyst's tool executions (Groq) -->

<br>

6. Then the **Business Writer** runs. Its first move is a tool call - `get_style_guide` for the *board* audience - and then it writes using the analyst's bullets.

<br>

7. Read the **FINAL OUTPUT**. It should follow the board style: a one-sentence recommendation, then at most three bullets with numbers. (On the local model, an agent may skip a tool or ignore the style - a small-model limit, not a flaw in the crew.)

<br>

8. Now give the crew a different request and audience:

```
python content_crew.py "Write an investor note comparing Acme Corp and Globex."
```

<br>

9. Compare the tool calls with the first run. The analyst should look up *both* companies this time, and the writer should fetch the *investor* style instead. Same code, different choices - that's the agentic part. What stays fixed is the *order* of the tasks: `Process.sequential` always runs the analysis before the writing.

<br>

10. Compare this lab to Lab 1. LangGraph gave us *explicit* control flow - we wrote the delegation tools ourselves. CrewAI gave us *declarative* collaboration - we described who the agents are, what tools they have, and what the tasks produce. CrewAI's other process type, `Process.hierarchical`, adds a manager agent that decides the task order too - it needs a stronger model than our local 3B, which is why we're using sequential today.

<br>

11. Both labs so far share one big limitation: everything lives in **one process, one framework, one codebase**. The analyst can't be reused by a team written in another framework, and nothing outside this script can even find out these agents exist. That's the problem the A2A protocol solves - and it's where we go next.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 3 - Your First A2A Agent: Cards, Servers, and Tasks**

**Purpose: To serve a real tool-using agent over A2A (spec v1.0) - an AgentExecutor that reports each step the agent takes as a task update, an Agent Card that advertises it, and a JSON-RPC endpoint we can call with nothing but curl. (Estimated time: 10-12 minutes)**

**Steps:**

1. Change into the protocol directory and look at the agent we'll serve. It's a LangGraph agent like the ones in Lab 1, with three tools: `lookup_company`, `get_news`, and `calculate`. Notice there's nothing about A2A in this file. **It's complete - no merge needed.**

```
cd ../protocol
code analyst_agent.py
```

<br>

2. Now look at the skeleton for the executor - the bridge between the agent and the protocol. It already gets (or creates) the task; the TODO is everything after that. **This file won't run yet.**

```
code analyst_executor.py
```

<br>

3. Merge in the completed executor code, **save**, and close the diff tab.

```
code -d ../extra/analyst_executor.txt analyst_executor.py
```

<br>

4. Read the merged code. It reports `TASK_STATE_WORKING`, then runs the agent step by step with `astream`. Every tool call the agent decides to make becomes another WORKING update with a message like `Calling get_news(Globex)`. If the agent errors, the task ends as `TASK_STATE_FAILED`. Otherwise the answer is published with `add_artifact(...)` and the task is marked `TASK_STATE_COMPLETED`.

<br>

5. Merge the completed server code, **save**, and close the diff tab. There are two blocks: the **Agent Card** (an `AgentSkill` describing *what* the agent can do, and an `AgentCard` describing *how* to reach it - note the `supported_interfaces` entry saying "JSON-RPC at http://127.0.0.1:9999"), and the **server wiring** (the SDK's request handler plus routes for the card and for the JSON-RPC methods).

```
code -d ../extra/analyst_server.txt analyst_server.py
```

<br>

6. Start the agent server. Leave it running in this terminal - we'll call this **Terminal 1 (server)** for the rest of this lab and Lab 4.

```
python analyst_server.py
```

You should see uvicorn report: `Uvicorn running on http://127.0.0.1:9999`.

<!-- SCREENSHOT TO RETAKE: images/maa2a-3-1.png - analyst server running -->

<br>

7. Open a **new terminal** (click **+** in the terminal panel) - **Terminal 2 (client)**. Discover the agent the way any A2A client would - by fetching its Agent Card from the well-known URL:

```
cd protocol
curl -s http://127.0.0.1:9999/.well-known/agent-card.json | python3 -m json.tool
```

Look at the JSON: `name`, `version`, `capabilities.streaming`, the `skills` list with its `tags` and `examples`, and `supportedInterfaces` with `protocolBinding: "JSONRPC"`. This card is the *entire* public contract of the agent.

<!-- SCREENSHOT TO RETAKE: images/maa2a-3-2.png - Company Analyst Agent card JSON -->

<br>

8. Now send the agent a question using raw JSON-RPC 2.0 - no SDK, just curl. Note the `A2A-Version: 1.0` header and the v1.0 method name `SendMessage`. **curl waits while the agent works: a few seconds on Groq, up to a couple of minutes on the local model.**

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
        "parts": [ { "text": "What is the revenue per employee at Globex?" } ]
      }
    }
  }' | python3 -m json.tool
```

<br>

9. Examine the response. It's a complete **Task** object: an `id`, a `status` of `TASK_STATE_COMPLETED`, an `artifacts` list holding the agent's answer, and a `history`. Read the history: your question, then one progress message per tool the agent chose - for example `Calling lookup_company(Globex)` and `Calling calculate(950000000 / 5400)`. The task is a record of what the agent did.

<!-- SCREENSHOT TO RETAKE: images/maa2a-3-3.png - Task response with history of tool steps -->

<br>

10. Tasks persist after they finish. Copy the `id` value from the response and fetch the task again with the `GetTask` method (replace `<TASK-ID>` with your actual id):

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

**Purpose: To write an A2A client that discovers an agent from its card, sends it a question, streams the agent's progress live as it works, and retrieves the finished task afterward. (Estimated time: 10-12 minutes)**

**Steps:**

1. Your Company Analyst server from Lab 3 should still be running in Terminal 1. Verify from **Terminal 2**:

```
curl -s http://127.0.0.1:9999/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
```

You should see `Company Analyst Agent`. (If not, go to Terminal 1, `cd protocol`, and run `python analyst_server.py` again.)

<br>

2. In Terminal 2, make sure you are in the **protocol** directory, and look at the client skeleton. The four numbered TODO sections mirror the lifecycle of every A2A client interaction: discover, connect, send/stream, retrieve. **This file won't run yet.**

```
code analyst_client.py
```

<br>

3. Merge in the completed client code, **save**, and close the diff tab:

```
code -d ../extra/analyst_client.txt analyst_client.py
```

<br>

4. Walk through what you merged. **Discovery**: `A2ACardResolver` fetches the same card you curled in Lab 3. **Connect**: `create_client(card, ...)` reads the card's `supportedInterfaces` and picks the transport - our code never mentions JSON-RPC. **Send/stream**: `client.send_message(...)` returns an async stream of events; each status update can carry a progress message. **Retrieve**: `client.get_task(GetTaskRequest(id=...))` fetches the task after the fact.

<br>

5. Run the client. Press **Enter** at the prompt to use the example question: *"How much revenue per employee does Initech bring in, and what's its latest news?"*

```
python analyst_client.py
```

<br>

6. Watch the output. First, discovery: the agent's name and skill, printed from the card. Then the events stream in **as the agent works**: `[task]`, `[status] WORKING Planning how to answer...`, then one WORKING update for each tool the agent decides to call (`lookup_company(Initech)`, `get_news(Initech)`, `calculate(95000000 / 350)`), then `[artifact]` with the answer and `[status] COMPLETED`. It's the same history you saw as one JSON blob in Lab 3 - now arriving live over Server-Sent Events.

<!-- SCREENSHOT TO RETAKE: images/maa2a-4-1.png - streamed tool-step updates (Groq) -->

<br>

7. After the stream ends, the client fetches the task by id: `final state: COMPLETED`, one artifact, and a history with your question plus each progress message. Anything that holds the task id can check on this task later - that's what makes long-running agent work possible.

<br>

8. Ask a question of your own on the command line:

```
python analyst_client.py "What is the latest news about Acme Corp?"
```

Compare the WORKING updates with step 6. There's no math in this question, so the agent shouldn't call `calculate`. A different question gives different steps - that's what makes this an agent rather than a script.

<br>

9. Now find `streaming=True` in `ClientConfig`, set it to `False`, save, and run the step 8 command again. You wait with no progress at all, then get only the finished task. For agents doing multi-step work, that live progress is why streaming matters. Set it back to `True` and save.

<br>

10. We're done with this agent. Go to **Terminal 1** and stop the server with **CTRL+C**. (Lab 5 starts fresh servers on different ports.)

<br>

11. Think about what you did NOT have to write in this lab: no HTTP routes, no JSON-RPC envelopes, no SSE parsing, no task storage. The card told the client everything it needed. In Lab 5, that's what lets one orchestrator drive agents from *different frameworks* without caring what's inside them.

<p align="center">
**[END OF LAB]**
</p>
<br><br>

**Lab 5 - The Payoff: A Cross-Framework Agent Network**

**Purpose: To connect a LangGraph agent and a CrewAI agent into one network over A2A, then build an orchestrator whose AI model reads their Agent Cards and decides which agents to call - without knowing which framework is behind either one. (Estimated time: 12 minutes)**

**Steps:**

1. Change into the network directory and look at the first provided server: a research agent like Lab 1's, built with LangGraph, with two tools (`lookup_company` and `get_news`) and an executor that reports each tool call just like Lab 3's. Its card advertises the skill `company_research` on port 10001. **This file is complete - no merge needed.**

```
cd ../network
code langgraph_server.py
```

<br>

2. Now look at the second provided server: Lab 2's Business Writer, built with CrewAI and still using its `get_style_guide` tool, behind the *exact same* protocol on port 10002. Its card advertises the skill `business_writing`. Different framework inside, identical A2A outside.

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

**The `sleep` gives the servers time to import their frameworks and start up. The `< /dev/null` matters: CrewAI can ask an interactive question after a run, and a background job that tries to read your keyboard gets suspended by the shell - which would silently stop the CrewAI agent after its first request.**

<br>

4. Verify both agents are up and advertising their cards:

```
curl -s http://127.0.0.1:10001/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
curl -s http://127.0.0.1:10002/.well-known/agent-card.json | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])"
```

You should see `Company Research Agent (LangGraph)` and `Business Writer (CrewAI)`.

<!-- SCREENSHOT TO RETAKE: images/maa2a-5-1.png - both agent cards live -->

<br>

5. Open the orchestrator skeleton and read `main()` first - it's already written. It discovers the agents and turns their cards into tools, then loops: ask the model what to do next, run each tool call as an A2A delegation, and stop when the model replies with the finished document. The three helpers are the TODOs. **This file won't run yet.**

```
code orchestrator.py
```

<br>

6. Merge in the three helper functions, **save**, and close the diff tab: `discover_agents` (fetch every card), `cards_to_tools` (each skill on a card becomes a tool whose description comes straight from the card - this is how the model "reads" the cards), and `delegate` (create a client from a card, send the message, collect the artifact text).

```
code -d ../extra/orchestrator.txt orchestrator.py
```

<br>

7. Check the orchestrator's imports: `a2a.client`, `httpx`, and `llm.py`, a helper that makes one plain web request to the model. **No LangGraph, no CrewAI, no agent framework at all.** The orchestrator is pure protocol plus a model.

<br>

8. Run the network. Press **Enter** at the prompt to use the example request: *"Write a short brief for our board on Globex as a possible robotics supplier, including any recent news they should know about."*

```
python orchestrator.py
```

**Seconds on Groq; several minutes on the local model. On the local model the orchestrator may skip an agent or answer directly - small models plan poorly, which is why Groq is recommended.**

<br>

9. Watch the model's decisions. After the roster of agents, you'll see `ORCHESTRATOR -> Company Research Agent (LangGraph)` with a request the model wrote itself, the facts that come back, then `ORCHESTRATOR -> Business Writer (CrewAI)` with the audience and those facts, and finally the **FINAL RESULT**. Nobody coded that order - the model planned it from the cards.

<!-- SCREENSHOT TO RETAKE: images/maa2a-5-2.png - orchestrator delegations and final result (Groq) -->

<br>

10. Give the network a different request:

```
python orchestrator.py "Prepare an investor note comparing Acme Corp and Initech."
```

The model may call the research agent twice - once per company - before the writer. Swap either server for any A2A agent whose card describes a matching skill - built with Google ADK, Microsoft Agent Framework, or anything else - and the orchestrator runs unchanged. That's the point of the protocol.

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
