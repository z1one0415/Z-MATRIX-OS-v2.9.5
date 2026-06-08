# Wave0 Controlled Read-Only Execution Rollback Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_ROLLBACK_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Rollback Architecture
FUTURE_PLAN_ONLY. Complete rollback plan for controlled read-only execution.

## Rollback Actions (in sequence)
| Step | Action | Effect | Reversible |
|:--:|:--|:--|:--:|
| 1 | Activate master kill switch | All gates disabled immediately | Yes (deactivate kill) |
| 2 | All per-adapter kills active | Individual adapter gates blocked | Yes (deactivate kill) |
| 3 | Evidence kill active | Evidence sink blocked | Yes (deactivate kill) |
| 4 | Output kill active | Output generation blocked | Yes (deactivate kill) |
| 5 | All adapter requested flags ignored | No intent recorded | Yes (re-request) |
| 6 | Config reset to default | All enabled→False | Yes (reconfigure) |
| 7 | Evidence sink flushed | In-memory evidence cleared | No (data lost) |
| 8 | Docs-only fallback | Return to planning state | Yes |

## Rollback Triggers
| # | Trigger | Severity | Action |
|:--|:--|:--:|:--|
| T1 | Canary failure (any phase) | HIGH | Steps 1-8, full rollback |
| T2 | Gate model violation detected | CRITICAL | Steps 1-5, gates→disabled |
| T3 | Permission bypass detected | CRITICAL | Steps 1-5, permissions→all denied |
| T4 | Evidence inconsistency | MEDIUM | Steps 3,7, evidence reset |
| T5 | Human-initiated rollback | ANY | Steps 1-8, full rollback |
| T6 | Rate limit exceeded | MEDIUM | Steps 2, per-adapter kill |
| T7 | Token leakage | CRITICAL | Steps 1-8, all kills, full rollback |
| T8 | Unexpected adapter behavior | HIGH | Steps 1-5, gates→disabled |

## Rollback Safety
- No data migration (read-only has no data to migrate)
- No external cleanup (no external state to clean)
- No files created (evidence is in-memory only)
- No network state to reverse
- Rollback is atomic (kill switch is instant)
- Rollback is reversible (deactivate kills → recover)

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4).

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Rollback plan → test & proof plan → forbidden actions

> Cap OS Wave0 | Controlled Exec Planning | Rollback Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED