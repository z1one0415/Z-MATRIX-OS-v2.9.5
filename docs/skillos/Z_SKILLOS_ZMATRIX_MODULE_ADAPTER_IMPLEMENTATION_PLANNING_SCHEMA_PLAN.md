# A1 Factor-Aligned — SCHEMA
## Status: Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_IMPLEMENTATION_PLANNING_SCHEMA_PLAN_READY
Base: 06931d4 | Level 5: BLOCKED | FUTURE_PLAN_ONLY | Factor: d02b60c9 | Impact: 22252711 | FactorLib: 06931d4 | C1: MERGED | FUTURE_PLAN_ONLY
## Scope: SCHEMA for Z-MATRIX module adapter. Factor-aligned. Dependency: FactorLib bridge.
## Boundary: No implementation. No code. No research. No direct factor access. No alpha_claim/output/execution. Level 5 BLOCKED.
## Next: Next planning doc.

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

## Evidence
- Clean rebuild from postmerge 06931d4. Old polluted A1 at 294872a not reused.
- Factor Library Read-Only Adapter: 06931d4 (POST_MERGE_SEALED)
- C1 Sandbox Evidence: MERGED_AND_SEALED
- Factor Interface Impact Review: 22252711
- Parent factor interface: d02b60c9

## Proof / Requirements
28 proof categories. All verified by 26 docs and git diff.

## Adapter Priority
Wave A1-P0: capability_registry_readonly | z9_memory_review_readonly | z2_research_output_readonly | local_report_reading | document_generation_in_memory | factor_library_readonly_adapter_bridge
Wave A1-P1 (deferred): z2_industry_chain_research_readonly | z2_scoring_context_dry_plan | factor_candidate_monitor_bridge | composition_graph_dry_plan_bridge
Blocked permanently: z8_execution_runtime | v3_trade_sandbox | broker | real_trade | production | portfolio_execution | order_signal | alpha_signal | paper_trading

## Status
Not authorized: merge A1, merge B1, implementation, runtime enablement, adapter execution enablement, capability execution, real factor call, real Z-MATRIX call, production/broker/real_trade, alpha claim, paper trading.
