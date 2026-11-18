# LinkRight, Architecture Decisions

Draft v0.1. Date 2026-06-05. Companion to `LinkRight-Plugin-Roadmap.md`. This holds the decisions Satvik asked me to make and the architect level reasoning behind them, especially the cost question.

---

## 1. The big one, execution model and cost

Satvik likes the BMAD style content engine design, config driven workflows, agents, evals, templates, single source of truth. The worry is cost, tokens and time. Here is the honest architect read.

### The hidden truth about BMAD

BMAD bundles two separate things that people treat as one.

One, the design structure. Workflows, agents as roles, evals as gates, templates as contracts, one memory as source of truth. This is excellent and worth keeping.

Two, the execution model. How many actual LLM calls or subagents you spawn to run it. This is where cost lives, and it is a separate choice.

You can keep the structure and make the execution cheap. Your own CLI already proves it. Most of its agents are deterministic code, width scripts, scorecards, fabrication guards, validators, and it calls an LLM only at the few steps that truly need reasoning. That is far cheaper and more reliable than spawning an LLM agent for every role.

### Real cost data, measured today

A deep research subagent that reads a codebase cost about 95,000 to 131,000 tokens and took about 11 minutes each. A focused generation subagent is lighter, but still tens of thousands of tokens per call.

So if every agent in a workflow is its own LLM subagent, a single daily post or resume run could be 300,000 to 700,000 tokens and 20 to 50 minutes. For a daily task, across users, that is too expensive and too slow.

### The four execution models, pros and cons

| Model | What it is | Tokens per run | Speed | Quality | Best for |
|---|---|---|---|---|---|
| Full swarm | Every agent is its own LLM subagent | 300k to 700k | Slow, 20 to 50 min | High by isolation, but slow feedback | One off high stakes, not daily |
| Single context conductor | One LLM plays all roles in sequence | 80k to 150k | Few minutes | Good, but long chains bloat and skip checks | Quick runs, lower stakes |
| Deterministic first, the CLI model | Code does every check and score, LLM only generates and judges | 20k to 80k | 1 to 4 min | High and consistent, testable | Daily product at scale |
| Agent harness, pi.dev or hermes | One capable agent with a tool belt and a planner loop, calling deterministic tools | 50k to 200k, variable | Variable | High for novel and interactive tasks | The CLI, interactive and autonomous use |

### Recommendation

Keep BMAD as the design language. Keep workflows, evals, templates, and the one memory. You love it and it is genuinely good.

Implement it the CLI way, deterministic first. Every hard gate becomes code, banned words, punctuation, hook signature, metric consistency, width fit, contrast, all of these are free deterministic checks, not LLM calls. Reserve LLM calls for the handful of steps that actually need reasoning, the draft, the voice score, one revision, the final judge.

Even the content engine fits this. It does not need twenty five LLM agents. It needs about three to five LLM calls, strategy pick, draft, voice and quality judge, maybe one rewrite, with everything else as deterministic gates. That drops a post from a few hundred thousand tokens to roughly twenty to fifty thousand, same quality, because the quality comes from the gates and the voice profile, not from spawning more agents.

Use subagent isolation only for the one or two heaviest creative stages where a clean context truly helps, the draft, not for every role.

Add the agent harness on the CLI. The pi.dev or hermes style planner and executor loop is where agentic pays off, interactive and autonomous use, and it calls the same deterministic tools. Daily batch runs use the cheap deterministic pipeline, interactive sessions use the harness.

Bottom line. Keep the design you love. Change the execution to be cheap, exactly the way your own CLI already does it. You do not have to choose between BMAD clarity and low cost, you keep the clarity and pay CLI prices.

---

## 2. The graph, my decision

Decision, retire the Neo4j graph as the spine. The 3 layer memory, Evidence then Fact then Signal, is the single source of truth.

Reasoning. The graph is legacy and peripheral on both surfaces. In the CLI it survives only through a legacy adapter and is mid migration out. In the web app it sits off the main resume path. It adds a third store, a Neo4j VPS, and ops and cost burden, for little the layered memory plus embeddings do not already give. Simpler is more reliable and cheaper.

If relationship views or a visual career graph are ever wanted, derive them as an optional read only view from the 3 layers, do not maintain the graph as a separate truth. So, graph out of the core, possible enrichment view later.

---

## 3. Resume format, the decision and the build shape

Decision, confirmed with Satvik. LaTeX and Overleaf is the default and the recommended option everywhere. It is the only format that has proven to render reliably.

HTML stays, but demoted. In the web app and the CLI, HTML is already built, so keep it as an optional second choice, not the default. Do not invest more in HTML resume rendering for now.

