# Wave0 Controlled Read-Only Execution P0 Merge Checklist

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P0_MERGE_CHECKLIST_READY
Branch: impl/...p0-clean @ 37d7d3d | Level 5: BLOCKED | Items: 15

| # | Check | Status |
|:--|:--|:--:|
| M1 | 39 whitelisted files only | ✅ |
| M2 | 0 code changes outside wave0/ | ✅ |
| M3 | 0 test changes outside wave0/ | ✅ |
| M4 | 0 stale " 2.*" files | ✅ |
| M5 | 0 v4.0 artifacts | ✅ |
| M6 | 0 old Wave0 unrelated docs | ✅ |
| M7 | 0 forbidden imports | ✅ |
| M8 | 0 execute/run/call/invoke methods | ✅ |
| M9 | All is_*_enabled()→False | ✅ |
| M10 | Review gate passed | ⬜ |
| M11 | REVIEW_DECISION approved | ⬜ |
| M12 | Target HEAD = 294872a | ⬜ |
| M13 | Post-merge seal planned | ⬜ |
| M14 | Level 5 BLOCKED verified | ✅ |
| M15 | 415 tests pass baseline | ✅ |

## Summary: 15 items | All must pass for merge

## Next
All pass → human MERGE_DECISION → merge to postmerge

> Cap OS Wave0 | Controlled Exec P0 | Merge Checklist | 15 items | Level 5 BLOCKED

## Pre-Merge Verification Steps
1. `git branch --show-current` = postmerge/skillos-v0-baseline-freeze
2. `git rev-parse HEAD` = 294872a
3. `git diff --stat` shows only whitelisted P0 files
4. `git diff --name-only` = 0 .py outside wave0/
5. `grep` stale/contaminated: 0 hits
6. Verify REVIEW_DECISION approved (10 PENDING→10 DECIDED)
7. Verify all tests pass (415 baseline)
8. Execute merge with --no-ff
9. Create post-merge seal immediately
10. Record merge commit SHA in seal

## Boundary
No code outside wave0/. No stale files. No v4.0 artifacts. Level 5 BLOCKED.