# Factor Library Read-Only Adapter Planning — Merge Risk Register

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_MERGE_RISK_REGISTER_READY
Level 5: BLOCKED | Items: 12

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|:--:|:--|:--:|:--:|:--|:--|:--|
| MR1 | Merge to wrong branch | CRITICAL | Low | Pre-merge branch verify | git branch --show-current | git reset --hard |
| MR2 | Force-push overwrites history | CRITICAL | Low | No --force flag | Branch protection | Restore ref |
| MR3 | Non-doc file creep (research/factor_library leaks) | HIGH | Low | git diff --stat verify | CI whitelist check | Revert merge |
| MR4 | Test regression on postmerge | HIGH | Low | 218 test baseline | CI test suite | Revert |
| MR5 | Concurrent merge conflicts | MEDIUM | Low | Sequential execution | Gate lock | git merge --abort |
| MR6 | Research files modified during planning | HIGH | Medium | grep for research/ before merge | CI research file check | Block merge |
| MR7 | Post-merge seal not created | HIGH | Low | Same commit sequence | Seal presence check | Retroactive seal |
| MR8 | Authorization creep (planning→impl) | CRITICAL | Low | FUTURE_PLAN_ONLY in docs | Automated grep | Revert |
| MR9 | A1/B1 merge before factor alignment | CRITICAL | Medium | Dependency gate | Merge order CI | Revert A1/B1 |
| MR10 | Merge before review pass | HIGH | Low | Gate presence check | Automated check | Block |
| MR11 | Missing canonical intent in merge diff | MEDIUM | Low | Intent coverage diff check | CI grep for intents | Revert if missing |
| MR12 | Blocked output cannot be removed retroactively | MEDIUM | Low | Ensure filters in adapter contract before impl | Contract check gate | Block merge |

**Summary**: 3 CRITICAL | 4 HIGH | 3 MEDIUM | 2 LOW

> Factor Library | Planning | Merge Risk Register | 12 items | Level 5 BLOCKED
## Evidence
- Parent baseline: d02b60c9 (V13.F5.1.2.1 accepted)
- Impact review: 22252711 (APPROVE_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING)
- Batch3 factors: F21, F22, F24, F26, F27, F30, F31, F34
- 8 canonical intents with 4 legacy aliases
- 7 forbidden intents (ALPHA_SIGNAL through PRODUCTION)
- C1 evidence schema compatible (no rework)
- A1/B1 blocked until alignment

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file/read write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No tag. Level 5 remains BLOCKED.

## Next
Human merge approval decision only. After merge: A1 hardening -> B1 hardening.
