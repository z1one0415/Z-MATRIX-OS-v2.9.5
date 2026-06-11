# Error, Abort & Degraded UI Contract — A1 Contract

## Status: FROZEN

- **Seal**: A1_CONTRACT_FREEZE
- **Version**: v0.1.0-rc
- **Contract File**: `skillos/frontend_handoff/contracts/error_abort_degraded_contract.json`
- **Frozen Date**: 2026-06-12

## Error Codes (17 codes, 3 categories)

### Client Errors (4xx — 7 codes)
| Code | HTTP | Message | Retry |
|:--|:--|:--|:--:|
| ERR_BAD_REQUEST | 400 | Malformed request | No |
| ERR_UNAUTHORIZED | 401 | Auth required | No |
| ERR_FORBIDDEN | 403 | Permission denied | No |
| ERR_NOT_FOUND | 404 | Resource not found | No |
| ERR_METHOD_BLOCKED | 405 | HTTP method blocked | No |
| ERR_TIMEOUT | 408 | Request timed out | Yes |
| ERR_TOO_MANY_REQUESTS | 429 | Rate limit exceeded | Yes |

### Server Errors (5xx — 3 codes)
| Code | HTTP | Message | Retry |
|:--|:--|:--|:--:|
| ERR_INTERNAL | 500 | Internal server error | Yes |
| ERR_SERVICE_UNAVAILABLE | 503 | Service unavailable | Yes |
| ERR_GATEWAY_TIMEOUT | 504 | Upstream timeout | Yes |

### Safety Errors (4xx — 4 codes)
| Code | HTTP | Message | Retry |
|:--|:--|:--|:--:|
| ERR_SAFETY_BLOCKED | 403 | Safety boundary enforced | No |
| ERR_READONLY_MODE | 403 | Read-only mode | No |
| ERR_DISABLED_DEFAULT | 403 | Feature disabled by default | No |
| ERR_CONTRACT_VIOLATION | 403 | Contract violation | No |

## Abort Reasons (7 reasons)

| Code | Severity | Recoverable |
|:--|:--|:--:|
| ABORT_SAFETY_GATE_FAILED | critical | No |
| ABORT_CONTRACT_VIOLATION | critical | No |
| ABORT_TIMEOUT | warning | Yes |
| ABORT_DEPENDENCY_FAILURE | error | Yes |
| ABORT_MANUAL | info | No |
| ABORT_PERMISSION_DENIED | critical | No |
| ABORT_EVIDENCE_CHAIN_BROKEN | critical | No |

## Degraded States (5 states)

| Code | Severity | Auto-Recover | Color |
|:--|:--|:--:|:--:|
| DEGRADED_PARTIAL_DATA | warning | Yes | amber |
| DEGRADED_HASH_VERIFICATION | warning | Yes | amber |
| DEGRADED_GRAPH_RENDERER | info | Yes | amber |
| DEGRADED_AUDIT_HISTORY | info | Yes | amber |
| DEGRADED_COMPONENT_UNREACHABLE | error | Yes | red |

## Permanently Blocked Actions (46 actions)

All actions across all pages are permanently blocked. Categorized by page:
- **Dashboard**: start/stop pipeline, enable/disable skill, modify config
- **Capabilities**: invoke/enable/disable/configure/promote skill
- **Factor Library**: create/modify/delete/promote factor, advance_f8, unseal
- **Composition Graph**: add/remove node/edge, modify graph, reconfigure flow
- **Research Report**: generate/modify/delete report, promote, set confidence
- **Z9 Review**: start/submit/approve/reject review, modify criteria
- **Evidence Chain**: modify/delete/inject evidence, tamper hash
- **Run State**: start/stop/abort/retry run, modify config
- **Gate State**: open/close/bypass gate, modify rules
- **Audit Trail**: modify/delete/redact/purge
- **Settings**: modify permissions, enable runtime/production/paper trading, modify safety boundary, change contract

## UI Treatment Matrix

| Error Type | UI Component | Interactive |
|:--|:--|:--|
| Transient error (timeout, 5xx) | error_card with retry button | Yes |
| Permanent error (4xx validation) | error_card without retry | No |
| Permission denied | blocked_overlay | No |
| Disabled feature | blocked_overlay | No |
| Partial data | degraded_badge (non-blocking) | Yes (partial) |
| Safety blocked | blocked_overlay | No |

## Compliance Verification

- [x] 17 error codes across 3 categories
- [x] 7 abort reasons with severity levels
- [x] 5 degraded states with auto-recovery flags
- [x] 46 permanently blocked actions
- [x] All blocked actions are mutation/execution actions
- [x] No forbidden fields in any code definition
