# Wave0 Controlled Read-Only Execution P1 Canary Forbidden Actions Matrix

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_FORBIDDEN_ACTIONS_MATRIX_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED | Items: 18

### Tier 1: Execution Enablement (CRITICAL)
| # | Action | Severity | Detection |
|:--:|:--|:--:|:--|
| 1 | Runtime enablement | CRITICAL | CI: enabled()==False check |
| 2 | Adapter execution enablement | CRITICAL | CI: triple gate→PLAN_ONLY |
| 3 | Capability execution | CRITICAL | CI: no EXECUTE action |

### Tier 2: External Communication (CRITICAL)
| # | Action | Severity | Detection |
|:--:|:--|:--:|:--|
| 4 | Real adapter call | CRITICAL | CI: no adapter invocation |
| 5 | Real GitHub call | CRITICAL | CI: no requests/urllib/httpx |
| 6 | Network call | CRITICAL | CI: no socket/httpx |

### Tier 3: File System / Branch (HIGH)
| # | Action | Severity | Detection |
|:--:|:--|:--:|:--|
| 7 | File write | HIGH | CI: FS unchanged check |
| 8 | Branch mutation | HIGH | CI: git status check |
| 9 | Merge (without review) | HIGH | Gate flow enforcement |
| 10 | External publish | CRITICAL | CI: no POST to external |

### Tier 4: Module Boundary (CRITICAL)
| # | Action | Severity | Detection |
|:--:|:--|:--:|:--|
| 11 | Z-MATRIX module calling | CRITICAL | CI: grep z2/z8/z9/v3 |
| 12 | Z-MATRIX module adapter | CRITICAL | CI: grep worldblocks/dealcompass |

### Tier 5: Safety/Language (CRITICAL)
| # | Action | Severity | Detection |
|:--:|:--|:--:|:--|
| 13 | Warning enablement | MEDIUM | CI: no caller-visible warning |
| 14 | Caller-visible warning | MEDIUM | CI: decision no warning fields |
| 15 | Result_envelope mutation | HIGH | CI: no envelope fields |
| 16 | Blocking / fail-closed | HIGH | CI: degrade instead of block |
| 17 | Production / broker / real_trade | CRITICAL | CI: grep for references |
| 18 | Level 5 behavior | CRITICAL | CI: Level 5 BLOCKED check |

### Summary: 18 items (10 CRITICAL, 4 HIGH, 2 MEDIUM, 0 LOW) + 2 doc-only

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f).

## Boundary
No runtime enablement. No adapter execution enablement. Level 5 BLOCKED.

> Cap OS Wave0 | Controlled Exec P1 Canary | Forbidden Actions | 18 items | FUTURE_PLAN_ONLY | Level 5 BLOCKED