# LinkRight — Unified Career Navigation & Candidate Platform

Welcome to **LinkRight** — the end-to-end career navigation, resume synchronization, interview preparation, and talent intelligence ecosystem.

---

## 1. System Modules

```text
LinkRight/
├── production/             <-- Core web platform (Navii AI, CC frontend, research & roadmap)
├── resume_sync_engine/     <-- Automated resume parsing, candidate-job matching, and sync engine
├── skills_suite/           <-- LinkRight AI agent skills (interview coach, network, hunt, portfolio)
├── core_extension/         <-- Browser extension plugin source, design handoffs & specs
├── memory/                 <-- Long-term candidate memory systems & persistence
├── portfolio/              <-- Portfolio generators and showcase templates
└── resumes_vault/          <-- Master resume archives, PDF variants, and profile datasets
```

---

## 2. Key Capabilities
- **Resume Sync Engine**: High-fidelity semantic matching between candidate profiles and job requirements.
- **Interview Coaching**: Automated preparation workflows, rubrics, and feedback generation (`skills_suite/linkright-interview-coach`).
- **Profile Scraping & Intelligence**: LinkedIn profile data extraction for personalized outreach.
