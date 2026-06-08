# FactorLib Impl P0 — ROLLBACK
## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_IMPLEMENTATION_PLANNING_ROLLBACK_PLAN_READY
Base: 7e0a6c9 | Level 5: BLOCKED | FUTURE_PLAN_ONLY | ALL_5_MERGED | ALL_5_MERGED | Blueprint for adapter code
## Scope: ROLLBACK for Factor Library adapter. Implementation blueprint. No code. Future files defined.
## Boundary: No implementation. No runtime/adapter/capability enablement. No real calls. Level 5 BLOCKED.
## Next: Next planning doc.

## Implementation Blueprint Summary
- Future files: 10 adapter files (models, contracts, registry, permissions, output_filter, evidence, degradation, adapter, kill_switch) + 6 test files
- Allowed methods: list_factors, get_factor_profile, get_factor_evidence, monitor_candidates, build_research_context
- Forbidden methods: execute, run, call, invoke, trade, optimize, backtest_live, generate_alpha, generate_signal, build_portfolio, place_order
- FactorInvocationRequest: request_id, caller, intent, factor_selector, subject, horizon, permission_tier, output_mode, execution_requested=false
- FactorInvocationResponse: response_id, decision(15 enums), factor_manifest, factor_profile, evidence_envelope, validation_snapshot, guardrail_profile, forbidden_outputs_removed, degraded
- Output filter: removes alpha_claim, expected_return_claim, position_weight, buy_signal, sell_signal, order_signal, broker_runtime, real_trade, production
- Degradation: 8 DENY states with degrade-to-noop/plan-only; no blocking, no fail-closed, no exception escalation
- Evidence handoff: source_commit, request_hash, response_hash_placeholder, decision_hash, factor_manifest_hash, validation_snapshot_hash, guardrail_profile_hash, application_contract_hash, permission_tier, source_class, rollback_marker, privacy_marker

## Dependencies
C1: POST_MERGE_SEALED | FactorLib Planning: 06931d4 | A1: 7383510 | B1: 7e0a6c9 | Parent: d02b60c9

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file/read write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No warning enablement. No blocking/fail-closed. No tag. Level 5 remains BLOCKED.

## Forbidden Actions
Implementation | Code/test/research changes | Runtime enablement | Adapter execution | Capability execution | Real factor/Z-MATRIX call | Network | File write | Production/broker/real_trade | Alpha/paper/trade signals | result_envelope mutation | Warning | Blocking/fail-closed | Tag | Level 5 planning

## Next Legal Entry
Human merge approval only. After merge: Factor Library implementation branch (separate human approval required).

## Key Data Structures
- FactorManifestView: factor_id, factor_name, factor_family_id, factor_status, factor_type, formula_ref, source_data_refs, universe_policy, asof_policy, horizon_policy, lifecycle_locks, runtime_boundary_locks
- FactorFamilyProfileView: family_id, family_group, overlap_group, orthogonality_required, max_active_candidates, new_family_requires_review, rejected_factor_preservation, family_overlap_denial
- FactorValidationSnapshotView: coverage_passed, coverage_tier, pit_passed, single_factor_validation_executed, true_oos_validation_executed, ready_for_candidate_review, promotion_allowed=false, multi_factor_composite_built=false, weight_optimization_executed=false, alpha_claim_allowed=false
- FactorGuardrailProfileView: required_guardrails, risk_flags, guardrail_state, failure_mode, promotion_denial, crowding_gate, turnover_gate, cost_gate, pit_leakage_gate, disclosure_staleness_gate
- FactorApplicationContractView: allowed_application_modes(8), blocked_application_modes(7), blocked_outputs(5), blocked_downstream_consumers(4), execution_requested=false, promotion_allowed=false, alpha_claim_allowed=false, production/broker/real_trade=BLOCKED

## Evidence Handoff Fields
13 fields: source_commit, request_hash, response_hash_placeholder, decision_hash, factor_manifest_hash, validation_snapshot_hash, guardrail_profile_hash, application_contract_hash, permission_tier, source_class, rollback_marker, privacy_marker → C1 evidence chain

## Dependency Summary
Parent: d02b60c9 | C1: POST_MERGE_SEALED | FactorLib Planning: 06931d4 | A1: 7383510 | B1: 7e0a6c9

## Level 5: BLOCKED
> FactorLib Impl P0 | ROLLBACK | FUTURE_PLAN_ONLY | Implementation blueprint
- Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_IMPLEMENTATION_PLANNING_ROLLBACK_PLAN: target section 1 of 4
- Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_IMPLEMENTATION_PLANNING_ROLLBACK_PLAN: target section 2 of 4
- Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_IMPLEMENTATION_PLANNING_ROLLBACK_PLAN: target section 3 of 4
- Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_IMPLEMENTATION_PLANNING_ROLLBACK_PLAN: target section 4 of 4
