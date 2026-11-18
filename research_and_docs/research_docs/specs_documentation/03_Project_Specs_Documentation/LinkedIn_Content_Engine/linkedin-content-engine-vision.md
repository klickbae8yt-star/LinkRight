# LinkedIn Content Engine — Vision Document

Captured at the end of a session that started as "build a simple n8n workflow to
generate one LinkedIn post" and grew into a self-improving content system. This
file is the handoff into a fresh chat — read it first, then continue from here.

## Where this started

Original ask: SSH into an Oracle ARM64 server, use the `pi` CLI (an agentic
coding-agent binary) over OpenRouter's free models to generate a LinkedIn post
from a topic string.

## What we learned along the way

- **pi CLI is installed and working** on the Oracle server (`linkright-server`,
  ARM64/aarch64). Binary lives at `~/pi/pi`, symlinked to `/usr/local/bin/pi`
  (the symlink matters — pi needs its sibling `theme/` and `assets/` folders,
  so copying just the binary breaks it with a `theme/dark.json` ENOENT error).
- **OpenRouter key** is stored server-side at `~/.pi_env` (`export
  OPENROUTER_API_KEY=...`), sourced at the start of any SSH command rather than
  hardcoded — the key was accidentally exposed once in an uploaded workflow
  JSON and should be treated as rotated/rotatable, not precious.
- **$20 has been added to the OpenRouter account** — this permanently unlocks
  1000 free-tier (`:free` model) requests/day, up from 50/day. This is
  *account-wide*, not per-model: OpenRouter's free-tier rate limit (20
  req/min, 50 or 1000 req/day) is a single shared bucket across every `:free`
  model you call. Chaining models does **not** multiply the quota — it only
  buys resilience against a specific model being deprecated or pulled (this
  happened live: `meta-llama/llama-3.1-8b-instruct:free` stopped being free
  mid-session).
- **Current free-model shortlist** (verified against openrouter.ai on
  2026-09-12 — re-verify before relying on this, the free lineup churns):
  `nvidia/nemotron-3.5-lightning:free` (primary pick — 1M context, strong
  agentic reasoning), `thinkingmachines/inkling:free` (fallback, different
  provider family so an independent failure domain), plus
  `nvidia/nemotron-3-ultra-550b-a55b:free`, `thinkingmachines/inkling-small:free`,
  `nvidia/nemotron-3-super-120b-a12b:free`, `liquid/lfm-2.5-2.6b:free` as
  further-down options. Avoid the coding-flavored free models
  (`cohere/north-mini-code`, `poolside/laguna-*`, `nex-agi/nex-n2.5-*`) for
  prose — they're tuned for code, not LinkedIn writing voice.
- **The router idea (small free model decides which bigger model handles the
  task) was explicitly rejected** once we realized quota is account-wide —
  routing added a wasted extra API call for no benefit. What survived: primary
  model + one fallback, tried in order, first success wins.

## The architecture question we landed on

**SSH + pi CLI is the wrong default tool for this job**, and should be reserved
for the narrow case where a step must execute *on that specific remote
machine* — read a local file, run a local script, touch a resource only that
server can see. Plain text generation and even most "agentic" reasoning don't
need that.

For everything else, **n8n's native AI Agent node (LangChain-based, built in,
no extra install) is the better fit**:

- An **OpenAI Chat Model node** pointed at OpenRouter's OpenAI-compatible
  endpoint (`https://openrouter.ai/api/v1`, OpenRouter key, model id such as
  `nvidia/nemotron-3.5-lightning:free`) stands in for the "provider."
- The **AI Agent node** orchestrates multi-step reasoning natively.
- A **Think tool** attached to the Agent surfaces its reasoning as a visible
  step in n8n's own execution log — no more parsing `--mode text` vs
  `--mode json` stdout by hand.
- Further tools (**HTTP Request tool**, **Code tool**, **Vector Store tool**,
  **Workflow tool** for calling sub-workflows) give it real agentic
  capability — fetching data, running JS/Python, searching memory, calling
  other workflows — all without touching SSH.
- Model fallback becomes trivial: swap the model id in the Chat Model node, or
  wire two Chat Model nodes with a fallback connection.
- Ollama is not applicable here — it's for running model weights locally; this
  whole setup calls a hosted API (OpenRouter), no local inference involved.

**Rule of thumb going forward:** reach for SSH/pi only when a step's *action*
has to happen on the Oracle server itself. Everything else — generation,
reasoning, tool use, memory, scoring — belongs in native n8n nodes.

