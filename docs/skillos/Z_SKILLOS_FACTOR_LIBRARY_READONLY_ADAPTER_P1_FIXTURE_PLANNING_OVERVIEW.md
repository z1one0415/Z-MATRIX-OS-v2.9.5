# FactorLib P1 Fixture — OVERVIEW
## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_P1_FIXTURE_PLANNING_OVERVIEW_READY
Base: 680f9f9 | P0: 680f9f9 | Level 5: BLOCKED | P0: 680f9f9 | Fixture planning | No real source | Level 5 BLOCKED
## Scope: OVERVIEW for P1 readonly fixture. Static/in-memory fixtures only.
## Fixture Scenarios (6): SAFE_VALIDATED, DENIED_PIT_FAILED, DENIED_COVERAGE_FAILED, DENIED_GUARDRAIL_FAILED, DENIED_PROMOTION, DENIED_EXECUTION_FORBIDDEN
## Response Decisions (16): DISABLED_DEFAULT_NOOP, ALLOW_REGISTRY_ONLY, ALLOW_EVIDENCE_ONLY, ALLOW_VALIDATION_SUMMARY, ALLOW_GUARDRAIL_SUMMARY, ALLOW_CANDIDATE_MONITOR, ALLOW_READONLY_CONTEXT, ALLOW_COMPOSITION_GRAPH_DRY_PLAN, DENY_FACTOR_NOT_FOUND, DENY_FACTOR_NOT_VALIDATED, DENY_PIT_FAILED, DENY_COVERAGE_FAILED, DENY_FAMILY_OVERLAP, DENY_GUARDRAIL_FAILED, DENY_PROMOTION_NOT_ALLOWED, DENY_EXECUTION_FORBIDDEN
## Blocked Outputs (9): alpha_claim, expected_return_claim, position_weight, buy_signal, sell_signal, order_signal, broker_runtime, real_trade, production
## Evidence Fields (13): source_commit=P1_FIXTURE_ONLY, request_hash, response_hash_placeholder, decision_hash, factor_manifest_hash, validation_snapshot_hash, guardrail_profile_hash, application_contract_hash, permission_tier, source_class=factor_library_fixture, rollback_marker, privacy_marker, no_real_source_flag
## Boundary: No implementation. No code/tests/research. No runtime/adapter/capability enablement. No real factor call. No research/factor_library read. Level 5 BLOCKED.
## Forbidden: Implementation | Code/tests/research changes | Runtime enablement | Adapter execution | Capability execution | Real factor call | Research read | Network | File write | Production/broker/real_trade | Alpha/paper signals | result_envelope mutation | Tag | Level 5 planning
## Next: Human review only.
