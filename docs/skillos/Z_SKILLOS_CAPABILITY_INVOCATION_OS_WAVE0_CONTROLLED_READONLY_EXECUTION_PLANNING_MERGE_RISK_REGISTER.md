# Wave0 Controlled Read-Only Execution Planning Merge Risk Register

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_PLANNING_MERGE_RISK_REGISTER_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED | Items: 10

| # | Risk | Severity | Likelihood | Mitigation | Future Control | Rollback Trigger |
|:--|:--|:--:|:--:|:--|:--|:--|
| MR1 | Merge to wrong branch | CRITICAL | Low | Pre-merge branch verify: git branch --show-current | Automated branch guard | git reset --hard pre-merge |
| MR2 | Force-push overwrites history | CRITICAL | Low | Strict no-force-push policy | Branch protection | Restore from backup ref |
| MR3 | Non-doc files creep into merge | HIGH | Low | git diff --stat verify: only docs/skillos/*CONTROLLED* | CI diff boundary check | Revert merge |
| MR4 | Post-merge test regression | HIGH | Low | Regression: 374 test baseline | CI test suite | Revert merge |
| MR5 | Concurrent merge conflicts | MEDIUM | Low | Sequential gate execution | Gate lock mechanism | git merge --abort |
| MR6 | Docs stale or incomplete after merge | MEDIUM | Medium | Post-merge seal with source SHA | Hash verification | Docs review cycle |
| MR7 | Merge message unclear for audit | LOW | Low | Standard merge message format | Message template | Amend message |
| MR8 | Authorization creep (read as enablement) | CRITICAL | Low | Every doc: FUTURE_PLAN_ONLY, Level 5 BLOCKED | Automated grep for authorized | Revert + rewrite |
| MR9 | Post-merge seal not created | HIGH | Low | Post-merge seal in same commit sequence | Seal presence check | Create retroactive seal |
| MR10 | Implementation starts before seal | HIGH | Medium | Gate flow: seal→unlock next phase | Gate CI | Freeze implementation |

## Severity Legend
CRITICAL: Permanent block | HIGH: Dual mitigation required | MEDIUM: Single mitigation | LOW: Documented

## Summary: 3 CRITICAL | 3 HIGH | 2 MEDIUM | 2 LOW

## Next: All risks reviewed → human merge decision

> Cap OS Wave0 | Controlled Exec Planning | Merge Risk Register | 10 items | Level 5 BLOCKED

## Risk Review Process
1. Human reviews all 10 merge risks
2. CRITICAL risks (MR1, MR2, MR8) require pre-merge verification
3. HIGH risks (MR3, MR4, MR9, MR10) require documented mitigation
4. MEDIUM risks (MR5, MR6) monitored during merge
5. LOW risk (MR7) accepted as-is

## Pre-Merge Verification
- MR1: git branch --show-current = postmerge/skillos-v0-baseline-freeze
- MR2: git push without --force flag
- MR3: git diff --stat shows only allowed files
- MR8: grep "authorized" returns 0 hits in all 26 docs

## Evidence
- Dependency: WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4)
- 374 test baseline verified
- All 26 docs verified: FUTURE_PLAN_ONLY, Level 5 BLOCKED

## Boundary
No code merge. No test merge. No enablement. No execution. Level 5 BLOCKED.

## Next
All risks reviewed → human merge decision → docs-only merge → post-merge seal