## The expanded vision (this is the new part)

The real goal isn't "generate one post." It's a **closed-loop, self-improving
content system** that runs unattended for weeks:

1. **Generate** a LinkedIn post (topic in, agentic reasoning, draft out).
2. **Publish** it to LinkedIn and capture the resulting post URL.
3. **Wait a day**, then **revisit that URL** (or use LinkedIn's API if
   available) and pull engagement numbers — likes, comments, shares, views,
   whatever is accessible.
4. **Log every post + its engagement numbers** somewhere durable — a data
   table, a sheet, a database — building a history over time.
5. Repeat daily, unattended, for a stretch (30 days was the number mentioned).
6. **Weekly**, look back over the week's posts and their engagement, and
   **write a strategic report**: what topics/angles/formats worked, what
   didn't, and why (as best an LLM can infer from the numbers + post content).
7. **Auto-tune the generation prompt** based on that weekly report — the
   system edits its own instructions going forward, closing the loop.

This is a memory-and-feedback architecture, not a one-shot generation
workflow. It needs: a persistent store (post history + engagement history), a
publish step, a scheduled re-check step, a weekly analysis step, and a
mechanism for the analysis to actually rewrite the live prompt (not just
recommend a rewrite — the ask was explicit self-updating).

### A relevant thing already sitting in this account

There is an existing **`linkedin-content-engine`** skill set installed
(`setup`, `daily-post`, `topic-hunt`, `profile-search`, `optimize`). The
`optimize` skill's own description is almost verbatim this ask: *"Reviews
recent post performance and improves the system, scoring weights, knowledge,
and voice drift... runs a weekly or monthly improvement pass."* This is worth
opening and reading before building any of the above from scratch in n8n — it
may already solve steps 5–7, or at least define the file/config shape
(`daily-post` presumably already handles generation + a voice profile) that
the n8n pipeline should either replace, wrap, or feed into. Comparing "build
this natively in n8n with SSH/pi + AI Agent" against "use the installed
linkedin-content-engine skill and see what it's missing" is the first fork in
the road for the next session.

### Possibilities not yet explored, worth raising next time

- **LinkedIn API access vs. scraping the public URL.** Scraping a public post
  URL daily for engagement numbers is fragile (markup changes, rate limits,
  possible ToS friction) and may not expose full metrics (impressions are
  often private-only). Worth checking whether a LinkedIn API / Developer app
  is feasible, or whether manual entry (you paste numbers in) is the honest
  fallback for MVP.
- **Where the history lives.** An n8n Data Table (per the destructive-ops
  discipline already established in the n8n-operator skill — identity keys,
  match modes, the works) vs. a Google Sheet vs. something else. This choice
  determines how "the weekly report node" queries history.
- **What "auto-updates the prompt" actually means mechanically.** Likely: the
  weekly analysis writes a new version of a stored prompt/config file (or a
  Data Table row) that the daily generation step reads at the start of each
  run — a project-context-style file, versioned, with a human allowed to see
  the diff before it's live (a guard rail worth considering, given how badly
  an unsupervised self-editing prompt could drift over 30 days).
- **Guard rails on the self-tuning loop.** Should every week's auto-edit be
  auto-approved, or should it land as a proposed diff you approve before it
  takes effect? Fully autonomous prompt mutation for a month with no checkpoint
  is a real risk (voice drift, reward-hacking the engagement metric, quality
  collapse) — worth deciding deliberately rather than by default.
- **Failure handling for the 30-day unattended run.** Publish failures,
  LinkedIn layout changes breaking the scrape, a day where engagement can't be
  fetched — the loop needs to survive a bad day without silently producing
  garbage data that poisons the following week's report.
- **Rate limits again, at scale.** 1000 free requests/day is generous for one
  post/day, but the weekly report + daily engagement checks + any research
  calls all draw from the same bucket — worth roughly budgeting the daily call
  count once the full pipeline is designed.

## What's next

This thread pauses here. Open a new chat for the content-engine build — start
by reading the installed `linkedin-content-engine` skill (especially
`optimize` and `setup`) before designing anything new in n8n, since it may
already cover large parts of steps 5–7 above.

The original thread continues separately on the referral-automation project
(the n8n-operator skill, `project-context.md`, and the pending 62-row repair
with its four unanswered clarifying questions) — that work resumes where it
left off, unaffected by this detour.