The pipeline, LaTeX to PDF via GitHub. The resume is a `.tex` file, pushed to a connected GitHub repo, compiled to PDF by a GitHub Action, and the PDF is hosted from there. This makes the output reproducible and shareable by link, with no local LaTeX install needed.

To implement this well I need to study `linkright-resume` and `linkright-skills`, which likely already hold this GitHub Actions compile and host flow. Pending their local paths.

---

## 4. Memory vocabulary, the pure UX call

Two levels, because the user and the code want different things.

User facing, hide the layering. A new user should not have to learn three layer names. Show one warm concept, Career Memory, the user's own brand could be LifeOS. The only state a user needs to feel is whether something is verified, a simple check. The polished output, the resume or the post, just appears, the user never thinks layer 3.

The recommended names, after seeing the live repo. The production memory already uses three files, facts, signals, and expressions, so the layers are real and named. The only weak word is Signal. The recommendation, one vocabulary everywhere.

Layer 1, Memory. The raw, private, lived record, the diary and the evidence. Matches the linkright-memory vault and the ~/.linkright/memory folder. Warm and instantly clear.

Layer 2, Facts. Confirmed, defensible statements, each with its provenance. Already used, keep it.

Layer 3, Strengths. What the facts add up to professionally, the strategic abstractions. This replaces Signal, which is insider jargon. A person understands my strengths on sight.

Outputs, Expressions. The resume, the posts, the interview answers, the stories. Derived from the three layers, not a fourth layer. Matches the existing expressions folder.

So the whole thing reads, Memory to Facts to Strengths, expressed as Expressions. Low churn, only Signal becomes Strength. The content project's real, tell, write and the CLI's Evidence, Fact, Signal both retire into this one set. The user mostly sees one warm concept, Career Memory, with a verified state, the layers stay mostly internal.

---

## 5. Open clarifications I need from Satvik

1. Local paths. Where are `linkright-resume`, `linkright-memory`, `linkright-skills`, `linkright-portfolio` on the laptop, or are they only on GitHub. I cannot fetch GitHub, but I can read any local path.
2. The Claude Code skills to learn from. The `.claude` skills I found are dev tooling, bmad-prfaq, gitnexus, ship-quick, notebooklm, not LinkRight product skills. If there are LinkRight specific Claude Code skills to take the best of, where are they.
3. Confirm the execution recommendation in section 1, keep BMAD structure, deterministic first execution, agent harness on the CLI. This shapes everything we build next.

---

## 6. Standing constraints

Do not delete the existing plugins until the new build is end to end. Study deeply before building anything. Small verified steps, nothing dumped at once.

---

## 7. Field scan, what to borrow from the Vaibhav Sisinty video

The video shows a job hunt and agent setup glued together from consumer tools. Our system is more rigorous, but a few patterns are worth taking.

Worth borrowing.

Hermes, the open source agent harness. It is exactly the pi.dev or hermes style harness we want for the CLI, self learning, persistent memory, agent swarms, cron schedules, hosted on a cheap VPS, driven through OpenRouter. This validates the CLI agent layer plan, study Hermes as the reference for the autonomous career employee.

Aggressive model tiering for cost. A cheap model like Kimi K2 through OpenRouter, around forty times cheaper, for agent swarm and long horizon work, a local Ollama model for non critical overnight tasks at zero cost, and a premium model only where judgement matters. Our CLI already does multi provider free tier plus the Oracle Ollama fallback, so reinforce it, it is the same cost discipline from section 1.

The hosted, always on virtual employee with cron. A career agent that runs daily on a server, not the user's laptop, scouts jobs, tailors the resume, writes cover letters, preps interviews, reads a persistent memory, and reports in the morning. linkright-hunt plus linkright-companion plus an apply step already map to this, borrow the always on framing.

Job board connectors plus computer use for the actual apply step. Indeed and LinkedIn through MCP or browser automation to file applications. This is the missing apply capability.

Where ours is already better, do not copy their weaknesses.

They fabricate fields, a made up pin code and invented details, and dump the raw resume into a prompt. Our Layer 1 truth, fabrication guards, no expand, and do not mention rules are a real quality and ethics edge. This is the moat, keep it.

Their flow is a fragile glue of consumer apps. Ours is one config driven engine on a single source of truth, more reliable, maintainable, and shareable.

Their interview prep is a one off vibe coded app. Ours is a structured skill grounded in a role matrix and a truth engine.

Net. The video confirms the agent harness direction, Hermes, and the cost approach, model tiering, and adds the hosted always on employee plus job board auto apply pattern. Our memory and credibility rigor stays the differentiator.

---

## 8. Memory retrieval, the claude-mem inspiration, and the graph decision

