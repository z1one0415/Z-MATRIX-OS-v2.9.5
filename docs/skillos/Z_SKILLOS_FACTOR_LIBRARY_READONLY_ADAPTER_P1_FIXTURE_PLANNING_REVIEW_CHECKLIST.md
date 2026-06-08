# FactorLib P1 Fixture — REVIEW_CHECKLIST
## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_P1_FIXTURE_PLANNING_REVIEW_CHECKLIST_READY
Base: 680f9f9 | P0: 680f9f9 | Level 5: BLOCKED | P0: 680f9f9 | Fixture planning | No real source | Level 5 BLOCKED
## Scope: REVIEW_CHECKLIST for P1 readonly fixture. Static/in-memory fixtures only.
## Fixture Scenarios (6): SAFE_VALIDATED, DENIED_PIT_FAILED, DENIED_COVERAGE_FAILED, DENIED_GUARDRAIL_FAILED, DENIED_PROMOTION, DENIED_EXECUTION_FORBIDDEN
## Response Decisions (16): DISABLED_DEFAULT_NOOP, ALLOW_REGISTRY_ONLY, ALLOW_EVIDENCE_ONLY, ALLOW_VALIDATION_SUMMARY, ALLOW_GUARDRAIL_SUMMARY, ALLOW_CANDIDATE_MONITOR, ALLOW_READONLY_CONTEXT, ALLOW_COMPOSITION_GRAPH_DRY_PLAN, DENY_FACTOR_NOT_FOUND, DENY_FACTOR_NOT_VALIDATED, DENY_PIT_FAILED, DENY_COVERAGE_FAILED, DENY_FAMILY_OVERLAP, DENY_GUARDRAIL_FAILED, DENY_PROMOTION_NOT_ALLOWED, DENY_EXECUTION_FORBIDDEN
## Blocked Outputs (9): alpha_claim, expected_return_claim, position_weight, buy_signal, sell_signal, order_signal, broker_runtime, real_trade, production
## Evidence Fields (13): source_commit=P1_FIXTURE_ONLY, request_hash, response_hash_placeholder, decision_hash, factor_manifest_hash, validation_snapshot_hash, guardrail_profile_hash, application_contract_hash, permission_tier, source_class=factor_library_fixture, rollback_marker, privacy_marker, no_real_source_flag
## Boundary: No implementation. No code/tests/research. No runtime/adapter/capability enablement. No real factor call. No research/factor_library read. Level 5 BLOCKED.
## Forbidden: Implementation | Code/tests/research changes | Runtime enablement | Adapter execution | Capability execution | Real factor call | Research read | Network | File write | Production/broker/real_trade | Alpha/paper signals | result_envelope mutation | Tag | Level 5 planning
## Next: Human review only.

## Fixture Factor Scenarios (6)
### FIXTURE_FACTOR_SAFE_VALIDATED
All validation passed, guardrails passed, contract complete. Expected decision: DISABLED_DEFAULT_NOOP. No forbidden outputs. not degraded.

### FIXTURE_FACTOR_DENIED_PIT_FAILED
PIT leakage detected. Expected decision: DENY_PIT_FAILED. degraded=True. forbidden_outputs_removed present.

### FIXTURE_FACTOR_DENIED_COVERAGE_FAILED
Coverage insufficient. Expected decision: DENY_COVERAGE_FAILED. degraded=True.

### FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED
Guardrail triggered. Expected decision: DENY_GUARDRAIL_FAILED. degraded=True.

### FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED
Promotion blocked by contract. Expected decision: DENY_PROMOTION_NOT_ALLOWED. degraded=True.

### FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN
Execution intent or forbidden intent detected. Expected decision: DENY_EXECUTION_FORBIDDEN. degraded=True.

## Fixture Data Model (per scenario)
- fixture_id (UUID)
- factor_id (e.g., "F21_fixture_safe")
- factor_family_id (e.g., "FF01_fixture")
- manifest_view (FactorManifestView)
- validation_snapshot_view (FactorValidationSnapshotView — varies per scenario)
- guardrail_profile_view (FactorGuardrailProfileView — passed/failed per scenario)
- application_contract_view (FactorApplicationContractView — complete blocked lists)
- evidence_envelope_view (FactorEvidenceEnvelopeView — source_commit=P1_FIXTURE_ONLY)
- expected_decision (FactorAdapterDecision)
- expected_forbidden_outputs_removed (list of BLOCKED_OUTPUTS)
- expected_degraded_state (True for DENY scenarios)
- expected_evidence_hashes (dict with all 13 handoff fields)
- no_real_source_flag (True — no real factor data)

## 16 Response Decisions Covered by Fixtures
ALLOW: REGISTRY_ONLY | EVIDENCE_ONLY | VALIDATION_SUMMARY | GUARDRAIL_SUMMARY | CANDIDATE_MONITOR | READONLY_CONTEXT | COMPOSITION_GRAPH_DRY_PLAN
DENY: FACTOR_NOT_FOUND | FACTOR_NOT_VALIDATED | PIT_FAILED | COVERAGE_FAILED | FAMILY_OVERLAP | GUARDRAIL_FAILED | PROMOTION_NOT_ALLOWED | EXECUTION_FORBIDDEN
BASE: DISABLED_DEFAULT_NOOP

## 9 Blocked Outputs (must be removed by fixture-aware output filter)
alpha_claim | expected_return_claim | position_weight | buy_signal | sell_signal | order_signal | broker_runtime | real_trade | production

## 13 Evidence Handoff Fields
source_commit=P1_FIXTURE_ONLY | request_hash | response_hash_placeholder | decision_hash | factor_manifest_hash | validation_snapshot_hash | guardrail_profile_hash | application_contract_hash | permission_tier | source_class=factor_library_fixture | rollback_marker | privacy_marker | no_real_source_flag

## Key Boundary Rules
- P1 fixture is not real factor read: all fixtures are synthetic, constructed in-memory
- P1 fixture must not read research/factor_library: fixture provider blocks research imports
- P1 fixture must not copy parent factor artifacts: no file copy from research/factor_library
- P1 fixture uses fake static or in-memory fixtures only: no real factor data
- P1 fixture must not enable runtime/adapter/capability execution: Level 5 BLOCKED
- P1 fixture must not produce alpha claim, position_weight, buy/sell signals: removed by output filter

## Dependency Chain
P0: 680f9f9 | C1: POST_MERGE_SEALED | A1: 7383510 | B1: 7e0a6c9 | Parent: d02b60c9 | Impact: 22252711

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No research/factor_library read. No network call. No file/read write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. Level 5 remains BLOCKED.

## Forbidden Actions
Implementation | Code/test/research changes | Runtime enablement | Adapter execution | Capability execution | Real factor call | Research/factor_library read | Network | File write | Production/broker/real_trade | Alpha/paper/trade signals | result_envelope mutation | Warning enablement | Blocking/fail-closed | Tag | Level 5 planning

## Next Legal Entry
Human merge approval only.
