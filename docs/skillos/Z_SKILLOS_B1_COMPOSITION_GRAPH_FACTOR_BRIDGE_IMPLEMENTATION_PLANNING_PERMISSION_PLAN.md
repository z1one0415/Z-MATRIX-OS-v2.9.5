# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — PERMISSION PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Permission tier model for B1 composition graph

## 2. Scope

This document defines the permission tier system for the B1 composition graph.
B1 consumes A1FactorBridgeResponse ONLY. Permission tiers control what operations
each node may perform. Denied context cannot become valid node.

### 2.1 Permission Levels

| Level | Name | Capabilities | Nodes |
|---|---|---|---|
| 1 | READONLY_STATIC | Read config only | static_input_node |
| 2 | REGISTRY_LOOKUP | Read capability registry | capability_registry_node |
| 3 | BRIDGE_CONSUME | Consume A1FactorBridgeResponse | a1_factor_bridge_response_node |
| 4 | EVIDENCE_AGGREGATE | Aggregate evidence hashes | factor_evidence_summary_node |
| 5 | DOCUMENT_GENERATE | Generate in-memory docs | document_generation_in_memory_node |
| 6 | REPORT_READ | Read local reports | local_report_reading_node |
| 7 | COMPOSITION_SUMMARY | Produce final summary | composition_summary_node |
| DENIED | DENIED_CONTEXT | Degradation routing only | a1_factor_bridge_denied_context_node |

### 2.2 Permission Propagation Rules

- Permission tier is carried on permission_tier_edge
- Permission can only DEGRADE along edge direction (Level N → Level ≥N)
- A node cannot perform operations above its permission level
- Denied context tier is terminal — no escalation possible
- Level 5 (DOCUMENT_GENERATE) is blocked from any execution or trading output

### 2.3 Permission Enforcement Points

- Node instantiation: check node type matches required permission level
- Edge creation: verify source permission ≤ target permission expectation
- Output filtering: blocked_output_filter_edge enforces at Level 4→5 boundary
- Terminal node: composition_summary_node accepts any valid upstream tier

### 2.4 Blocked Permission Operations

The following operations are NEVER permitted at any level:
- Runtime execution (any level)
- Real factor invocation (any level)
- Trading operations (any level)
- Alpha signal generation (any level)
- Autonomous retry (any level)
- State mutation (any level)

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

Evidence preserved at permission boundaries: permission_tier, graph_node_hash,
graph_edge_hash, c1_handoff_marker.

## 4. Boundary

- Permission model is static (defined at graph construction, not runtime)
- No dynamic permission escalation
- No permission bypass mechanism
- All permission checks are planning-phase constraints

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO permission escalation
- NO dynamic permission changes
- NO code creation

## 6. Proof / Review Requirements

- Permission tier monotonicity proof
- Level 5 blocked proof (no execution at document generation)
- Denied context isolation proof
- c1_handoff_marker preservation across permission boundaries

## 7. Next Legal Entry

- EVIDENCE_PLAN: evidence hash computation
- DEGRADATION_PLAN: degradation decision routing

---