Decision, full decommission the old graph path. The Oracle `/api/oracle/ingest-atom` to Supabase nugget mirror, and the Neo4j lifeos graph, are gone. They sit off the live path and add cost and ops for no real return. Satvik confirmed this.

What replaces the graph is a retrieval layer, not a database. claude-mem is the model, and it uses no graph at all. It captures observations, stores them in SQLite plus a Chroma vector store, and serves accurate context through hybrid search, semantic plus keyword, with progressive disclosure and citations, on a small local worker. That is exactly the accurate retrieval we want, achieved without a graph.

Apply this to the 3 layer career memory.

Hybrid search over the memory. Given a JD, an interview question, or a content topic, search the memory by meaning and by keyword together, and pull the most relevant Facts, Strengths, and Stories. The CLI already embeds and does cosine search, upgrade it to hybrid, vector plus keyword, for precision.

Progressive disclosure, layer aware retrieval. This maps onto the three layers perfectly. Pull only the layer the task needs. A resume bullet needs Facts and Strengths. An interview answer pulls a Story. A deep dive drops to raw Memory. Retrieve the least context that answers the task, with the token cost visible, the same cost discipline from section 1.

Citations and provenance. Every retrieved item carries an id back to its source, the same idea as our fabrication guard, where a Fact already carries its evidence. Keep it and surface it.

Privacy by default. claude-mem has a private tag that keeps sensitive content out of storage and retrieval. Our Layer 1 holds deeply private material and the linkright-memory repo is already private, add a private marker so sensitive Layer 1 content is never pulled into an output.

If a graph view is ever wanted. Derive it on demand from the memory, relationships computed from shared entities, tags, and embedding similarity, as a read only view for visualisation only. Never a separate maintained database.

In short, do not rebuild a graph, build a claude-mem style retrieval layer over the 3 layer memory, hybrid search plus progressive disclosure plus citations plus privacy.

---

## 9. Knowledge retrieval at execution, must follow versus situational

This is Satvik's idea, and it is the biggest token lever we have found. Today every step loads whole knowledge files into context, a wall of reference the model has to skim. Instead, each step that needs knowledge should generate a few targeted queries, retrieve only the relevant answers in a tight paragraph form with citations, and load only those. Same claude-mem retrieval layer, pointed at the knowledge base instead of the career memory.

The key split, must follow versus situational.

Must follow, always loaded, small and deterministic. The hard gates, the punctuation and banned word rules, the scoring thresholds, the user's voice profile core signals, the config. These are tiny and apply every time, so load them directly, never through retrieval. This is the floor that keeps quality safe even if a retrieval misses.

Situational, retrieved on demand. The large reference, the post types catalog, the psychology and storytelling toolkit, the algorithm mechanics, the design principles, the bullet bank, the metrics ledger, the audience research. These are big and only partly relevant to any one task, so retrieve only the slices that matter for this post or this resume.

How a step uses it. The agent forms a short list of sharp queries for its task, for a teardown post, what makes a strong teardown hook, how to structure a data backed insight, the current rule for document carousels. It hybrid searches the chunked knowledge, pulls back tight paragraph answers with ids, and loads just those. A small query step, not a wall of text.

Authoring implication. Knowledge has to be written as small, self contained, queryable chunks, rule cards or question and answer snippets, each tagged, not just long prose. This forces clarity and makes retrieval accurate. Each knowledge file carries a marker, load always or load situational.

The growth loop, this is the real payoff. Because retrieval is query driven, the knowledge base can grow without limit, every new rule and pattern the System Optimizer learns becomes a new chunk, and no single execution gets heavier. Learnings turn into retrievable knowledge instead of prompt bloat. The base gets smarter forever, the context stays tight.

One retrieval engine, two corpora. The same layer indexes both the per user career memory, Memory, Facts, Strengths, Stories, and the generic engine knowledge base, rules and patterns. One primitive, two sources, both served by hybrid search plus progressive disclosure plus citations.

Schema change this implies. In each agent.yaml, split dependencies.knowledge into knowledge.always and knowledge.retrieve. The always list loads directly, the retrieve list is fetched by query at run time. This is a clean, small change to the config model.

Cost and quality together. Sharp, relevant knowledge beats a wall of generic reference the model has to wade through, so this lifts quality while it cuts tokens. Paired with deterministic first execution from section 1 and model tiering from section 7, this is the core of a cheap, high quality engine.

One caveat, honestly. Retrieval can miss. The defences are, keep must follow always loaded, chunk and tag the knowledge well, and optionally pin a couple of core chunks per task type so the essentials are never missed. Never put a hard gate behind retrieval, gates stay code and always on.
