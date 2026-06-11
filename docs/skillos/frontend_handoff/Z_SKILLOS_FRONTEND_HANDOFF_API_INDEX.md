# Z-SkillOS Frontend Handoff API Index

## Version: v0.1.0-rc

## All endpoints are GET-only. No POST/PUT/PATCH/DELETE.
## All mutation endpoints return {"status":"BLOCKED","reason":"readonly_disabled_default"}

## Health & Version
- GET /api/health — {"status":"ok","version":"v0.1.0-rc"}
- GET /api/version — Version info

## Dashboard
- GET /api/dashboard/summary — dashboard_summary.json fixture

## Capability OS
- GET /api/capabilities — capability_list.json fixture

## Factor Library
- GET /api/factor-library/summary — factor_library_summary.json fixture

## Composition Graph
- GET /api/composition-graph/summary — composition_graph_summary.json fixture

## Research Report
- GET /api/research-report/summary — research_report_summary.json fixture

## Z9 Review
- GET /api/z9-review/summary — z9_review_summary.json fixture

## Evidence Chain
- GET /api/evidence-chain — evidence_chain_demo.json fixture

## State Registry
- GET /api/run-state — run_state_demo.json fixture
- GET /api/gate-state — gate_state_demo.json fixture

## Audit
- GET /api/audit-trail — audit_trail_demo.json fixture

## Frontend
- GET /api/frontend/routes — route index
- GET /api/frontend/contracts — contract index
