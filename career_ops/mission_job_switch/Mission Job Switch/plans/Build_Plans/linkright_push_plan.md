# linkright-push — Skill Plan

**Skill:** `/linkright-push`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 1 — Build Second (after linkright-mem)  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-push` is the GitHub backbone of the entire Linkright system.

It provides:
- Permanent, versioned, public URLs for every resume variant
- Private version-controlled vault for all memory data
- Public GitHub Pages portfolio site
- Live career pipeline Kanban dashboard
- Application metrics widgets
- Resume pull/push workflow for edit-version-republish cycles

The philosophy: **GitHub as career control panel.** Everything important about your job search — resumes, memory, pipeline, portfolio — lives in repos: versioned, backed up, accessible from anywhere, and with a permanent URL for every version ever sent.

This matters for a reason beyond organization: when you send a resume to a company and get called back three months later, you should be able to pull the exact version that got you in. Without versioning, that's impossible.

---

## 2. Repository Architecture

### Repository 1: `linkright-resume` (PUBLIC)

Permanent hosting for all resume versions.

```
linkright-resume/
├── index.html                    ← latest version, primary resume
├── roles/
│   ├── <company-slug>-<role-slug>/
│   │   ├── index.html            ← tailored version for this role
│   │   └── resume.pdf            ← PDF export
│   └── ...
└── README.md                     ← minimal: name + contact
```

**Public URLs:**
- `https://<username>.github.io/linkright-resume/` → latest resume (put this in email sig)
- `https://<username>.github.io/linkright-resume/roles/anthropic-senior-pm/` → role-specific version

**Why public:**
- Recruiter can see it directly from email/LinkedIn
- GitHub Pages = zero hosting cost
- Version history shows professional trajectory (optional to make visible)

### Repository 2: `linkright-portfolio` (PUBLIC)

Portfolio site and career dashboard.

```
linkright-portfolio/
├── index.html                    ← portfolio home + featured projects
├── cases/
│   └── <case-slug>.html          ← individual case studies
├── dashboard/
│   └── index.html                ← live pipeline Kanban + metrics
└── README.md
```

**Public URLs:**
- `https://<username>.github.io/linkright-portfolio/` → portfolio (share with hiring managers)
- `https://<username>.github.io/linkright-portfolio/dashboard/` → career dashboard (personal use)

### Repository 3: `linkright-memory` (PRIVATE)

All sensitive career data. Private. Never public.

```
linkright-memory/
├── user_setup.md                 ← personal config, constraints, targets
├── memory/
│   ├── facts.md
│   ├── signals.md
│   ├── outcomes.json             ← application outcomes for adaptive model
│   ├── evidence/
│   ├── interpretations/
│   └── expressions/
├── pipeline.json                 ← full opportunity pipeline state
├── diary/
│   └── YYYY-MM-DD.md
└── decisions/
    └── decision_log.md
```

**Why private:** Contains salary targets, rejected companies, honest rejection analyses, personal constraints, raw work reflections. None of this should be indexable.

---

## 3. GitHub Actions Automation

Three automated workflows in the private memory repo:

### Action 1 — Diary Reminder

```yaml
# Fires on weekday evenings — user's local timezone
name: Daily diary reminder
on:
  schedule:
    - cron: '0 13 * * 1-5'   # adjust to user's timezone
jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Send email reminder
        # Uses GitHub-native emailling or sends via SMTP
        # Subject: "Linkright: Add today's diary entry"
```

### Action 2 — Weekly Pipeline Report

```yaml
# Fires Sunday morning
name: Weekly pipeline summary
on:
  schedule:
    - cron: '0 6 * * 0'
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate report
        run: python scripts/weekly_report.py
      - name: Email report
        # Sends pipeline summary to user's email from user_setup.md
```

### Action 3 — Resume URL Health Check

