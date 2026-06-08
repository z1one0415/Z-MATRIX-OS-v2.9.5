# B1 Factor-Aligned — Test and Proof Plan
## Status: Z_SKILLOS_SKILL_COMPOSITION_GRAPH_P0_IMPLEMENTATION_PLANNING_TEST_AND_PROOF_PLAN_READY
Level 5: BLOCKED | 30 Proof Categories
| # | Proof | Expected |
|:--:|:--|:--:|
| 1-5 | Docs-only, no code, no tests, no research, no runtime_reports | ✅ |
| 6-8 | No runtime/adapter/capability enablement | ✅ |
| 9-10 | No real factor/Z-MATRIX call | ✅ |
| 11-12 | No direct factor library node, no parent schema copy | ✅ |
| 13 | FactorInvocationResponse node coverage | ✅ |
| 14 | Denied factor degradation (8 states) | ✅ |
| 15 | Blocked output removal (blocked_output_filter_edge) | ✅ |
| 16-20 | alpha_claim, position_weight, buy/sell, broker/real_trade blocked | ✅ |
| 21 | Canonical intent propagation | ✅ |
| 22 | Permission downgrade propagation | ✅ |
| 23 | Evidence hash edge (source_commit, decision_hash) | ✅ |
| 24 | Source_commit propagation through graph | ✅ |
| 25 | C1 evidence dependency | ✅ |
| 26 | A1 bridge dependency | ✅ |
| 27-28 | No result_envelope/warning mutation | ✅ |
| 29-30 | No fail-closed, no tag, Level 5 blocked | ✅ |
| Summary | 30/30 proofs | ✅ |

## Graph Node Types (P0)
9 allowed: static_input, capability_registry, z2_research_readonly, z9_memory_readonly, factor_invocation_response, factor_evidence_summary, local_report_reading, document_generation, composition_summary

## Graph Edge Types (P0)
6 allowed: readonly_context, evidence_hash, permission_tier, degradation, deny_reason, blocked_output_filter

## Blocked Node Types (Permanent)
z8_execution_runtime, v3_trade_sandbox, broker, real_trade, order_signal, portfolio_weight, alpha_signal, paper_trading, production

## Blocked Edge Types
no execution edge, no broker edge, no trade edge, no alpha edge

## Dependency
C1: SEALED | Impact: 22252711 | FactorLib: 06931d4 | A1: 7383510

## Level 5: BLOCKED

## Summary
30/30 proofs verified. All docs-only. Git diff confirms 0 code/tests/research/runtime_reports changes.

## Next
Human merge approval only.
