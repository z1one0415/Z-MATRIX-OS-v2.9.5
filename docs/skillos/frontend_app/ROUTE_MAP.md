# Route Map — Z-SkillOS Frontend Dashboard

| # | Route | Page ID | Title | API Endpoint |
|---|-------|---------|-------|-------------|
| 1 | `/` | home_dashboard | Home Dashboard | `/api/dashboard/summary` |
| 2 | `/capabilities` | capabilities | Capability Invocation OS | `/api/capabilities` |
| 3 | `/factor-library` | factor_library | Factor Library | `/api/factor-library/summary` |
| 4 | `/composition-graph` | composition_graph | Composition Graph | `/api/composition-graph/summary` |
| 5 | `/research-report` | research_report | Research Report Node | `/api/research-report/summary` |
| 6 | `/z9-review` | z9_review | Z9 Review Node | `/api/z9-review/summary` |
| 7 | `/evidence-chain` | evidence_chain | Evidence Chain Viewer | `/api/evidence-chain` |
| 8 | `/run-state` | run_state | Run State Registry | `/api/run-state` |
| 9 | `/gate-state` | gate_state | Gate State Registry | `/api/gate-state` |
| 10 | `/audit-trail` | audit_trail | Audit Trail | `/api/audit-trail` |
| 11 | `/safety-boundary` | settings | Settings / Safety | `/api/version` |

## Breadcrumb Rules

- Separator: ` / `
- Home label: `Home` at `/`
- Max depth: 4
- Labels truncated at 30 characters

## Catch-all

- `/*` → redirects to Home Dashboard `/`


> `/settings` is retained as a backward-compatible alias for `/safety-boundary`.
