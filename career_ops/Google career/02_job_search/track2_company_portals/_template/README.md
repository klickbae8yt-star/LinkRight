# Adding a New Career Portal

1. Copy `portals/_template` to `portals/<company_slug>`.
2. Save Chrome DevTools network capture (HAR) inside `portals/<company_slug>/captures/`.
3. Run:
   `python3 scripts/har_to_api.py analyze --har "portals/<company_slug>/captures/<file>.har" --portal <company_slug> --company "<Company Name>" --scaffold`
4. Review generated `portal.json` and set `"enabled": true`.
5. Test locally and rebuild the unified n8n workflow:
   `python3 scripts/run_portals.py --dry-run`
   `python3 scripts/build_workflow.py`

