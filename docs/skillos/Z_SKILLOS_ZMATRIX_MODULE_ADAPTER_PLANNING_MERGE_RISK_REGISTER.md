# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — MERGE RISK REGISTER
> Status: _MERGE_RISK_REGISTER_READY | Level 5 BLOCKED | Items: 10
| # | Risk | Sev | Lik | Mitigation |
|:--|:--|:--:|:--:|:--|
| MR1 | Wrong branch | C | L | Pre-merge verify |
| MR2 | Force-push | C | L | No --force |
| MR3 | Non-doc creep | H | L | git diff verify |
| MR4 | Regression | H | L | 218 baseline |
| MR5 | Concurrent merge | M | L | Sequential |
| MR6 | Docs stale | M | M | SHA in seal |
| MR7 | Message unclear | L | L | Template |
| MR8 | Impl creep | C | L | FUTURE_PLAN_ONLY grep |
| MR9 | Seal missing | H | L | Same sequence |
| MR10 | Pre-seal impl | H | M | Gate flow |
