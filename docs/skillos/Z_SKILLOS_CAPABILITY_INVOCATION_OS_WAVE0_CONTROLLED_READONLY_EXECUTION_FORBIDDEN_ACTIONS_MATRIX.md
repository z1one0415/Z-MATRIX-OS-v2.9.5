# Wave0 Controlled Read-Only Execution Forbidden Actions Matrix

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_FORBIDDEN_ACTIONS_MATRIX_READY
FUTURE_PLAN_ONLY | docs-only | Level 5: BLOCKED

| # | Forbidden Action | Severity | Scope |
|:--|:--|:--:|:--|
| 1 | Runtime enablement | CRITICAL | Permanent until Level 5 gate |
| 2 | Adapter execution enablement | CRITICAL | Permanent until explicit gate |
| 3 | Capability execution | CRITICAL | Permanent until Level 5 gate |
| 4 | Real adapter call | CRITICAL | Permanent until canary gate |
| 5 | GitHub call | CRITICAL | Permanent until separate gate |
| 6 | Network call | CRITICAL | Permanent until read gate |
| 7 | File write | HIGH | Permanent until explicit gate |
| 8 | Branch mutation | HIGH | Permanent |
| 9 | Merge | HIGH | Permanent without review |
| 10 | External publish | CRITICAL | Permanent |
| 11 | Z-MATRIX call | CRITICAL | Permanent |
| 12 | Production / broker / real_trade | CRITICAL | Permanent (Level 5) |
| 13 | Level 5 behavior | CRITICAL | Permanent |

> Cap OS Wave0 | Controlled Exec Planning | Forbidden Actions | 13 items | FUTURE_PLAN_ONLY