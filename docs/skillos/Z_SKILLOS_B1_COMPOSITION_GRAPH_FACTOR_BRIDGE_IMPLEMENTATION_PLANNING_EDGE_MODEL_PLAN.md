# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — EDGE MODEL PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Edge type model specifications for B1 composition graph

## 2. Scope

This document specifies the 8 ALLOWED edge types for the B1 composition graph.
Edges connect nodes in a DAG structure. B1 consumes A1FactorBridgeResponse ONLY.
The graph must be acyclic. Denied context cannot become valid node.

### 2.1 ALLOWED Edge Types (8)

#### readonly_context_edge
- Purpose: Passes immutable context between nodes without side effects
- Source nodes: static_input_node, factor_evidence_summary_node, local_report_reading_node
- Target nodes: capability_registry_node, factor_evidence_summary_node, composition_summary_node
- Evidence carried: graph_edge_hash
- Constraints: Read-only, no mutation, no execution trigger

#### evidence_hash_edge
- Purpose: Carries evidence hash chain from bridge response to summary
- Source nodes: a1_factor_bridge_response_node
- Target nodes: factor_evidence_summary_node
- Evidence carried: graph_edge_hash, factor_decision_hash, bridge_decision_hash
- Constraints: Hash integrity must be preserved end-to-end

#### permission_tier_edge
- Purpose: Propagates permission tier context between nodes
- Source nodes: capability_registry_node
- Target nodes: factor_evidence_summary_node, document_generation_in_memory_node
- Evidence carried: graph_edge_hash, permission_tier
- Constraints: Permission can only degrade (never escalate) along edge direction

#### degradation_edge
- Purpose: Routes denied/invalid contexts to degradation handling
- Source nodes: a1_factor_bridge_denied_context_node
- Target nodes: composition_summary_node (with degradation marker)
- Evidence carried: graph_edge_hash, rollback_marker
- Constraints: Degradation is terminal — no recovery path within same graph run

#### denied_context_edge
- Purpose: Carries denied bridge context to the denied context node
- Source nodes: Bridge layer (external input)
- Target nodes: a1_factor_bridge_denied_context_node
- Evidence carried: graph_edge_hash, bridge_decision_hash
- Constraints: Denied context cannot become valid node — must terminate in degradation

#### blocked_output_filter_edge
- Purpose: Filters blocked outputs (alpha, position, signals) before downstream
- Source nodes: factor_evidence_summary_node
- Target nodes: document_generation_in_memory_node
- Evidence carried: graph_edge_hash, forbidden_outputs_removed_hash
- Constraints: MUST remove alpha_claim, position_weight, buy/sell signal, order_signal

#### c1_handoff_edge
- Purpose: Carries C1 handoff marker for downstream orchestration
- Source nodes: document_generation_in_memory_node
- Target nodes: composition_summary_node
- Evidence carried: graph_edge_hash, c1_handoff_marker
- Constraints: c1_handoff_marker must be preserved intact at terminal node

#### a1_bridge_source_edge
- Purpose: Entry edge from A1 bridge response into the composition graph
- Source nodes: External A1 bridge layer
- Target nodes: a1_factor_bridge_response_node
- Evidence carried: graph_edge_hash, source_class, no_real_source_flag, fixture_source_commit
- Constraints: ONLY A1FactorBridgeResponse may traverse this edge

### 2.2 BLOCKED Edge Types (8)

These MUST NEVER appear in the B1 composition graph:
- execution_edge — triggers code execution
- trade_edge — triggers trade operations
- broker_edge — connects to brokerage
- real_time_feedback_edge — real-time data feedback loop
- autonomous_retry_edge — autonomous retry without human approval
- mutation_edge — mutates state
- production_edge — production deployment path
- alpha_signal_edge — alpha signal propagation

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Only 8 ALLOWED edge types may be instantiated
- Each edge must carry graph_edge_hash evidence
- Edges must respect DAG constraint (no cycles)
- Permission can only degrade along edge direction, never escalate
- Blocked output filter edge is mandatory before document generation

## 5. Forbidden Actions

- NO creation of blocked edge types
- NO runtime enablement (runtime enablement is not authorized)
- NO execution triggering through any edge
- NO autonomous retry or feedback loops

## 6. Proof / Review Requirements

- Each allowed edge type has defined source/target/evidence/constraints
- Each blocked edge type has stated reason for blocking
- graph_edge_hash must be planned for every edge type
- DAG constraint must be provably maintained by edge connectivity

## 7. Next Legal Entry

- DAG_VALIDATOR_PLAN: ensures assembled graph meets all structural constraints
- PERMISSION_PLAN: details the permission tier propagation rules

---
