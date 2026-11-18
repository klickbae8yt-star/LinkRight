# Rules & Lessons

## Entry Template
- **mistake / situation:** What happened and where.
- **root_cause:** Why it happened.
- **prevention_rule:** What to do every time.
- **added_on:** YYYY-MM-DD

## Lessons Logged
- **situation:** n8n 2.34.6 `@n8n/task-runner` threw `ReferenceError: URLSearchParams is not defined` inside Code node `Parse ds:1 jobs`.
  - **root_cause:** n8n 2.x runs Code nodes inside an isolated `node:vm` context without Web/Node globals like `URLSearchParams`, `URL`, or `fetch`.
  - **prevention_rule:** Use pure ECMAScript `encodeURIComponent` in n8n Code nodes and always unit-test Code nodes via `tests/test_framework.mjs` inside a strict `node:vm` context.
  - **added_on:** 2026-11-10
- **situation:** Adding `Schedule Trigger` caused `Fetch Google Careers` and `Parse ds:1 jobs` to fail because they referenced `$('Run Search').first()`.
  - **root_cause:** Reaching back to a trigger node that did not run on scheduled executions crashes the node.
  - **prevention_rule:** Resolve trigger inputs inside `Config` using `$json` immediately after all triggers, and have downstream nodes read `$('Config')` or `$('Portal Registry')` only.
  - **added_on:** 2026-11-11

