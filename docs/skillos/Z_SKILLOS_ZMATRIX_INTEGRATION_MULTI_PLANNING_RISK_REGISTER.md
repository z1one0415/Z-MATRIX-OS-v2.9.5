# Z-MATRIX Integration Multi-Planning Risk Register
## Status: Z_SKILLOS_ZMATRIX_INTEGRATION_MULTI_PLANNING_RISK_REGISTER_READY
Base: postmerge @ 67cd642 | Level 5: BLOCKED | Items: 12
| # | Risk | Sev | Lik | Mitigation |
|:--|:--|:--:|:--:|:--|
| R1 | Planning→Z-MATRIX call implication | C | L | Every doc: FUTURE_PLAN_ONLY, no call |
| R2 | 3 parallel branches diverge | H | M | Same decision base commit |
| R3 | Lane A implies module import | C | L | Explicit: no import |
| R4 | Lane B implies composition execution | H | L | DAG plan-only, no execution |
| R5 | Lane C implies file write | H | L | In-memory only, hash-only |
| R6 | Scope creep across lanes | M | M | Prefix-boundary enforced |
| R7 | Docs quality inconsistent | M | M | Unified depth standards |
| R8 | Wave0 sample line not referenced | M | L | Dependency listed everywhere |
| R9 | Review decision incomplete | H | L | 10 PENDING template |
| R10 | Merge order wrong after planning | M | L | Sequenced in closeout |
| R11 | Stale "2.py" from prior branch | C | L | grep check before commit |
| R12 | No regression run | L | L | Run once before summary |
