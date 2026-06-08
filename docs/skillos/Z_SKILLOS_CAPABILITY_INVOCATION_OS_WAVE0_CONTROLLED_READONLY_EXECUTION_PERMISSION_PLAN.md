# Wave0 Controlled Read-Only Execution Permission Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_PERMISSION_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Permission Model
FUTURE_PLAN_ONLY. Strict permission model for controlled read-only execution.

## Allowed Permissions (future, gated)
| Permission | Scope | Gate Required |
|:--|:--|:--|
| READ_ONLY | Read existing local resources | Permission gate + adapter gate |
| GENERATION_ONLY | In-memory generation only, no file write | Permission gate + output kill off |

## Denied Permissions (always)
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
| EXTERNAL_PUBLISH | No publishing to external services | CRITICAL |

## Permission Rules
- Unknown permission = denied (default-deny)
- Missing permission = denied
- Generation-only is non-execution (does not trigger adapter call)
- All denied unless future explicit gate
- Permission check runs after gate evaluation, before any action
- Permission denial is non-blocking (returns DENY, not exception)

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). P0 permissions already implement all-denied default.

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Permission plan → evidence plan → adapter priority

> Cap OS Wave0 | Controlled Exec Planning | Permission Plan | FUTURE_PLAN_ONLY | Level 5 BLOCKED