# LinkRight, Unification Roadmap

Draft v0.2 for alignment. Date 2026-06-05. v0.2 is rewritten from ground truth, after a deep code study of both local repos, `~/Documents/sync-resume-engine` (web app) and `~/Documents/linkright_production` (CLI), plus the four installed Cowork skills and the content engine we built. This corrects the guesses in v0.1.

---

## 1. The vision

LinkRight is a career intelligence operating system. The product should live on four surfaces, all sharing one career memory.

1. Cowork plugins, the Claude desktop app.
2. Claude Code plugins.
3. The CLI, `pip install linkright`, to be upgraded with an agent harness inspired by pi.dev or hermes.
4. The web app at sync.linkright.in, with a focus on backend performance, speed, and quality.

The whole point is that the same career truth feeds the resume, the interview prep, the LinkedIn content, and the job search, on every surface, so nothing contradicts and everything compounds.

---

## 2. The keystone, one 3 layer career memory

This is the heart, and it already exists, well built, in the CLI as memory v2. The model is three layers.

Layer 1, Evidence, the real. Raw imported documents and chunks, the unfiltered truth. In the content project this is `layer_1_the_real`.

Layer 2, Fact, the tell. Atomic, confirmed statements, each carrying its evidence provenance and a confidence score. Nothing here that is not traceable to Layer 1. In the content project this is `layer_2_the_tell`.

Layer 3, Signal, the write. Controlled vocabulary strategic abstractions, the compressed output language. In the content project this is `layer_3_the_write`, the resume bullets and the Metrics Bank.

All of it sits under a CareerProfile root, stored as JSONL plus embeddings in `~/.linkright/`. This is the single source of truth every tool should read. It is the same idea as the content project's real, tell, write markdown layers, just renamed Evidence, Fact, Signal and implemented in code.

---

## 3. The atom graph, answered

Satvik asked, check where the old atom graph is used, and his instinct that it is weaker than the 3 layer memory is correct.

In the CLI, there is no graph database. The old flat nugget shape survives only through `legacy_adapter.py`, which derives nugget shapes from v2 Facts so the large resume orchestrator does not have to be rewritten yet. It is mid migration, not dead, and slated for removal.

In the web app, a Neo4j graph in `oracle-backend/lifeos/` does exist, with Achievement, Experience, Skill, Metric nodes. But it is off the main resume path. It is fed by an external interview tool through `/api/oracle/ingest-atom`, and mirrored into Supabase. The live memory the resume pipeline actually reads is the Supabase nugget store.

So the relationship is, roughly, two independent attempts, with the 3 layer memory being the newer and better direction. The graph is legacy or peripheral on both surfaces. The plan should standardise on the 3 layer memory and treat the graph as optional enrichment, not the spine.

---

## 4. Current state across the four surfaces, ground truth

| Capability | CLI (linkright_production) | Web app (sync-resume-engine) | Cowork skills | Content engine we built |
|---|---|---|---|---|
| 3 layer memory | Yes, v2 Evidence, Fact, Signal, JSONL | No, Supabase nugget store plus peripheral Neo4j | Partly, real, tell, write markdown in content project | Voice profile plus metrics ledger, a partial Layer 2 and 3 |
| Resume | Yes, HTML, scored, width fit, fabrication guards | Yes, HTML, 8 phase pipeline, fabrication guards | `linkright-sync`, LaTeX only, and `sync`, HTML, older | No |
| Cover letter | Yes | Yes | Inside `linkright-sync` | No |
| Job search, Scout | Yes, scored matching | Yes, scan, watchlist, applications | No | Profile search, networking only |
| Interview | Yes, coach plus practice plus stories | Yes, interview-prep routes | `interview-coach`, `mock-interview-simulator` | No |
| LinkedIn content | Yes, a content pillar | Yes, broadcast routes | No | Yes, the full engine |
| Agent harness | No, exposes an MCP server only | No | No | Subagent conductor for content |
| LLM routing, fallback | Yes, many free providers plus Oracle VPS | Yes, multi provider plus Oracle | Per skill | Per workflow |

Takeaway. The CLI is the most complete and modern. It already has all four pillars plus the 3 layer memory plus an MCP server. The web app is strong on resume plus Scout plus hosted memory. The Cowork skills and our content engine are partial, and our content engine overlaps the CLI content pillar.

---

## 5. Divergences to resolve before unifying

Resume format split. The CLI and the web app both output HTML. The Cowork `linkright-sync` skill is LaTeX only, Satvik removed HTML there because it was brittle. Decide one source of truth for resume rendering, or keep HTML for web and CLI and LaTeX for the Cowork skill, explicitly.

Duplication. Our Cowork content engine and the CLI content pillar do the same job differently. They should converge on one design and one memory read.

Memory storage. Three stores exist, CLI JSONL, web app Supabase, web app Neo4j. The unified design needs one canonical memory contract, with adapters per surface, not three truths.

