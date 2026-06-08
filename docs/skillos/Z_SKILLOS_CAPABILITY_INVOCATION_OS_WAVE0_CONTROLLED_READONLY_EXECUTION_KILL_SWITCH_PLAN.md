# Wave0 Controlled Read-Only Execution Kill Switch Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_KILL_SWITCH_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Kill Switch Architecture
FUTURE_PLAN_ONLY. Seven-layer kill switch for emergency disable of controlled execution.

| # | Kill Switch | Scope | Default | Override |
|:--|:--|:--|:--|:--|
| 1 | Master Kill | All controlled execution | ACTIVE (True) | Overrides ALL |
| 2 | Runtime Kill | Runtime gate | ACTIVE | Overrides runtime gate |
| 3 | Adapter Framework Kill | Framework gate | ACTIVE | Overrides framework gate |
| 4 | Per-Adapter Kill (github) | GitHub adapter gate | ACTIVE | Overrides github gate |
| 5 | Per-Adapter Kill (docgen) | Doc gen adapter gate | ACTIVE | Overrides docgen gate |
| 6 | Per-Adapter Kill (docs) | Local docs adapter gate | ACTIVE | Overrides docs gate |
| 7 | Per-Adapter Kill (report) | Report reading adapter gate | ACTIVE | Overrides report gate |
| 8 | Evidence Kill | Evidence sink | ACTIVE | Blocks evidence collection |
| 9 | Output Kill | Output generation | ACTIVE | Blocks any output |
| 10 | Emergency Rollback | All systems | ACTIVE | Immediate all-disable |

## Kill Switch Rules
- All kills default active (True = BLOCKED)
- Master kill overrides all other gates regardless of state
- Per-adapter kill overrides individual adapter gate even if master off
- Evidence kill blocks evidence sink independently
- Output kill blocks output generation independently
- Emergency rollback activates all kills simultaneously
- Kill switch check runs before any planned adapter action
- Kill false must not enable anything unless future explicit gate exists

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). P0 kill switch already implemented with master + per-adapter + evidence + output kills.

## Activation Scenarios
- Canary failure → master kill
- Rate limit exceeded → per-adapter kill
- Token leakage → all kills active
- Human-initiated → emergency rollback
- Gate model violation → master kill

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Kill switch plan → permission plan → evidence plan

> Cap OS Wave0 | Controlled Exec Planning | Kill Switch Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED