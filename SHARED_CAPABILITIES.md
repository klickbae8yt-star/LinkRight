# Cross-Project Shared Capabilities & Data Flows

This document details how data models, extraction engines, and intelligence pipelines are shared across **AutoFlow**, **Miraya**, **LinkRight**, and **Dropshipping**.

## 1. Architectural Dependency Graph

```mermaid
graph TD
    subgraph DataEngine ["Shared Data & Extraction Engines"]
        SE["SerpAPI & LinkedIn Scraping Engine"]
        LLM["LLM Pool & Prompt Rubrics (Intent, Voice, Scoring)"]
        LeadDB["Lead & Profile Datasets (MongoDB / CSVs)"]
    end

    subgraph AutoFlow ["AutoFlow Engine (Platform)"]
        AF_Node["n8n Crawlers & Reusable Workflow Nodes"]
        AF_Blue["Industry Automation Blueprints"]
    end

    subgraph Miraya ["Miraya Media House (Agency)"]
        M_Brand["Influencer Outreach & D2C Brand Deals"]
        M_Personal["Personal Branding Pipeline (Dogfooding Satvik #0)"]
        M_Content["30-Day LinkedIn & Content Production"]
    end

    subgraph LinkRight ["LinkRight (Career & Candidate Suite)"]
        LR_Recruit["Recruiter & Hiring Manager Profile Enrichment"]
        LR_Resume["Resume Synchronization & Shortlist Optimization"]
        LR_Interview["Targeted Networking & Outreach Tracking"]
    end

    subgraph Dropshipping ["Dropshipping / Dwelo (E-commerce)"]
        DS_Trend["Social Trend Analysis & Sprinklr Data"]
        DS_Store["Product Discovery & E-com Operations"]
    end

    %% Dependencies
    AF_Node -->|Orchestrates| SE
    AF_Node -->|Orchestrates| LLM
    
    SE -->|Prospect Leads| LeadDB
    LeadDB -->|D2C Founders| M_Brand
    LeadDB -->|Recruiters & Talent| LR_Recruit
    
    LLM -->|Voice Authenticity| M_Content
    LLM -->|Career Narratives| LR_Resume
    LLM -->|Creator Pitch Outlines| M_Personal

    SE -.->|Viral Product Signals| DS_Trend
```

## 2. Shared Assets Matrix

| Asset / Engine | Primary Producer | Consuming Projects | Usage in Consumer |
| :--- | :--- | :--- | :--- |
| **LinkedIn Profile Scraper** | LinkRight / `growth/linkedin_snippet` | Miraya & LinkRight | Founder discovery for Miraya; Recruiter profile intelligence for LinkRight. |
| **Lead Scoring & Intent Rubrics** | AutoFlow (`MIRAYA-EVAL-*`) | Miraya & LinkRight | Classifying prospect email replies (Miraya); evaluating recruiter messages (LinkRight). |
| **30-Day Authority Content Engine** | Miraya (`growth/30_day_engine`) | Miraya & Personal Branding | Agency inbound pipeline; personal brand dogfooding for Satvik (#0). |
| **Resume & Skill Parsers** | LinkRight (`resume_sync_engine`) | LinkRight & Miraya | Candidate shortlisting (LinkRight); internal agency hiring evaluations (Miraya `operations/hiring`). |
