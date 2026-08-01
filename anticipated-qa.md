# Anticipated Q&A: Multi-Agent AI Systems & the A2A Protocol
**Generated**: 2026-07-31
**Course version**: 1.0

## Section: Multi-Agent Foundations (Labs 1-2)

**Q: When should I use multiple agents instead of one agent with more tools?**
A: Split when you can name the specialization you need - a distinct persona, toolset, or model. One agent with 20+ tools degrades (wrong-tool picks, context bloat); one agent per concern stays small and testable. But every hop is an extra LLM call, so don't split "just because" - start with one agent and let pain drive the split.

**Q: Is the supervisor pattern the same as LangGraph's old `langgraph-supervisor` library?**
A: Same idea, newer mechanics. The `langgraph-supervisor` add-on package is effectively frozen; the LangChain 1.x docs now recommend building the supervisor directly with tool-calling - wrap each specialist agent in a `@tool` function, exactly what Lab 1 does.

**Q: Why does the supervisor sometimes route wrong or skip a tool call?**
A: We're running a 3B-parameter model locally. Small models occasionally emit spurious or malformed tool calls - a known limitation, not a bug in the lab. Re-run once; with a Groq key (larger model) routing is much more reliable. Production systems add routing validation and retries for exactly this reason.

**Q: What's the real difference between LangGraph and CrewAI - which should my team pick?**
A: Control vs. convention. LangGraph: you wire the control flow explicitly (graphs, edges, state) - maximum control, more code. CrewAI: you declare roles, tasks, and a process type - faster to stand up, less control over flow. And after this workshop, remember the stakes are lower than they look: behind an A2A card, the framework is a per-agent implementation detail.

**Q: What does CrewAI's hierarchical process do that we didn't use?**
A: `Process.hierarchical` adds a manager agent that plans, orders, and delegates the tasks dynamically instead of running them in list order. It needs a strong manager model (it must produce well-formed delegation calls repeatedly), which is why the lab sticks to sequential on a local 3B model.

**Q: How do agents share memory in these frameworks?**
A: In LangGraph, shared state (the message list, plus any typed fields you add) flows along graph edges and can be checkpointed. In CrewAI, `context=[task]` pipes one task's output into another's prompt, and crews can add memory features. Note what's *not* shared: each specialist's internal tool calls stay private - which becomes a formal principle (opacity) in A2A.

## Section: The A2A Protocol (Labs 3-4)

**Q: How is A2A different from MCP? Do I need both?**
A: MCP connects an agent to its *tools* (vertical); A2A connects agents to *each other* (horizontal). They're complementary - the official docs' example: a mechanic-agent uses MCP for its diagnostic scanner and A2A to talk to the customer's agent and the parts-supplier's agent. A complete system typically uses both.

**Q: Is A2A a Google product? Do I risk vendor lock-in?**
A: It started at Google (April 2025) but was donated to the Linux Foundation in June 2025 and now has 150+ member organizations - AWS, Microsoft, IBM, Salesforce, SAP, ServiceNow among them. The v1.0 spec (March 2026) is stable and vendor-neutral, with production support in Azure AI Foundry, Copilot Studio, and AWS Bedrock AgentCore.

**Q: Why did my curl call fail without the A2A-Version header?**
A: Version negotiation. A v1.0 server assumes the older 0.3 spec when the header is absent and returns a structured VERSION_NOT_SUPPORTED error. Always send `A2A-Version: 1.0` (SDK clients do it for you). You hit this deliberately in Lab 3 step 11.

**Q: The method names I've seen elsewhere are `message/send` and `tasks/get` - why does the lab use `SendMessage` and `GetTask`?**
A: Those slash-style names are the v0.3 binding. v1.0 unified JSON-RPC method names with the gRPC service as PascalCase (`SendMessage`, `GetTask`, `ListTasks`...). Servers can enable a 0.3 compat mode for older clients, but new code should use v1.0 names.

**Q: What changed in the Agent Card between the versions people blog about and v1.0?**
A: Two big ones. The well-known path became `/.well-known/agent-card.json` (was `agent.json` before v0.3). And v1.0 replaced the flat `url`/`preferredTransport` fields with a `supportedInterfaces[]` list (url + protocolBinding + optional tenant), plus added `signatures[]` for signed cards.

**Q: What are the task states, and what are input-required and auth-required for?**
A: v1.0 states: SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED, REJECTED, INPUT_REQUIRED, AUTH_REQUIRED. The last two make A2A genuinely agentic: INPUT_REQUIRED pauses the task to ask the caller for more information (multi-turn); AUTH_REQUIRED pauses for credentials or human approval - escalation built into the wire protocol.

**Q: When would I choose gRPC or REST over JSON-RPC?**
A: They're three bindings of one protobuf-canonical data model, so it's an ops decision, not a features one. JSON-RPC is simplest (what the labs use); gRPC suits high-throughput internal backends; HTTP+JSON/REST fits plain web stacks. The card's `supportedInterfaces` advertises what a server offers, and `create_client` picks automatically.

**Q: Why did my client's message get rejected with "Message must be from a user"?**
A: The SDK's `new_text_message()` helper defaults to `ROLE_AGENT`. A client sending work must mark its message `role=Role.ROLE_USER`. It's the most common first-run error in Lab 4's code - the completed version passes the role explicitly.

**Q: Do tasks survive a server restart?**
A: With the lab's `InMemoryTaskStore`, no - it's for development. The SDK ships database-backed task stores (PostgreSQL, MySQL, SQLite extras) for persistence in production.

**Q: How do I secure an A2A agent in production?**
A: Standard web auth, declared in the card's `securitySchemes`: OAuth2 (v1.0 modernized the flows - implicit and password grants removed; device-code and PKCE added), API keys, OIDC, or mTLS - all over HTTPS. v1.0 adds signed cards (JWS) so callers can verify a card wasn't forged, and a `tenant` field on interfaces for multi-tenant deployments.

## Section: Cross-Framework Networks (Lab 5)

**Q: The orchestrator routes by skill tags - isn't that fragile?**
A: Tag matching is deliberately simple for the lab. Production options: richer capability matching on skill descriptions/examples (often with an LLM doing the matching), curated internal registries, or letting a planning agent choose. The key point stands: the card gives you machine-readable capability data to route on.

**Q: How would I add a Google ADK or Microsoft Agent Framework agent to the Lab 5 network?**
A: ADK: `to_a2a(root_agent, port=...)` serves any ADK agent with an auto-generated card - point the orchestrator at its URL and give its skills matching tags. MAF: the `agent-framework-a2a` package exposes/consumes A2A agents (`A2AAgent`). Neither requires touching the orchestrator - that's the whole point.

**Q: Why not just import both frameworks into one Python process instead of running servers?**
A: For two frameworks you control on one machine, you could. But that breaks down the moment agents are owned by different teams, deployed on different schedules, written in different languages, or living in different companies. A2A gives you process, language, and organizational independence - plus discovery, streaming, auth, and task persistence you'd otherwise rebuild.

**Q: What happens if one agent in the network is down?**
A: Discovery or delegation fails with a connection error (the optional Lab 5 step demonstrates it). Production orchestrators wrap discovery/delegation in retries with backoff, health checks, timeouts, and fallbacks to alternate agents with the same capability tags.

**Q: Can A2A agents call each other recursively - agent A delegates to B, which delegates to C?**
A: Yes - that's normal and powerful (B is a client to C while being a server to A). It's also why production systems enforce delegation depth caps and deadlines, per the production section: uncapped recursion is how you get runaway cost and circular waits.

## Section: Production Concerns

