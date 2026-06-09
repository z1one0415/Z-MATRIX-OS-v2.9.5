# Z-SkillOS B1 Composition Graph Factor Bridge Implementation Branch Approval Risk Register

## Status: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY
## Date: 2026-06-09
## Base HEAD: 06f4015f36191a0cd58a60b1e57e5d417843ab38

## Risk Register

### Risk 1: B1 graph bypasses A1 bridge and reads Factor Library directly
- **Severity**: CRITICAL | **Likelihood**: LOW
- **Mitigation**: Graph only imports A1FactorBridgeResponse. No factor_library imports allowed.
- **Control**: AST import scan; merge-blocking CI check.
- **Rollback Trigger**: Any import from skillos.capability_invocation_os.adapters.factor_library in composition_graph/.

### Risk 2: B1 graph consumes FactorInvocationResponse instead of A1FactorBridgeResponse
- **Severity**: CRITICAL | **Likelihood**: LOW
- **Mitigation**: Type annotations enforce A1FactorBridgeResponse. No FactorInvocationResponse in graph code.
- **Control**: Import scan for FactorInvocationResponse in composition_graph/.
- **Rollback Trigger**: FactorInvocationResponse imported or used in composition_graph/.

### Risk 3: B1 graph invokes real Z-MATRIX module
- **Severity**: CRITICAL | **Likelihood**: VERY_LOW
- **Mitigation**: No Z-MATRIX runtime imports. Only frozen dataclass consumption.
- **Control**: Import blocklist scan for Z2/Z8/Z9/V3/gate_data modules.
- **Rollback Trigger**: Any Z-MATRIX runtime import found in composition_graph/.

### Risk 4: Denied bridge context converted to valid graph node
- **Severity**: CRITICAL | **Likelihood**: MEDIUM
- **Mitigation**: node_builder enforces: DENY decision → a1_factor_bridge_denied_context_node ONLY. Contract test required.
- **Control**: Parametrized test across all DENY scenarios. Denied context cannot become valid node.
- **Rollback Trigger**: Any DENY A1BridgeResponse producing non-denied graph node.

### Risk 5: Graph edge becomes execution edge
- **Severity**: CRITICAL | **Likelihood**: LOW
- **Mitigation**: Edge types restricted to 8 allowed types. Execution edges in blocked set.
- **Control**: Edge type validation in dag_validator. Test for blocked edge rejection.
- **Rollback Trigger**: Any execution_edge/trade_edge/broker_edge found in graph.

### Risk 6: forbidden_outputs_removed not propagated through graph
- **Severity**: HIGH | **Likelihood**: MEDIUM
- **Mitigation**: Graph node inherits forbidden_outputs_removed from A1BridgeResponse. Evidence tracks hash.
- **Control**: Test assertion on every graph node output.
- **Rollback Trigger**: Any graph node missing forbidden_outputs_removed propagation.

### Risk 7: no_real_source_flag lost in graph transformation
- **Severity**: HIGH | **Likelihood**: MEDIUM
- **Mitigation**: Graph evidence preserves no_real_source_flag from bridge response.
- **Control**: Explicit test on every graph evidence entry.
- **Rollback Trigger**: Any graph evidence without no_real_source_flag when source had it.

### Risk 8: source_class lost in graph
- **Severity**: HIGH | **Likelihood**: LOW
- **Mitigation**: Graph evidence preserves source_class=factor_library_fixture.
- **Control**: Test assertion on graph evidence source_class.
- **Rollback Trigger**: source_class missing or wrong in graph evidence.

### Risk 9: P1_FIXTURE_ONLY lost in graph
- **Severity**: HIGH | **Likelihood**: LOW
- **Mitigation**: Graph evidence preserves fixture_source_commit.
- **Control**: Test assertion on graph evidence fixture_source_commit.
- **Rollback Trigger**: fixture_source_commit missing in graph evidence.

### Risk 10: factor_decision_hash / bridge_decision_hash lost
- **Severity**: MEDIUM | **Likelihood**: LOW
- **Mitigation**: Graph evidence inherits both hashes from A1 bridge evidence.
- **Control**: Test assertion verifying non-empty hashes in graph output.
- **Rollback Trigger**: Empty factor_decision_hash or bridge_decision_hash in graph output.

### Risk 11: graph_node_hash / graph_edge_hash non-deterministic
- **Severity**: MEDIUM | **Likelihood**: LOW
- **Mitigation**: Hash from sorted JSON of node/edge content. Deterministic by construction.
- **Control**: Repeat-call test verifying same input → same hash.
- **Rollback Trigger**: Same input producing different graph_node_hash on repeated calls.

### Risk 12: alpha_claim / position_weight / buy_signal leakage
- **Severity**: CRITICAL | **Likelihood**: VERY_LOW
- **Mitigation**: Output boundary filter removes all BLOCKED_OUTPUTS. No trading fields on graph models.
- **Control**: Grep scan; parametrized test on all graph outputs.
- **Rollback Trigger**: Any forbidden output field with non-null value in graph output.

### Risk 13: Runtime enablement prematurely activated
- **Severity**: CRITICAL | **Likelihood**: LOW
- **Mitigation**: All config functions return False. Kill switch active. enabled()→False.
- **Control**: Kill switch test suite. Merge-blocking.
- **Rollback Trigger**: Any enabled() returning True in graph code.

### Risk 14: Adapter execution enablement prematurely activated
- **Severity**: CRITICAL | **Likelihood**: LOW
- **Mitigation**: No execute/run/call/invoke method names. Only build_*/get_*/validate_* allowed.
- **Control**: AST scan for forbidden method names.
- **Rollback Trigger**: Any forbidden method name in composition_graph/.

### Risk 15: result_envelope mutation
- **Severity**: HIGH | **Likelihood**: LOW
- **Mitigation**: Graph operates on frozen dataclasses. No in-place mutation.
- **Control**: Immutability test. Source response unchanged after graph processing.
- **Rollback Trigger**: Any mutation of input A1FactorBridgeResponse detected.

### Risk 16: Tests only cover happy path
- **Severity**: MEDIUM | **Likelihood**: MEDIUM
- **Mitigation**: Test matrix must include all 6 fixture scenarios through graph.
- **Control**: Minimum test categories in merge checklist.
- **Rollback Trigger**: Fewer than 5 deny-path tests found at merge review.

### Risk 17: Level 5 boundary drift
- **Severity**: CRITICAL | **Likelihood**: VERY_LOW
- **Mitigation**: No Level 5 language in code or docs. Explicit BLOCKED markers.
- **Control**: Grep scan at merge time.
- **Rollback Trigger**: Any Level 5 enablement language found.

## Summary: CRITICAL 9, HIGH 5, MEDIUM 3 = 17 risks. All mitigated.