```yaml
# Fires on every push to main
name: Validate resume renders
on:
  push:
    branches: [main]
    paths: ['**.html']
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check HTML validity
        run: python scripts/validate_html.py
```

---

## 4. Career Kanban Dashboard

The dashboard at `/dashboard/index.html` reads from `pipeline.json` and renders live.

**No server required.** Pure client-side JavaScript. The file can be opened locally by double-clicking or served via GitHub Pages.

### Dashboard Sections

**Section 1 — Pipeline Kanban**

Five columns: SAVED | APPLIED | SCREENING | INTERVIEW | OFFER

Each card shows:
- Company name
- Role title
- Days in current stage (auto-computed from stage_history)
- Fit score (from hunt scoring)
- Shortlist probability (from adaptive model, if available)

Color coding: green = <7 days, yellow = 7-14 days, red = >14 days in stage (needs action)

**Section 2 — Key Metrics**

```
Applications sent this month:     [N]
Response rate:                     [N]%  ([N] of [N] applications)
Interview conversion:              [N]%  ([N] of [N] responses)
Avg days to first response:        [N]
Avg fit score (applied jobs):      [N]%
Shortlist model confidence:        [low/medium/high]
```

**Section 3 — Shortlist Model Insight**

If model confidence ≥ medium:
"Your highest-converting job type: [archetype + domain + company stage]"
"Suggested priority: [recommendation]"

**Technology stack:**
- Single HTML file — no build step, no framework
- Inline JavaScript to parse `pipeline.json`
- Loads pipeline.json from same repo (same-origin fetch)
- Works offline if opened from local file system

---

## 5. Resume Versioning System

Every push gets a git tag:

```bash
# Automatic on every resume push:
git tag resume-<company-slug>-<role-slug>-<YYYY-MM-DD>
git push origin --tags
```

To retrieve any version:
```bash
git checkout resume-anthropic-senior-pm-2026-05-20 -- roles/anthropic-senior-pm/index.html
```

Use cases:
- You applied in January, they call back in April — pull the exact version they saw
- You want to see how your positioning has evolved
- You're debugging why one version performed better than another

---

## 6. Push / Pull Workflows

### Push a resume

```
/linkright-push resume --company anthropic --role senior-pm

Workflow:
1. Validate HTML (ATS scan, width check via measure_width.py)
2. Generate PDF via headless Chrome
3. Copy to: roles/anthropic-senior-pm/
4. git add → git commit "resume: anthropic senior-pm [date]"
5. git tag resume-anthropic-senior-pm-[date]
6. git push origin main --tags
7. Return: public URL
```

### Pull a resume for editing

```
/linkright-push pull --company anthropic --role senior-pm

Workflow:
1. git pull latest
2. Copy to local working directory
3. Return: local file path + load into linkright-sync for editing
```

### Push memory vault

```
/linkright-push memory

Workflow:
1. Diff current memory/ vs last committed version
2. Show summary: "X new facts, Y updated signals, Z new outcomes"
3. User confirms
4. git add memory/ → git commit "memory: [date] — [summary]"
5. git push origin main
6. Return: commit hash
```

### Push pipeline data

```
/linkright-push pipeline

Workflow:
1. Read pipeline.json from linkright-hunt
2. Show diff from last committed version
3. User confirms (or auto-push with confirmation setting)
4. Commit + push
5. Dashboard at GitHub Pages URL now reflects latest data
```

---

## 7. First-Time Setup

When user runs `/linkright-push` for the first time:

