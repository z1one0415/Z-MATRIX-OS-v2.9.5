# Wave0 Controlled Read-Only Execution P1 Canary Permission Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_PERMISSION_PLAN_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED

## Permission Model
FUTURE_PLAN_ONLY. Strict permission model for P1 canary. Read-only only. Write/production/broker/real_trade all denied.

### Allowed Permissions (future, gated)
| Permission | Scope | Gate Required |
|:--|:--|:--|
| READ_ONLY | Read existing local resources (provided-input) | Permission gate + adapter gate + input source gate |
| GENERATION_ONLY | In-memory generation, no file write | Permission gate + output kill off |

### Denied Permissions (always)
| Permission | Reason | Severity |
|:--|:--|:--:|
| WRITE | No file/branch mutation | HIGH |
| BRANCH_MUTATION | No branch modifications | HIGH |
| MERGE | No merge operations | HIGH |
| PUBLISH | No external publish | CRITICAL |
| PRODUCTION | No production access | CRITICAL |
| BROKER | No broker access | CRITICAL |
| REAL_TRADE | No real trade access | CRITICAL |
| NETWORK | No network calls (unless future explicit read gate) | CRITICAL |
| Z_MATRIX_MODULE | No Z-MATRIX module calls | CRITICAL |
| FILE_WRITE | No file system writes | HIGH |
| EXTERNAL | No external source processing | CRITICAL |
| GITHUB_METADATA | No GitHub real call (separate gate required) | CRITICAL |

### Permission Rules
- Unknown permission = denied
- Missing permission = denied
- Generation-only is non-execution
- All denied unless future explicit gate
- Permission check runs after gate evaluation
- Permission denial is non-blocking (returns DENY, not exception)

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f).

## Boundary
No runtime enablement. No adapter execution enablement. Level 5 BLOCKED.

> Cap OS Wave0 | Controlled Exec P1 Canary | Permission Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED