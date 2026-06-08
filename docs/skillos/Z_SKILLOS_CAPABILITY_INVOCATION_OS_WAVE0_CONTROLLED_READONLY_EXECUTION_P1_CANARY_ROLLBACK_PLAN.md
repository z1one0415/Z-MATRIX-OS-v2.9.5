# Wave0 Controlled Read-Only Execution P1 Canary Rollback Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_ROLLBACK_PLAN_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED

## Rollback Actions (8 steps)
FUTURE_PLAN_ONLY. Complete rollback plan for P1 canary.

| Step | Action | Effect | Reversible |
|:--:|:--|:--|:--:|
| 1 | Activate master kill switch | All canary gates disabled immediately | Yes (deactivate kill) |
| 2 | All per-adapter kills active | Individual adapter gates blocked | Yes (deactivate) |
| 3 | P1 canary kill active | P1 canary gate blocked | Yes (deactivate) |
| 4 | Evidence kill active | Evidence sink blocked | Yes (deactivate) |
| 5 | Output kill active | Output generation blocked | Yes (deactivate) |
| 6 | All requested flags ignored | No intent recorded | Yes (re-request) |
| 7 | Config reset to default | All enabled→False | Yes (reconfigure) |
| 8 | Docs-only fallback | Return to planning state | Yes (re-plan) |

### Rollback Triggers (8)
| Trigger | Severity | Action |
|:--:|:--:|:--|
| Canary failure (any phase) | HIGH | Steps 1-8, full rollback |
| Gate model violation | CRITICAL | Steps 1-5, gates→disabled |
| Permission bypass detected | CRITICAL | Steps 1-5, permissions→all denied |
| Evidence inconsistency | MEDIUM | Steps 4,7, evidence reset |
| Human-initiated rollback | ANY | Steps 1-8, full rollback |
| Rate limit exceeded | MEDIUM | Step 2, per-adapter kill |
| Token leakage | CRITICAL | Steps 1-8, all kills |
| Unexpected adapter behavior | HIGH | Steps 1-5, gates→disabled |

### Rollback Safety
- No data migration (read-only has no data)
- No external cleanup (no external state)
- No files created (evidence in-memory only)
- No network state to reverse
- Rollback is atomic (kill switch instant)
- Rollback is reversible (deactivate kills → recover)

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f).

## Boundary
No runtime enablement. No adapter execution enablement. Level 5 BLOCKED.

> Cap OS Wave0 | Controlled Exec P1 Canary | Rollback Plan | 8 steps, 8 triggers | FUTURE_PLAN_ONLY | Level 5 BLOCKED