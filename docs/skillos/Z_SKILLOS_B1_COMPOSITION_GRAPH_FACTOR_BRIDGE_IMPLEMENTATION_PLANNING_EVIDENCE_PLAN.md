# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — EVIDENCE PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Evidence hash chain specification for B1 composition graph

## 2. Scope

This document defines how evidence hashes propagate through the B1 composition graph.
B1 consumes A1FactorBridgeResponse ONLY. All evidence fields must be preserved or
computed at each node transition. Denied context cannot become valid node.

### 2.1 Evidence Fields

| Field | Origin | Propagation |
|---|---|---|
| source_class | a1_bridge_source_edge entry | Immutable through entire graph |
| no_real_source_flag | a1_bridge_source_edge entry | Immutable, must always be True in B1 |
| fixture_source_commit | a1_bridge_source_edge entry | Immutable reference to af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| request_hash | a1_factor_bridge_response_node | Computed at entry, immutable downstream |
| response_hash_placeholder | a1_factor_bridge_response_node | Placeholder for future real response |
| factor_decision_hash | a1_factor_bridge_response_node | Propagated through evidence_hash_edge |
| bridge_decision_hash | a1_factor_bridge_response_node | Propagated through evidence_hash_edge |
| graph_node_hash | Each node | Computed per-node, unique per instance |
| graph_edge_hash | Each edge | Computed per-edge, unique per instance |
| permission_tier | permission_tier_edge | Propagated, monotonically non-increasing |
| forbidden_outputs_removed_hash | blocked_output_filter_edge | Computed at filter boundary |
| rollback_marker | degradation_edge | Set on degradation, immutable |
| privacy_marker | document_generation_in_memory_node | Set at doc gen, propagated to terminal |
| c1_handoff_marker | c1_handoff_edge | Set at doc gen, preserved at terminal |

### 2.2 Hash Computation Rules

- graph_node_hash = SHA256(node_type + node_id + input_hashes + config_hash)
- graph_edge_hash = SHA256(edge_type + source_node_hash + target_node_hash)
- factor_decision_hash = inherited from A1FactorBridgeResponse (not recomputed)
- bridge_decision_hash = inherited from A1FactorBridgeResponse (not recomputed)
- forbidden_outputs_removed_hash = SHA256(removed_output_types + removal_timestamp_placeholder)

### 2.3 Evidence Chain Integrity

- Every node must produce graph_node_hash
- Every edge must produce graph_edge_hash
- Hash chain must be verifiable from entry to terminal
- Any break in chain triggers DENY_GRAPH_DAG_INVALID
- Missing evidence on any node/edge triggers DENY_GRAPH_OUTPUTS_UNSAFE

### 2.4 Evidence at Terminal (composition_summary_node)

The terminal node must aggregate:
- All upstream graph_node_hash values
- All upstream graph_edge_hash values
- factor_decision_hash (from bridge)
- bridge_decision_hash (from bridge)
- c1_handoff_marker (from doc gen)
- privacy_marker (from doc gen)
- forbidden_outputs_removed_hash (from filter)

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Evidence computation is deterministic (same inputs = same hash)
- No external service calls for hash computation
- No real source data enters the hash chain (no_real_source_flag = True)
- Evidence is append-only within a single graph run

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO real source data in evidence chain
- NO hash computation that includes real factor outputs
- NO code creation in this planning document

## 6. Proof / Review Requirements

- graph_node_hash proof: every node produces it
- graph_edge_hash proof: every edge produces it
- no_real_source_flag propagation proof
- P1_FIXTURE_ONLY propagation proof (fixture_source_commit)
- source_class propagation proof
- factor_decision_hash propagation proof
- bridge_decision_hash propagation proof
- forbidden_outputs_removed propagation proof
- c1_handoff_marker preservation proof

## 7. Next Legal Entry

- DEGRADATION_PLAN: what happens when evidence chain breaks
- OUTPUT_BOUNDARY_PLAN: what outputs are filtered

---
