# Z-SkillOS Capability Invocation OS Permission Model Implementation Plan

## Status
Z_SKILLOS_PERMISSION_MODEL_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Tier enforcement implementation plan.

## Tier Definitions (T0-T5)
- T0 docs-only: auto-granted, no evidence required
- T1 analysis-only: auto-granted, evidence required
- T2 code/local: permission required, evidence required
- T3 advisory: human approval required, evidence required
- T4 external: human approval required, evidence required, rollback plan
- T5 blocked: NEVER GRANTED, no path, no override, no bypass

## Escalation Matrix
| From→To | T1 | T2 | T3 | T4 | T5 |
| T0 | Auto | Permission | Human | Human+Rollback | DENY |
| T1 | — | Permission | Human | Human+Rollback | DENY |
| T2 | — | — | Human | Human+Rollback | DENY |
| T3 | — | — | — | Human+Rollback | DENY |
| T4 | — | — | — | — | DENY |

## Enforcement Rules
- Deny-by-default: no permission = deny
- Immutable tier: tier cannot be downgraded at runtime
- Tier audit: every tier decision logged
- Drift check: periodic tier re-evaluation
- Human override: human can escalate tier up (never down)
- Rollback trigger: T5 invocation attempt → immediate deny + audit + alert

## No implementation. Level 5 remains BLOCKED.
