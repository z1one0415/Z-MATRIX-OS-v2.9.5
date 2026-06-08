# Skill Composition Graph P0 Implementation Planning — Overview (Factor-Aligned Clean)

## Status: Z_SKILLOS_SKILL_COMPOSITION_GRAPH_P0_IMPLEMENTATION_PLANNING_FACTOR_ALIGNED_OVERVIEW_READY
Branch: plan/...composition-graph-factor-aligned-clean | Base: postmerge @ 7383510 | Level 5: BLOCKED

## Purpose
FUTURE_PLAN_ONLY. Docs-only. Plan the Skill Composition Graph P0 Implementation with factor-interface alignment. This plans the graph layer that composes Z-MATRIX capabilities and factor invocations into read-only composition plans. B1 consumes A1's FactorInvocationResponse and Factor Library's evidence envelope — it does NOT directly read factor library data or Z-MATRIX modules.

## Dependencies
- C1 Sandbox Evidence: POST_MERGE_SEALED
- Factor Interface Impact Review: 22252711
- Factor Library Read-Only Adapter Planning: 06931d4
- A1 Factor-Aligned Z-MATRIX Module Adapter: 7383510
- Parent factor interface baseline: d02b60c9

## Key Alignment Requirements
- B1 is NOT a runtime graph — only dry-plan/readonly composition
- B1 must consume A1's FactorInvocationResponse, NOT directly read factor library
- B1 must NOT bypass A1 / Factor Library Adapter
- B1 must NOT treat denied factor as valid node
- B1 must NOT output alpha_claim / position_weight / buy_signal / sell_signal
- B1 must NOT connect to Z8 / V3 / broker / real_trade
- B1 must NOT modify result_envelope
- B1 must NOT produce caller-visible warnings

## Allowed P0 Node Types
static_input_node | capability_registry_node | z2_research_output_readonly_node | z9_memory_review_readonly_node | factor_invocation_response_node | factor_evidence_summary_node | local_report_reading_node | document_generation_in_memory_node | composition_summary_node

## Allowed P0 Edge Types
readonly_context_edge | evidence_hash_edge | permission_tier_edge | degradation_edge | deny_reason_edge | blocked_output_filter_edge

## Blocked Permanently
z8_execution_runtime_node | v3_trade_sandbox_node | broker_node | real_trade_node | order_signal_node | portfolio_weight_node | alpha_signal_node | paper_trading_node | production_node

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file read/write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No warning enablement. No blocking/fail-closed. Level 5 BLOCKED.

## Forbidden Actions
Implementation | Code/test/research changes | Runtime enablement | Adapter execution | Capability execution | Real factor/Z-MATRIX call | Network | File write | Production/broker/real_trade | Alpha/paper/trade signals | Tag | Level 5 planning

## Proof Requirements
30 proofs in TEST_AND_PROOF_PLAN. FactorInvocationResponse coverage, blocked output filtering, denied factor degradation, C1/A1/FactorLib dependencies.

## Next
Scope → File-Level → Node Model → Edge Model → DAG Validator → Permission Propagation → Evidence Propagation → Degradation → Loop Prevention → Output Boundary → Test/Proof → Closeout → Seal

> B1 Factor-Aligned | Planning | Overview | FUTURE_PLAN_ONLY | Level 5 BLOCKED