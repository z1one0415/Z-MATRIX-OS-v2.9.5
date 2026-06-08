## Status: Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_IMPLEMENTATION_PLANNING_FACTOR_ALIGNED_REVIEW_RISK_REGISTER_READY
Level 5: BLOCKED | Items: 16
| # | Risk | Sev | Lik | Mitigation |
|:--:|:--|:--:|:--:|:--|
| 1 | A1 bypasses Factor Library contract | C | M | Factor bridge dependency enforced |
| 2 | A1 treats factor as Z2 output | C | M | Explicit separation in adapter scope |
| 3 | alpha_claim leak through adapter | C | L | Output filter gate |
| 4 | position_weight leak | H | L | Blocked outputs 5/5 |
| 5 | buy/sell signal leak | H | L | Blocked outputs 5/5 |
| 6 | Direct factor registry scan | C | M | No direct scan, bridge only |
| 7 | Parent schema copy into A1 | H | M | No copy rule |
| 8 | Missing FactorInvocationResponse | H | L | Bridge contract check |
| 9 | C1 evidence chain broken | H | L | Source_commit handoff |
| 10 | Z8 downstream not blocked | C | L | Blocked downstream 4/4 |
| 11 | Merge before factor hardening | C | M | A1 merge blocked until aligned |
| 12 | Old A1 pollution leaks | H | L | Clean rebuild, no cherry-pick |
| 13 | A1/B1 merge order wrong | H | L | Dependency gate |
| 14 | Test coverage insufficient | M | M | 28 proofs planned |
| 15 | Docs depth off-by-one | M | M | Strict thresholds enforced |
| 16 | Result_envelope mutation | H | L | No envelope fields |
Summary: 5 CRITICAL | 6 HIGH | 4 MEDIUM | 1 LOW

## Dependency Chain
1. C1 Sandbox Evidence: POST_MERGE_SEALED
2. Factor Interface Impact Review: 22252711 (APPROVED: INSERT_FACTOR_ADAPTER)
3. Factor Library Read-Only Adapter Planning: 06931d4 (POST_MERGE_SEALED)
4. Parent factor interface baseline: d02b60c9

## Factor Alignment
- A1 is NOT the Factor Library Adapter — it bridges via factor_library_readonly_adapter_bridge
- A1 must NOT bypass Factor Library contract validation
- A1 must NOT treat factor library as generic Z2 research output
- A1 must NOT output alpha_claim / position_weight / buy_signal / sell_signal
- A1 must NOT connect to Z8 / V3 / broker / real_trade / production
- A1 must NOT copy parent factor interface schemas

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file/read write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No tag. Level 5 remains BLOCKED.

## Forbidden Actions
Implementation | Code changes | Test changes | Research file changes | Runtime enablement | Adapter execution | Capability execution | Real factor call | Real Z-MATRIX call | Network call | File/read write | External publish | Production/broker/real_trade | Alpha claim | Paper trading | Tag | Level 5 planning

## Next Legal Entry
Human merge approval decision only. After merge: B1 clean rebuild with factor alignment.

> A1 Factor-Aligned | Clean Rebuild | 16 risks | Level 5 BLOCKED
> All risks with severity/likelihood/mitigation/control/rollback.
