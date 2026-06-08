# Wave0 Controlled Read-Only Execution P1 Canary Input Matrix Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_INPUT_MATRIX_PLAN_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED

## Input Source Matrix
FUTURE_PLAN_ONLY. Defines allowed input sources and their gate requirements.

### Input Sources
| Source | Canary Phase | Sample Size | Gate Required | Status in P1 |
|:--|:--:|:--:|:--|:--:|
| Synthetic | Phase 1 | 5 invocations | Input source gate (synthetic) | ALLOWED (plan only) |
| Provided (human) | Phase 2 | 5 invocations | Input source gate (provided) | ALLOWED (plan only) |
| Local Sandbox | Phase 3 | 10 reads | Input source gate (sandbox) | ALLOWED (plan only) |
| External Source | — | — | Input source gate (external) | **REJECTED** |
| GitHub Metadata | — | — | Input source gate + separate GitHub gate | **REJECTED** |
| Z-MATRIX | — | — | Input source gate + Z-MATRIX gate | **PERMANENTLY REJECTED** |

### Input Rules
1. Cannotary starts with synthetic input only
2. Provided input only after synthetic canary succeeds
3. Local sandbox only after provided canary succeeds
4. External source rejected in all P1 canary phases
5. GitHub metadata requires separate gate (not in P1 scope)
6. Z-MATRIX permanently forbidden
7. Failure in current input class rolls back to synthetic

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f).

## Boundary
No runtime enablement. No adapter execution enablement. No external source. No GitHub. Level 5 BLOCKED.

> Cap OS Wave0 | Controlled Exec P1 Canary | Input Matrix | FUTURE_PLAN_ONLY | Level 5 BLOCKED