# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — OUTPUT BOUNDARY PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Output boundary and filtering for B1 composition graph

## 2. Scope

This document defines what outputs are ALLOWED and BLOCKED from the B1 composition
graph. B1 consumes A1FactorBridgeResponse ONLY. The blocked_output_filter_edge
enforces output filtering. Denied context cannot become valid node.

### 2.1 ALLOWED Outputs

| Output Type | Description | Producer Node |
|---|---|---|
| composition_summary | Readonly summary of factor evidence | composition_summary_node |
| evidence_hash_report | Hash chain integrity report | composition_summary_node |
| degradation_report | Degradation decision audit trail | composition_summary_node |
| planning_document | In-memory planning document | document_generation_in_memory_node |
| c1_handoff_payload | Handoff data for C1 orchestration | composition_summary_node |

### 2.2 BLOCKED Outputs (ABSOLUTE FORBIDDEN)

| Blocked Output | Reason | Filter Point |
|---|---|---|
| alpha_claim | Trading signal — forbidden in planning graph | blocked_output_filter_edge |
| position_weight | Portfolio allocation — forbidden | blocked_output_filter_edge |
| buy_signal | Trade execution — forbidden | blocked_output_filter_edge |
| sell_signal | Trade execution — forbidden | blocked_output_filter_edge |
| order_signal | Order routing — forbidden | blocked_output_filter_edge |
| broker_instruction | Brokerage — forbidden | blocked_output_filter_edge |
| real_trade_instruction | Real trading — forbidden | blocked_output_filter_edge |
| production_deployment | Production — forbidden | blocked_output_filter_edge |
| alpha_signal | Alpha generation — forbidden | blocked_output_filter_edge |
| runtime_execution_result | Runtime — forbidden | blocked_output_filter_edge |

### 2.3 Output Filtering Mechanism

The blocked_output_filter_edge operates between factor_evidence_summary_node and
document_generation_in_memory_node. It:
1. Inspects all output fields in the evidence payload
2. Removes any field matching blocked output types
3. Computes forbidden_outputs_removed_hash over removed fields
4. Passes only allowed outputs downstream
5. If ALL outputs are blocked → DENY_GRAPH_OUTPUTS_UNSAFE

### 2.4 Output Evidence

Every output carries:
- forbidden_outputs_removed_hash (what was filtered)
- c1_handoff_marker (preserved)
- privacy_marker (set)
- graph_node_hash (of producing node)

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Output filtering is mandatory (cannot be bypassed)
- No blocked output type may reach composition_summary_node
- Filter operates at evidence level (not string matching)
- Only allowed output types defined in 2.1 may exit the graph

## 5. Forbidden Actions

- NO alpha_claim generation or passthrough
- NO position_weight calculation or passthrough
- NO buy/sell signal generation
- NO order_signal emission
- NO runtime enablement (runtime enablement is not authorized)
- NO code creation in this planning document

## 6. Proof / Review Requirements

- alpha_claim blocked proof
- position_weight blocked proof
- buy/sell signal blocked proof
- order_signal blocked proof
- production/broker/real_trade blocked proof
- blocked output filtering proof (mechanism verification)
- forbidden_outputs_removed propagation proof

## 7. Next Legal Entry

- ROLLBACK_PLAN: rollback mechanism when outputs fail filtering
- TEST_AND_PROOF_PLAN: comprehensive proof categories

---
