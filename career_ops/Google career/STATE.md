# Project State

## Active Portal Registry
| Portal ID | Company/ATS | Parser | Status | Last Verified | Notes |
|---|---|---|---|---|---|
| `google` | Google | `google_ds1` | ✅ Live (19 jobs) | 2026-11-11 | SSR GET, no cookies. |
| `greenhouse` | Greenhouse ATS (30 company slugs) | `greenhouse_v1` | ✅ API Confirmed (Figma: 143 jobs) | 2026-11-11 | `boards-api.greenhouse.io` — no auth. |
| `lever` | Lever ATS (slugs TBC) | `lever_v0` | ⚠️ API live, slug list needs verification | 2026-11-11 | Many Lever slugs differ from company names. |
| `ashby` | Ashby ATS (20 company slugs) | `ashby_v1` | ✅ API Confirmed (Supabase: 75 jobs) | 2026-11-11 | Returns `isRemote`, compensation data. |
| `wellfound` | Wellfound | `json_path` | ⏳ Awaiting HAR capture | — | Login required. GraphQL API expected. |
| `himalayas` | Himalayas | `json_path` | ⏳ Awaiting HAR capture | — | No login. Next.js SSR or REST. |
| `remoteok` | Remote OK | `json_path` | ⏳ Check public JSON feed first | — | May not need HAR: `.json` feed exists. |
| `cutshort` | Cutshort | `json_path` | ⏳ Awaiting HAR capture | — | Login required. |
| `instahyre` | Instahyre | `json_path` | ⏳ Awaiting HAR capture | — | Login required. |
| `iimjobs` | IIMjobs | `json_path` | ⏳ Awaiting HAR capture | — | Login required. |
| `linkedin` | LinkedIn | `json_path` | ⏳ Awaiting HAR capture | — | Voyager API, may need MHTML fallback. |
| `otta` | Otta | `json_path` | ⏳ Awaiting HAR capture | — | Login preferred. UK + global remote. |

## Directories & Core Infrastructure
- `01_company_discovery/` — Company signal sources (`hn`, `yc_companies`, `techcrunch`, `inc42`, `surge_peakxv`, `antler`, `producthunt`, `crunchbase`, `the_ken`, `linkedin_funding_posts`, `twitter_founders`, `betalist`) + `companies/master_list.json`
- `02_job_search/track1_linkedin_signals/captures/` — Human hiring post signals
- `02_job_search/track2_company_portals/` — Direct company career portals (`google`, `ashby`, `greenhouse`, `lever`, `_template`)
- `02_job_search/track3_aggregators/` — Job board aggregators (`wellfound`, `himalayas`, `remoteok`, `cutshort`, `instahyre`, `iimjobs`, `otta`, `yc_jobboard`)
- `_secrets/` — AES-256-CBC encrypted credentials + cookies + `registry.json` (gitignored)
- `_shared/dashboard/server.py` — Localhost Auth & Workflow Health Dashboard (`http://127.0.0.1:8765`)
- `N8N_CLOUD_BUILDER_SPEC.md` — Specification for Cloud n8n Builder plugin (4 modular workflows + 4 Data Tables)

## Next Actions
1. Start the Localhost Auth & Workflow Health Dashboard (`python3 _shared/dashboard/server.py --port 8765`) and sign in to cookie-gated portals (LinkedIn Track 1, Wellfound, Cutshort, etc.) via `/auth/start?portal=<id>`.
2. Build `01_company_discovery` scrapers (starting with Hacker News `source.json` public Firebase API) and `score_company.py`.
3. Hand `N8N_CLOUD_BUILDER_SPEC.md` to the Cloud n8n Builder plugin when ready to deploy to n8n Cloud.

