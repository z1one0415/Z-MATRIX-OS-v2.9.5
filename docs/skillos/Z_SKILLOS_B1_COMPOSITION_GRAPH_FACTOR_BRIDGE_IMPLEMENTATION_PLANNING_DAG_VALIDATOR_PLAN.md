# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — DAG VALIDATOR PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: DAG validation rules for B1 composition graph

## 2. Scope

The DAG validator ensures the composition graph is structurally valid before any
processing occurs. B1 consumes A1FactorBridgeResponse ONLY. The validator enforces
that denied context cannot become valid node and that all structural invariants hold.

### 2.1 Validation Rules

| Rule ID | Description | Degradation on Failure |
|---|---|---|
| V-001 | Graph must be acyclic (DAG) | DENY_GRAPH_DAG_INVALID |
| V-002 | No blocked node types present | DENY_GRAPH_SOURCE_FORBIDDEN |
| V-003 | No blocked edge types present | DENY_GRAPH_EXECUTION_FORBIDDEN |
| V-004 | a1_factor_bridge_response_node exists as entry | DENY_GRAPH_BRIDGE_DENIED |
| V-005 | No real source nodes present | DENY_GRAPH_REAL_SOURCE_FORBIDDEN |
| V-006 | All outputs pass blocked filter | DENY_GRAPH_OUTPUTS_UNSAFE |
| V-007 | Permission tier monotonically non-increasing | DENY_GRAPH_SOURCE_FORBIDDEN |
| V-008 | Denied context nodes have no valid-processing edges | DENY_GRAPH_BRIDGE_DENIED |
| V-009 | composition_summary_node is terminal (no outgoing) | DENY_GRAPH_DAG_INVALID |
| V-010 | static_input_node is root (no incoming) | DENY_GRAPH_DAG_INVALID |
| V-011 | c1_handoff_marker present at terminal | DENY_GRAPH_OUTPUTS_UNSAFE |
| V-012 | graph_node_hash present on all nodes | DENY_GRAPH_DAG_INVALID |
| V-013 | graph_edge_hash present on all edges | DENY_GRAPH_DAG_INVALID |
| V-014 | No execution_edge present | DENY_GRAPH_EXECUTION_FORBIDDEN |
| V-015 | No autonomous_retry_edge present | DENY_GRAPH_EXECUTION_FORBIDDEN |

### 2.2 Topological Sort Requirements

- Kahn's algorithm or DFS-based topological sort
- Cycle detection must trigger DENY_GRAPH_DAG_INVALID immediately
- Sort order determines evidence hash propagation sequence

### 2.3 Structural Invariants

- Maximum node count: configurable (planned default: 32)
- Maximum edge count: configurable (planned default: 64)
- Maximum depth: configurable (planned default: 8)
- Single entry point: a1_factor_bridge_response_node (for bridge data)
- Single terminal: composition_summary_node

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Validator operates on in-memory graph representation only
- No disk I/O, no network, no external service calls
- Validation is pre-processing: runs before any node executes
- Validation failure triggers degradation, not exception

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO execution of the graph during validation
- NO code creation in this planning document
- NO bypassing of any validation rule

## 6. Proof / Review Requirements

- DAG acyclic proof must be demonstrable
- Blocked node type proof must enumerate all 13 blocked types
- Blocked edge type proof must enumerate all 8 blocked types
- No execution edge proof must be independently verifiable

## 7. Next Legal Entry

- PERMISSION_PLAN: permission tier propagation rules
- EVIDENCE_PLAN: evidence hash computation planning

---
