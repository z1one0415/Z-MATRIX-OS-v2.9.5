# Wave0 Controlled Read-Only Execution Forbidden Actions Matrix

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_FORBIDDEN_ACTIONS_MATRIX_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Forbidden Actions (15 items, 5 tiers)

### Tier 1: Execution Enablement (CRITICAL — permanent block)
| # | Action | Severity | Scope | Detection |
|:--|:--|:--:|:--|:--|
| 1 | Runtime enablement | CRITICAL | Permanent until Level 5 gate | CI: enabled()==False check |
| 2 | Adapter execution enablement | CRITICAL | Permanent until explicit gate | CI: triple gate→PLAN_ONLY only |
| 3 | Capability execution | CRITICAL | Permanent until Level 5 gate | CI: no EXECUTE action |

### Tier 2: External Communication (CRITICAL)
| # | Action | Severity | Scope | Detection |
|:--|:--|:--:|:--|:--|
| 4 | Real adapter call | CRITICAL | Permanent until canary gate | CI: no adapter.call() |
| 5 | Real GitHub call | CRITICAL | Permanent until separate gate | CI: no requests/urllib |
| 6 | Network call | CRITICAL | Permanent until read gate | CI: no socket/httpx |
| 7 | External publish | CRITICAL | Permanent | CI: no POST to external |

### Tier 3: File System (HIGH)
| # | Action | Severity | Scope | Detection |
|:--|:--|:--:|:--|:--|
| 8 | File write | HIGH | Permanent until explicit gate | CI: FS unchanged check |
| 9 | Branch mutation | HIGH | Permanent | CI: git status check |
| 10 | Merge (without review) | HIGH | Permanent | Gate flow enforcement |
| 11 | runtime_audit/runtime_reports/data | HIGH | Permanent | CI: dir absence check |

### Tier 4: Module Boundary (CRITICAL)
| # | Action | Severity | Scope | Detection |
|:--|:--|:--:|:--|:--|
| 12 | Z-MATRIX module calling | CRITICAL | Permanent | CI: grep z2/z8/z9/v3 |
| 13 | Z-MATRIX module adapter | CRITICAL | Permanent | CI: grep worldblocks/dealcompass |

### Tier 5: Safety Boundary (CRITICAL — Level 5 permanent)
| # | Action | Severity | Scope | Detection |
|:--|:--|:--:|:--|:--|
| 14 | Production / broker / real_trade | CRITICAL | Permanent (Level 5) | CI: grep production/broker |
| 15 | Level 5 behavior | CRITICAL | Permanent | CI: Level 5 BLOCKED check |

## Summary
| Tier | Items | Severity |
|:--|:--:|:--|
| T1: Execution Enablement | 3 | CRITICAL |
| T2: External Communication | 4 | CRITICAL |
| T3: File System | 4 | HIGH |
| T4: Module Boundary | 2 | CRITICAL |
| T5: Safety Boundary | 2 | CRITICAL |
| **Total** | **15** | **11 CRITICAL, 4 HIGH** |

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4).

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Forbidden actions matrix → closeout → seal

> Cap OS Wave0 | Controlled Exec Planning | Forbidden Actions | 15 items | FUTURE_PLAN_ONLY | Level 5 BLOCKED