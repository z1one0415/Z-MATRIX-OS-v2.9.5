# Z9 Review Node Implementation Planning — Review Risk Register
## Status: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED

## 1. Status
Document type: Review risk register. Part of Z9 Review Node Implementation Planning package.
Base commit: 1d61244. Planning branch locked at fdae771.
Requires human merge approval before Z9 Review Node implementation.
All 26 planning documents must pass depth verification before merge.

## 2. Scope
Docs-only Z9 Review Node disabled-default P0 implementation planning.
Defines future review risk register for Z9 Review Node disabled-default P0.
No implementation. No code. No tests. No research files. No zmatrix changes.
No runtime enablement. No adapter execution enablement. No capability execution.
Z9 Review Node reviews explanation quality and evidence completeness ONLY.
Z9 Review Node does NOT evaluate trading profit, PnL, or broker actions.
Z9 Review Node does NOT issue trade instructions or memory mutations.

## 3. Dependency / Evidence
* Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
* Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED
* Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED
* Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_MERGED_AND_SEALED
* B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
* A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
* FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
* postmerge HEAD: 1d61244
Primary input: Z2 z9_review_snapshot_candidate only.
No direct B1 CompositionGraphResponse consumption.
No direct research/factor_library access.
Evidence inherits 19 fields from Z2 snapshot exclusively.

## 4. Boundary
* Review-only. Explanation quality only.
* Z2 z9_review_snapshot_candidate only.
* 6 review labels: EXPLANATION_ACCEPTED_STRUCTURE_ONLY through EXPLANATION_REJECTED_UNSAFE_SOURCE.
* 10 degradation decisions from ALLOW_Z9_READONLY_REVIEW to DISABLED_DEFAULT_NOOP.
* 9 explanation-only attribution types. NO profit attribution.
* Z2 feedback: advisory/readonly only. Requires human review.
* No runtime enablement. No adapter execution. No capability execution.
* No paper trading. No trade_result. No real_pnl. No broker_action.
* No memory mutation. No persistent memory write.
* Level 5 remains BLOCKED.

## 5. Forbidden Actions
* No trade_instruction, buy_signal, sell_signal, position_weight, order_signal
* No automatic_rebalance, broker_action, paper_trade_order, real_trade_order
* No real_pnl, performance_claim, alpha_claim, expected_return_claim
* No production_decision, memory_mutation_result, persistent_memory_write
* No auto_patch_z2_report, auto_update_factor_score, auto_update_memory
* No auto_trade_adjustment, position_adjustment, rebalance_instruction
* No execution_edge, trade_edge, broker_edge, autonomous_retry_edge, mutation_edge
* No production_edge, alpha_signal_edge, real_time_feedback_edge
* No runtime enablement, adapter execution enablement, capability execution

## 6. Proof / Review Requirements
* 48 proof categories defined in Test and Proof Plan
* 38+ review checklist checks
* 32+ merge checklist checks
* 24+ review risk register entries
* 20+ merge risk register entries
* 18+ pending fields in review decision record
* All docs have 7-section structure
* Key content: z9_review_snapshot_candidate, 1d61244, DENY_Z9_*, Z2 dependency

## 7. Next Legal Entry
Human Z9 Review Node Implementation Planning merge approval decision only.
No implementation without separate approval.
No runtime enablement. No adapter execution enablement. No capability execution.
No paper trading. No trade_result. No real_pnl. No memory mutation.
Level 5 remains BLOCKED.

### Risk Register (24+ risks)
| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback |
|:--:|:--|:--:|:--:|:--|:--|:--|
| 1 | Z9 bypasses Z2, reads B1 directly | CRITICAL | LOW | Type validation | Import scan | Instance check |
| 2 | Z9 consumes FactorInvocationResponse | CRITICAL | LOW | Input contract | isinstance check | Direct input |
| 3 | Z9 calls real Z runtime | CRITICAL | VERY LOW | Import blocklist | AST scan | Runtime import |
| 4 | Trade/PNL data in Z2 snapshot | CRITICAL | LOW | Output filter blocks all | Snapshot validation | Trade field found |
| 5 | Memory mutation attempted | CRITICAL | VERY LOW | kill_switch blocks | Config check | Mutation detected |
| 6 | Degraded review accepted as valid | HIGH | MEDIUM | Degradation enforced | Contract test | Valid conclusion from degraded |
| 7 | Missing evidence treated as valid | HIGH | MEDIUM | Evidence completeness check | Contract test | Missing → valid |
| 8 | Evidence chain broken (no hash) | HIGH | LOW | Inheritance from Z2 | Hash validation | Empty hash |
| 9 | Z9 feedback mutates Z2 | HIGH | LOW | Feedback is readonly | Human review gate | Auto-patch |
| 10 | Confidence mismatch undetected | MEDIUM | MEDIUM | Alignment review | Test matrix | Misaligned passed |
| 11 | Attribution includes profit | CRITICAL | LOW | Attribution type filter | Check test | Profit attribution |
| 12 | Blocked output leakage | CRITICAL | LOW | Output filter | Grep scan | Forbidden field |
| 13 | z9_review_node_hash non-deterministic | MEDIUM | LOW | Deterministic hash | Repeat test | Non-matching |
| 14 | z9_review_section_hash non-deterministic | MEDIUM | LOW | Deterministic hash | Repeat test | Non-matching |
| 15 | z9_feedback_candidate_hash unstable | MEDIUM | LOW | Deterministic hash | Repeat test | Non-matching |
| 16 | Runtime enablement premature | CRITICAL | LOW | enabled()→False | Kill switch test | enabled→True |
| 17 | Tests only happy path | MEDIUM | MEDIUM | Full deny matrix | Merge check | Incomplete coverage |
| 18 | Fail-closed instead of degraded | HIGH | LOW | Degradation pattern | Contract test | raise/block |
| 19 | Review sections incomplete | MEDIUM | LOW | Schema validation | Section count | Missing sections |
| 20 | Persistent memory write | CRITICAL | VERY LOW | deny_memory_mutation | Check test | Write detected |
| 21 | Z2 feedback bypasses human | HIGH | LOW | Feedback advisory only | Human review flag | Auto action |
| 22 | Level 5 boundary drift | CRITICAL | VERY LOW | BLOCKED markers | Doc audit | Level 5 language |
| 23 | Production/broker linkage | CRITICAL | VERY LOW | Blocked outputs | Grep scan | Production found |
| 24 | Paper trading fields leak | HIGH | LOW | Output filter | Parametrized test | Paper trading field |