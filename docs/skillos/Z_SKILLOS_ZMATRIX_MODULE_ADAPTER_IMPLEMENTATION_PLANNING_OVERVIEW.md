# Z-MATRIX Module Adapter Implementation Planning — Overview (Factor-Aligned Clean)

## Status: Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_IMPLEMENTATION_PLANNING_FACTOR_ALIGNED_OVERVIEW_READY
Branch: plan/...zmatrix-adapter-factor-aligned-clean | Base: postmerge @ 06931d4 | Level 5: BLOCKED

## Purpose
FUTURE_PLAN_ONLY. Docs-only. Plan the Z-MATRIX Module Adapter Implementation with explicit factor-interface alignment. This is the upper-layer adapter planning that orchestrates Z-MATRIX module access through the WAVE0 controlled read-only execution framework, with factor library dependency bridged through the Factor Library Read-Only Adapter (06931d4).

## Dependencies
- C1 Sandbox Evidence: Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_IMPLEMENTATION_PLANNING_POST_MERGE_SEALED
- Factor Interface Impact Review: 22252711
- Factor Library Read-Only Adapter Planning: 06931d4
- Parent factor interface baseline: d02b60c9

## Adapter Priority
### Wave A1-P0 (immediate scope, factor-aligned)
1. capability_registry_readonly — registry discovery
2. z9_memory_review_readonly — memory/evidence review
3. z2_research_output_readonly — research output reading
4. local_report_reading — local report access
5. document_generation_in_memory — in-memory document generation
6. factor_library_readonly_adapter_bridge — bridge to Factor Library adapter

### Wave A1-P1 (deferred)
1. z2_industry_chain_research_readonly
2. z2_scoring_context_dry_plan
3. factor_candidate_monitor_bridge
4. composition_graph_dry_plan_bridge

### Blocked Permanently (Level 5)
z8_execution_runtime | v3_trade_sandbox | broker | real_trade | production | portfolio execution | order signal | alpha signal | paper trading

## Key Alignment Requirements
- A1 is NOT the Factor Library Adapter — it bridges through the planned Factor Library Read-Only Adapter
- A1 must NOT bypass Factor Library contract validation
- A1 must NOT treat factor library as generic Z2 research output
- A1 must NOT output alpha_claim / position_weight / buy_signal / sell_signal
- A1 must NOT connect to Z8 / V3 / broker / real_trade / production
- A1 must NOT copy parent factor interface schemas

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file read/write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. Level 5 BLOCKED.

## Forbidden Actions
Implementation code | Code/test changes | Research file changes | Runtime enablement | Adapter execution | Capability execution | Real factor call | Real Z-MATRIX call | Network call | File write | External publish | Production/broker/real_trade | Alpha claim | Paper trading | Tag | Level 5 planning

## Proof Requirements
28 proofs defined in TEST_AND_PROOF_PLAN. All verified by 26 docs and git diff.

## Next
Scope → File-Level → Contract → Registry → Permission → Readonly Policy → Schema → Evidence → Priority Wave → Rollback → Test/Proof → Closeout → Seal

> A1 Factor-Aligned | Planning | Overview | FUTURE_PLAN_ONLY | Level 5 BLOCKED