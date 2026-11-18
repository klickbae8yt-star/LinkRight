# LinkRight, Master Plan v1.0

The single, consolidated plan. Date 2026-06-05. This pulls every decision into one place. The detailed reasoning lives in `LinkRight-Plugin-Roadmap.md` and `LinkRight-Architecture-Decisions.md`. This file is the source of truth for what we are building and in what order.

---

## 1. What LinkRight is

A career intelligence operating system. One career truth feeds every tool, the resume, the interview prep, the LinkedIn content, the job hunt, so nothing contradicts and everything compounds. It lives on four surfaces, the Cowork plugin, the Claude Code plugin, the CLI, and the web app.

---

## 2. The spine already exists, linkright-skills

The live, coherent LinkRight is the `linkright-skills` repo, a set of Claude Code Agent Skills. We adopt it and take the best of it, we do not rebuild it.

| Skill | Job |
|---|---|
| linkright-setup | first time setup |
| linkright-mem | career memory, resume and diary into structured facts and strengths |
| linkright-hunt | job finder, scores roles against the profile |
| linkright-sync | resume writer, JD into a tailored, ATS safe resume |
| linkright-push | publisher, resume to GitHub Pages, versioned, with PDF |
| linkright-interview, linkright-interview-coach | story bank, mock interviews, scoring |
| linkright-companion | daily briefing |
| linkright-network | content and outreach in the user's voice |
| linkright-portfolio | public portfolio and a live career dashboard |

---

## 3. The heart, the Career Memory, three layers

Memory, the raw private lived record, diary and evidence. Facts, confirmed defensible statements, each with its provenance. Strengths, what the facts add up to professionally. The outputs, the resume, posts, interview answers, and stories, are Expressions, derived from the three layers, not a fourth layer.

It is a git backed private vault, the `linkright-memory` repo, portable into ~/.linkright. The user mostly sees one warm idea, Career Memory, with a verified state.

The graph is decommissioned. The Oracle ingest-atom path, the Supabase nugget mirror, and the Neo4j graph are all gone. They were off the live path and added cost for no return.

Retrieval replaces the graph. Inspired by claude-mem, accurate context comes from hybrid search, semantic plus keyword, with progressive disclosure and citations, over a small store. No graph database. If a graph view is ever wanted, derive it on demand from the memory, never maintain a separate one.

---

## 4. The execution model, cheap and high quality

Four ideas stacked.

BMAD structure. Config driven workflows, agents as expert lenses, evals as gates, templates as contracts, one memory as the source of truth. This is the design language.

Deterministic first. Every hard gate is code, punctuation, banned words, hook signature, metric consistency, width, contrast. The model is called only for the few steps that truly need reasoning, the draft, the judgement, a rewrite. This is what keeps cost low and quality steady.

Knowledge by retrieval. Do not load whole knowledge files. Split knowledge into must follow, the small always loaded rules, and situational, the large reference fetched on demand by sharp queries. The base can grow forever, the context stays tight. In each agent config, dependencies.knowledge splits into knowledge.always and knowledge.retrieve.

Model tiering. A cheap model for swarm and long horizon work, a local model for non critical overnight tasks, a premium model only where judgement matters. Subagent isolation only for the one or two heaviest creative stages, not for every role.

---

## 5. The pieces, per capability

Memory, the contract in section 3, the keystone every other piece reads.

Resume, sync and push. LaTeX is the default and the recommended format, compiled to PDF by a GitHub Action, served on GitHub Pages, versioned. HTML stays as an optional second format. Do not invest more in HTML.

Job hunt, hunt, plus a new apply step. Job board connectors or computer use to find and file applications.

Interview, interview and coach. A role matrix and a truth engine, reading the memory instead of re asking for the profile.

Content, network. Fold our content engine into it, the validated voice profile, the BMAD structure, the gates, and the deterministic first execution. This is an upgrade to the existing skill, not a separate plugin.

Companion, the daily briefing. Portfolio, the public site and the live pipeline dashboard.

---

## 6. The four surfaces

Cowork plugin. The skills as Cowork skills. The current content Cowork plugin stays untouched for now, the vector retrieval adds little there at today's size.

Claude Code plugin. The linkright-skills set, already that shape.

CLI. The `linkright_production` package, plus a new autonomous agent harness inspired by Hermes and pi.dev, self learning, persistent memory, cron, hosted, calling the deterministic tools.

Web app. The `sync-resume-engine`, kept as the hosted sync, jobs, and memory layer, with a focus on backend performance, speed, and quality.

---

## 7. Locked decisions

Graph decommissioned, retrieval layer instead. Resume default LaTeX, HTML optional. Memory names, Memory, Facts, Strengths, outputs Expressions. Execution, BMAD structure plus deterministic first plus knowledge by retrieval plus model tiering. Engine stays user agnostic, user specifics live in config and instance files. Settings and memory are separate. Layer 1 is private by default. Do not disturb the content Cowork plugin yet. Never reduce the depth of knowledge, retrieval changes loading, not storage. All research is preserved, locally, in a zip, and in the private GitHub repo.

---

## 8. Build phases, small verified steps

Phase 0, done. Research, the roadmap, the decisions, and full preservation.

Phase A, next. Write the Career Memory contract. One document that defines Memory, Facts, Strengths, and Expressions, the retrieval interface, the must follow versus situational split, and the agent config knowledge.always and knowledge.retrieve schema. Design only, no code, it touches nothing live, and everything else reads from it.

Phase B. Fold the content engine into linkright-network, the voice profile, the gates, the deterministic first execution, as an upgrade to the existing skill.

Phase C. Switch the resume to LaTeX, compiled by a GitHub Action, HTML demoted to optional.

Phase D. Build the retrieval layer, hybrid search over the memory and the knowledge base.

Phase E. Add the CLI agent harness, Hermes inspired.

Phase F. The web app backend performance pass.

Each phase breaks into small steps with a check at the end. We move only on your go.

---

## 9. Where everything is preserved

The workspace folder on your computer, a consolidated zip at `LinkRight-Research/`, and the private GitHub repo `satvik-jain-iitd/linkright-research`. Three copies, one offsite.

---

## 10. The immediate next step

Phase A, the Career Memory contract. It is the keystone, low risk, design only, and it does not touch any working skill. Once it is locked, every other phase has a firm thing to build against. Recommended to do this next, on your go.
