# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — NODE MODEL PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Node type model specifications for B1 composition graph

## 2. Scope

This document specifies the 8 ALLOWED node types for the B1 composition graph.
B1 consumes A1FactorBridgeResponse ONLY. The a1_factor_bridge_response_node is the
primary data entry point. Denied context cannot become valid node.

### 2.1 ALLOWED Node Types (8)

#### static_input_node
- Purpose: Provides immutable configuration context to the graph
- Inputs: None (root node)
- Outputs: readonly_context_edge to downstream nodes
- Evidence: graph_node_hash
- Constraints: Must be DAG root, no incoming edges

#### capability_registry_node
- Purpose: Enumerates available capabilities without invoking them
- Inputs: readonly_context_edge from static_input_node
- Outputs: permission_tier_edge to downstream
- Evidence: graph_node_hash, permission_tier
- Constraints: Read-only registry lookup, no execution

#### a1_factor_bridge_response_node
- Purpose: Receives and validates A1FactorBridgeResponse payloads
- Inputs: a1_bridge_source_edge from bridge layer
- Outputs: evidence_hash_edge to factor_evidence_summary_node
- Evidence: source_class, no_real_source_flag, fixture_source_commit, request_hash,
  response_hash_placeholder, factor_decision_hash, bridge_decision_hash, graph_node_hash
- Constraints: MUST only accept A1FactorBridgeResponse, NEVER FactorInvocationResponse

#### a1_factor_bridge_denied_context_node
- Purpose: Receives denied bridge contexts for audit/degradation routing
- Inputs: denied_context_edge from bridge layer
- Outputs: degradation_edge to degradation handler
- Evidence: bridge_decision_hash, graph_node_hash, rollback_marker
- Constraints: Denied context cannot become valid node — must route to degradation ONLY

#### factor_evidence_summary_node
- Purpose: Aggregates evidence from bridge response into summary
- Inputs: evidence_hash_edge from a1_factor_bridge_response_node
- Outputs: readonly_context_edge to document_generation_in_memory_node
- Evidence: factor_decision_hash, graph_node_hash, forbidden_outputs_removed_hash
- Constraints: Must filter blocked outputs before passing downstream

#### local_report_reading_node
- Purpose: Reads local report files for context enrichment
- Inputs: readonly_context_edge from static_input_node
- Outputs: readonly_context_edge to composition_summary_node
- Evidence: graph_node_hash
- Constraints: Read-only file access, no network, no external API

#### document_generation_in_memory_node
- Purpose: Generates planning documents in memory (no disk write in graph)
- Inputs: readonly_context_edge from factor_evidence_summary_node
- Outputs: c1_handoff_edge to composition_summary_node
- Evidence: graph_node_hash, c1_handoff_marker, privacy_marker
- Constraints: In-memory only, no side effects

#### composition_summary_node
- Purpose: Final aggregation node producing the composition summary
- Inputs: c1_handoff_edge, readonly_context_edge from upstream nodes
- Outputs: Terminal (DAG leaf)
- Evidence: All upstream hashes aggregated, c1_handoff_marker preserved
- Constraints: Must preserve c1_handoff_marker, must be DAG terminal

### 2.2 BLOCKED Node Types (13)

These MUST NEVER appear in the B1 composition graph:
- factor_library_direct_node — bypasses A1 bridge
- real_factor_node — real factor invocation
- z2_runtime_node — runtime execution
- z8_execution_node — Z8 execution layer
- z9_memory_mutation_node — memory mutation
- v3_sandbox_node — sandbox execution
- broker_node — brokerage operations
- real_trade_node — real trading
- alpha_signal_node — alpha signal generation
- paper_trading_node — paper trading simulation
- portfolio_weight_node — portfolio weight calculation
- order_signal_node — order signal emission
- production_node — production deployment

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Only 8 ALLOWED node types may be instantiated
- Each node must carry graph_node_hash evidence
- a1_factor_bridge_response_node is the ONLY bridge entry point
- Denied context nodes MUST route to degradation, never to valid processing

## 5. Forbidden Actions

- NO creation of blocked node types
- NO runtime enablement (runtime enablement is not authorized)
- NO execution of any node (planning only)
- NO direct Factor Library consumption

## 6. Proof / Review Requirements

- Each allowed node type must have defined inputs/outputs/evidence/constraints
- Each blocked node type must have stated reason for blocking
- graph_node_hash must be planned for every node type

## 7. Next Legal Entry

- EDGE_MODEL_PLAN: defines the connections between these nodes
- DAG_VALIDATOR_PLAN: validates the assembled graph structure

---