**Q: How do I actually enforce a token budget across agents I don't own?**
A: Propagate a budget in task metadata and have each agent decrement and refuse work past the cap; meter at the A2A boundary (it's the natural choke point); and add circuit breakers on cumulative spend in the orchestrator. For third-party agents you can't trust to honor metadata, enforce on your side: cap what you send, time-box the task, and cancel past deadline.

**Q: What observability tooling should we start with?**
A: OpenTelemetry is the emerging standard - the `a2a-sdk` has a `[telemetry]` extra, and LangSmith/Langfuse/AgentOps cover the framework layer. Minimum bar regardless of tooling: log A2A task ids and context ids at every boundary so you can stitch multi-hop journeys together.

**Q: How do I test a multi-agent system?**
A: Layer it: unit-test tools (deterministic), test each specialist agent against fixture prompts, then integration-test the network with recorded/mocked A2A responses. The A2A boundary is a gift for testing - you can stand in a fake agent that returns canned artifacts without touching the real one.

## General / Cross-Cutting

**Q: Where do the 57% / 16% / 81% numbers come from?**
A: Anthropic's "2026 State of AI Agents Report" (published December 2025, with research firm Material; 500+ US technical leaders surveyed in late 2025): 57% use agents for multi-stage workflows, 16% have cross-functional agents, 81% plan to move beyond simple task automation in 2026.

**Q: Why are lab responses so slow?**
A: The local llama3.2:3b runs on a 4-core codespace with no GPU - expect 30 seconds to 2+ minutes per LLM call, and 1-3 minutes for the first call while the model loads into memory. A free Groq API key (`export GROQ_API_KEY=...`) switches every lab to fast hosted models automatically.

**Q: My A2A server says "address already in use."**
A: A server from a previous lab is still running. `kill $(lsof -t -i:9999)` (substitute the port). In Lab 5, `kill %1 %2` cleans up the background servers.

**Q: CrewAI printed telemetry/tracing warnings - is something broken?**
A: No. CrewAI phones home telemetry by default; in restricted networks that produces harmless warnings. The devcontainer sets `CREWAI_DISABLE_TELEMETRY=true` to quiet them.

**Q: Whatever happened to AutoGen? Should I still learn it?**
A: AutoGen is officially in maintenance mode (community-managed, no new features). Its ideas - especially conversational group chat - live on in Microsoft Agent Framework (1.0 GA, April 2026), which merged AutoGen and Semantic Kernel. Learn the patterns; build on MAF.

**Q: Does A2A support agents written in languages other than Python?**
A: Yes - that's much of the point. Official SDKs exist for Python, JavaScript/TypeScript, Java, Go, and .NET, and any HTTP-capable language can implement the protocol directly. Two agents never need to share a language, only the wire format.

**Q: Is there a public registry where I can discover other companies' agents?**
A: Not standardized yet - the v1.0 spec deliberately doesn't prescribe a registry API. Today, discovery is well-known URLs plus curated (usually internal) catalogs. Watch this space; registries plus signed cards are where the ecosystem is clearly heading.

**Q: Can I use these labs with a different local model?**
A: Yes - set `OLLAMA_MODEL` to any tool-capable Ollama model (e.g. a larger llama or qwen tag) before running the labs, and the code picks it up. Bigger models are more reliable at tool calling but slower on codespace CPUs; 3B is the pragmatic floor.

## Appendix: Timing & Break Plan (3-hour run)

| Block | Content | Minutes |
|---|---|---|
| Open + setup | Slides 1-4, codespaces starting | 15 |
| Why multi-agent + patterns | Slides 5-12 | 20 |
| LangGraph + **Lab 1** | Slides 13-17 + lab | 22 |
| CrewAI + **Lab 2** | Slides 18-21 + lab | 20 |
| **Break** | - | 10 |
| A2A fundamentals + **Lab 3** | Slides 22-32 + lab | 30 |
| A2A clients + **Lab 4** | Slides 33-38 + lab | 25 |
| Cross-framework + **Lab 5** | Slides 39-44 + lab | 25 |
| Production + wrap | Slides 45-52 | 13 |

Buffer strategy: Lab 5's LLM wait is the natural absorber - discuss production concerns during the run if ahead, trim slide 49 if behind.