No agent loop anywhere. The CLI is agent ready through MCP but has no planner or executor. The harness Satvik wants, pi.dev or hermes style, does not exist yet on any surface.

---

## 6. Unified target

One memory contract, the 3 layer Evidence, Fact, Signal model, defined once as a shared schema. Each surface reads and writes it through an adapter. The CLI keeps JSONL local, the web app keeps Supabase, but both speak the same Evidence, Fact, Signal shape, and the graph becomes optional enrichment.

One set of pillar engines, resume, cover letter, job search, interview, content, each defined once against the memory contract, then surfaced as a Cowork skill, a Claude Code command or skill, a CLI command, and a web app flow. The CLI already has these as MCP tools, that is the natural bridge to Claude Code and Cowork.

One agent harness on top of the CLI, a planner and executor loop, inspired by pi.dev or hermes, that drives the pillar tools autonomously where the user wants hands off, while keeping the gated human in the loop mode for high stakes steps.

Web app, backend performance focus, keep it the hosted sync and Scout and memory layer, optimise the worker pipeline for speed and quality.

---

## 7. Build phases, small steps, nothing dumped at once

Phase A, lock this map. Confirm the memory contract and resolve the divergences in section 5. No code yet.

Phase B, write the shared memory contract, the Evidence, Fact, Signal schema as one document, the single source of truth all surfaces target.

Phase C, converge content. Fold our Cowork content engine and the CLI content pillar into one content design that reads the memory contract. This is where we already have the most depth.

Phase D, the Cowork plugin, the LinkRight plugin, wrap the pillar engines as Cowork skills reading the shared memory.

Phase E, the Claude Code plugin, mostly the same skills repackaged, plus commands.

Phase F, the CLI agent harness, add the planner executor loop on top of the existing MCP tools.

Phase G, web app backend performance pass.

Each phase breaks into small verified steps with a check at the end.

---

## 8. Open questions for Satvik, to perfect this map

1. Memory names. Keep the CLI names Evidence, Fact, Signal as the canonical 3 layer, or rename to real, tell, write to match the content project. One vocabulary across everything.
2. Resume format. One canonical renderer, HTML everywhere, or HTML for web and CLI and LaTeX for Cowork, on purpose.
3. The graph. Retire the Neo4j graph entirely, or keep it as optional enrichment behind the 3 layer memory.
4. Source of truth surface. Should the CLI be the reference implementation that the others mirror, since it is the most complete, or the web app.
5. Content convergence. Rebuild the CLI content pillar on our content engine design, or fold our engine into the CLI's existing pillar.

---

## 9. Ground truth update, the linkright-skills system is the live spine

Reading the four repos changed the picture again, for the better. The most current, coherent LinkRight is `linkright-skills`, a set of Claude Code Agent Skills, eight specialists that already do almost everything we planned.

| Skill | Job |
|---|---|
| linkright-setup | first time setup wizard |
| linkright-mem | career memory, resume and diary into structured facts and signals in ~/.linkright/memory |
| linkright-hunt | job finder, 500 plus company boards, scores each against the profile |
| linkright-sync | resume writer, JD into a tailored ATS safe resume |
| linkright-push | publisher, resume to GitHub Pages, versioned, with PDF |
| linkright-interview, linkright-interview-coach | story bank, mock interviews with voice, FAANG style scoring |
| linkright-companion | daily briefing, what to do, where applications stand |
| linkright-network | content plus outreach, LinkedIn posts and cold emails in the user's voice |
| linkright-portfolio | public portfolio plus a live career dashboard |

The memory is `linkright-memory`, a private git backed vault, confirming the 3 layer model in production. `facts.md` is Layer 2 Facts, `signals.md` is Layer 3 Signals, `expressions/stories` are the STAR stories, plus a diary and a decisions journal for the Layer 1 raw. Git backed for backup and portability into ~/.linkright. No graph anywhere, the graph is dead in the live system.

The resume hosting is `linkright-resume`, versioned HTML plus PDF served on GitHub Pages, driven by linkright-push. The portfolio and dashboard are `linkright-portfolio`, static pages generated from a pipeline.json.

What this means for the plan.

The spine already exists. linkright-skills is the unified Claude Code and Cowork surface we were going to build. We do not rebuild it, we adopt it and take the best of it.

Our content engine is an enhanced linkright-network. Fold the voice profile, the BMAD structure, the gates, and the deterministic first execution into linkright-network, rather than ship a separate content plugin.

Skill names are settled. Use the existing linkright- names, setup, mem, hunt, sync, push, interview, companion, network, portfolio. They are clear, searchable, and already exist.

The resume format change lands here. Today linkright-sync and linkright-push produce HTML on Pages. Per the decision, switch the default to LaTeX, compiled to PDF by a GitHub Action, still served on Pages. HTML becomes the optional second format.

Memory vocabulary is settled too. Production already uses facts and signals, which match Evidence, Fact, Signal. Keep that, it is consistent across the CLI and the skills.