```
STEP 1: Check prerequisites
  → git installed?
  → GitHub CLI (gh) installed? (install instructions if not)
  → gh auth login (if not authenticated)

STEP 2: Create repos
  gh repo create linkright-resume --public --description "[Name] - Resume"
  gh repo create linkright-portfolio --public --description "[Name] - Portfolio"
  gh repo create linkright-memory --private --description "Linkright Memory Vault"

STEP 3: Enable GitHub Pages
  → For linkright-resume: branch main, folder /
  → For linkright-portfolio: branch main, folder /

STEP 4: Initialize file structure
  → Clone all 3 repos
  → Create folder structure
  → Push initial README + placeholder index.html

STEP 5: First test
  → Push a sample resume
  → Verify URL is live (takes 1-2 minutes for GitHub Pages to activate)
  → Confirm private repo is not publicly accessible

STEP 6: Store URLs in user_setup.md
  resume_base_url: [URL]
  portfolio_base_url: [URL]
```

---

## 8. Skill Gates

### Gate 1 — Action Selection

```
What do you want to do?
a) Push a resume (new or updated version)
b) Pull a resume for editing
c) Push memory vault
d) Push/sync pipeline data
e) Deploy portfolio site
f) View dashboard URL
g) Set up repos (first time)
```

### Gate 2 — Execute

Run the appropriate workflow from Section 6 above.

### Gate 3 — Confirm + Report

Show: what was committed, what URL was updated.  
For resume push: return permanent public URL.  
For memory push: return commit hash.

---

## 9. Hard Rules

- **ALWAYS validate HTML before pushing to public resume repo** — broken HTML at a public URL is worse than no URL
- **ALWAYS generate PDF alongside HTML** for every resume push
- **NEVER push to public repos without user confirmation** of exactly what's being published
- **ALWAYS tag every resume push** with company + role + date
- **NEVER make memory repo public** — contains sensitive career data
- **ALWAYS show diff before any memory commit**
- **NEVER push unvalidated content** — ATS scan + constraint check must pass first

---

## 10. References to Write

| File | Contents |
|---|---|
| `references/ref_01_github_setup.md` | First-time setup guide; GitHub CLI commands; Pages configuration; troubleshooting |
| `references/ref_02_repo_structure.md` | Full structure of all 3 repos with file descriptions and purpose |
| `references/ref_03_actions_templates.md` | GitHub Actions YAML for all 3 automated workflows |
| `references/ref_04_dashboard_template.md` | Full dashboard HTML + JavaScript; pipeline.json schema; Kanban rendering logic |

---

## 11. Scripts to Build

| Script | Purpose |
|---|---|
| `scripts/push_resume.sh` | Full push workflow for a resume (validate → PDF → commit → tag → push) |
| `scripts/pull_resume.sh` | Pull specified resume version to local |
| `scripts/push_memory.sh` | Diff + confirm + commit + push memory vault |
| `scripts/generate_pdf.py` | Headless Chrome → HTML to PDF |
| `scripts/scaffold_repos.sh` | First-time repo creation and structure initialization |
| `scripts/build_dashboard.py` | Generate dashboard HTML from pipeline.json |
| `scripts/weekly_report.py` | Generate weekly pipeline summary for GitHub Action |
| `scripts/validate_html.py` | HTML validation before push |

---

## 12. Build Checklist

- [ ] Write ref_01_github_setup.md
- [ ] Write ref_02_repo_structure.md
- [ ] Write ref_03_actions_templates.md
- [ ] Write ref_04_dashboard_template.md (full working Kanban HTML)
- [ ] Write scripts/scaffold_repos.sh
- [ ] Write scripts/push_resume.sh
- [ ] Write scripts/build_dashboard.py
- [ ] Write SKILL.md (lean orchestrator)
- [ ] Run first-time setup on test GitHub account
- [ ] Push test resume → confirm URL works
- [ ] Push test pipeline.json → confirm dashboard renders
- [ ] Confirm private repo is not publicly visible

---

## 13. Success Criteria

- All 3 repos created and correctly structured
- Resume URL live at GitHub Pages within 5 minutes of first push
- Every resume push tagged with company + role + date
- PDF generated for every HTML push
- Pipeline dashboard renders correctly from pipeline.json
- Memory vault private and committed without errors
- Dashboard metrics accurate against pipeline.json data
