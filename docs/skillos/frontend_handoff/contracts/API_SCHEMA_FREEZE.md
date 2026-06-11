# API Schema Freeze — A1 Contract

## Status: FROZEN

- **Seal**: A1_CONTRACT_FREEZE
- **Version**: v0.1.0-rc
- **Contract File**: `skillos/frontend_handoff/contracts/api_schema.json`
- **Frozen Date**: 2026-06-12

## Summary

The Z-SkillOS frontend API schema defines 15 GET-only endpoints. All mutation operations (POST/PUT/PATCH/DELETE) return `{"status":"BLOCKED","reason":"readonly_disabled_default"}`.

## Endpoint Inventory

| # | Endpoint | Description |
|:--|:--|:--|
| 1 | GET /api/health | System health check |
| 2 | GET /api/version | Version and contract info |
| 3 | GET /api/dashboard/summary | Dashboard overview |
| 4 | GET /api/capabilities | Capability catalog |
| 5 | GET /api/factor-library/summary | Factor seal status |
| 6 | GET /api/composition-graph/summary | Graph node/edge status |
| 7 | GET /api/research-report/summary | Report preview |
| 8 | GET /api/z9-review/summary | Review queue |
| 9 | GET /api/evidence-chain | Evidence traversal |
| 10 | GET /api/run-state | Pipeline run status |
| 11 | GET /api/gate-state | Gate matrix |
| 12 | GET /api/audit-trail | Audit log |
| 13 | GET /api/frontend/routes | Route index |
| 14 | GET /api/frontend/contracts | Contract index |
| 15 | GET /api/health (also counted) | — |

## Error Formats

| Format | HTTP Status | Use Case |
|:--|:--|:--|
| standard_error | 400, 404, 408, 429, 500, 503, 504 | Standard error responses |
| blocked_error | 403 | Safety/policy blocked actions |
| degraded_error | 200 (degraded) | Partial data responses |

## Blocked Methods

All non-GET HTTP methods are globally blocked:
- POST → `{"status":"BLOCKED","reason":"readonly_disabled_default"}`
- PUT → `{"status":"BLOCKED","reason":"readonly_disabled_default"}`
- PATCH → `{"status":"BLOCKED","reason":"readonly_disabled_default"}`
- DELETE → `{"status":"BLOCKED","reason":"readonly_disabled_default"}`

## Forbidden Fields

The following fields MUST NOT appear in any API response or request body:
- `buy`, `sell`, `order`, `position`
- `broker_action`, `runtime_enable`, `production_enable`
- `paper_trading_start`, `alpha_claim`

## Component Status

All endpoint responses from `research_report` and `z9_review` respect:
- `generation_enabled`: `false` (const)
- `review_enabled`: `false` (const)
- `disabled_default`: `true` (const)

All capability endpoints enforce:
- `enabled_count`: `0` (const)
- `readonly`: `true` (const)

## Compliance Verification

- [x] All endpoints are GET-only
- [x] No buy/sell/order/position fields
- [x] No broker_action/runtime_enable/production_enable/paper_trading_start/alpha_claim
- [x] All mutation defaults to disabled/blocked
- [x] Blocked error format defined for all mutation attempts
- [x] research_report and z9_review nodes default to disabled
