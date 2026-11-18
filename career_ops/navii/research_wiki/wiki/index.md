# Navii Second Brain — Index

Knowledge base built from: Navii company/LinkedIn data, Saurabh Palan (co-founder/CTO) LinkedIn data, Aakanksha Upadhyay (team) LinkedIn data. Source CSVs: `Navii_Linkedin.csv`, `Saurabh_Linkedin.csv`, `Aakanksha_Linkedin.csv` (from `/Users/satvikjain/Downloads/Navii_Voice`), plus web pages for heynavii.ai and LinkedIn profiles.

## Entities
- [[navii]]
- [[saurabh-palan]]
- [[aakanksha-upadhyay]]

## Concepts
- [[professional-agent-network]]
- [[ai-career-agent]]
- [[voice-based-candidate-screening]]

## Sources
- [[navii-website]]
- [[navii-linkedin-company]]
- [[navii-linkedin-posts]] (62 posts)
- [[saurabh-palan-profile]]
- [[saurabh-palan-linkedin-posts]] (212 posts)
- [[aakanksha-upadhyay-profile]]
- [[aakanksha-upadhyay-linkedin-posts]] (147 posts)

## Notes on this build
These entity/concept pages were authored by hand in the format the **Karpathy LLM Wiki** plugin generates (frontmatter: type/created/updated/sources/tags/aliases/reviewed; sections: Basic Information, Description, Related Entities, Related Concepts, Mentions in Source), because the plugin itself has no CLI/API — it only runs interactively inside Obsidian via the command palette, gated behind a configured LLM provider ("llmReady guard"). To extend this wiki automatically:

1. Open the `linkright_production` vault in Obsidian.
2. Enable **Karpathy LLM Wiki** under Settings → Community plugins (already unzipped into `.obsidian/plugins/karpathywiki`, added to `community-plugins.json`).
3. Configure an LLM provider + API key in the plugin settings and hit "Test Connection."
4. Run **"Ingest from folder"** on `Navii/sources/` to auto-generate/refresh richer entity & concept pages, or **"Ingest current file"** on any single source note.
5. Run **"Lint wiki"** periodically to catch duplicates/dead links/orphans, and **"Regenerate index"** to refresh this file automatically.

Pages here have `reviewed: false` — the plugin will safely extend/refresh them (only `reviewed: true` pages are protected from being overwritten).
