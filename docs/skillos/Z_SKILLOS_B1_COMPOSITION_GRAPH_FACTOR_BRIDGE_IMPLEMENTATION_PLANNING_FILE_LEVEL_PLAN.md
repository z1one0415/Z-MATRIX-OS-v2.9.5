# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — FILE LEVEL PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- This document plans future implementation files. NO code is created here.

## 2. Scope

This file-level plan describes the structure, responsibilities, and contracts for
each planned implementation file. B1 consumes A1FactorBridgeResponse ONLY — never
FactorInvocationResponse directly.

### 2.1 Planned Code Files

| # | File | Responsibility |
|---|---|---|
| 1 | __init__.py | Package marker, version constant, kill-switch re-export |
| 2 | constants.py | ALLOWED/BLOCKED node types, edge types, degradation decisions |
| 3 | config.py | Graph configuration (max nodes, max edges, timeout placeholders) |
| 4 | models.py | Pydantic models for nodes, edges, graph state |
| 5 | contracts.py | Input/output contracts, A1FactorBridgeResponse consumption |
| 6 | node_builder.py | Factory for building allowed node instances |
| 7 | edge_builder.py | Factory for building allowed edge instances |
| 8 | dag_validator.py | DAG acyclicity, blocked type detection, structural validation |
| 9 | evidence.py | Evidence hash chain computation and propagation |
| 10 | degradation.py | Degradation decision engine (8 decisions) |
| 11 | graph.py | Main composition graph assembly orchestrator |
| 12 | kill_switch.py | DISABLED_DEFAULT_NOOP implementation, global disable |

### 2.2 Planned Test Files

| # | File | Coverage Target |
|---|---|---|
| 1 | test_disabled_default.py | Kill switch defaults to disabled |
| 2 | test_models.py | Model validation, serialization |
| 3 | test_node_builder.py | Allowed nodes build, blocked nodes reject |
| 4 | test_edge_builder.py | Allowed edges build, blocked edges reject |
| 5 | test_dag_validator.py | Acyclicity, blocked detection, structural |
| 6 | test_evidence.py | Hash propagation, chain integrity |
| 7 | test_degradation.py | All 8 degradation decisions |
| 8 | test_no_forbidden_imports.py | No import of blocked modules |

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

All files must import from A1 bridge response types. The a1_factor_bridge_response_node
is the sole data entry point. Denied context cannot become valid node.

## 4. Boundary

- All files reside under skillos/capability_invocation_os/composition_graph/
- Tests reside under tests/skillos/capability_invocation_os/composition_graph/
- No file may import from factor_library directly
- No file may import execution, trading, or broker modules
- c1_handoff_marker must be preserved through the graph pipeline

## 5. Forbidden Actions

- DO NOT create any of the above files in this planning phase
- NO runtime enablement (runtime enablement is not authorized)
- NO code generation, no stub files, no skeleton implementations
- NO research files, no data files, no runtime_reports

## 6. Proof / Review Requirements

- File-level plan completeness: every planned file has defined responsibility
- No planned file exceeds single-responsibility principle
- Every planned file traces to at least one test file
- Evidence hash propagation coverage: every hash field has a planned owner

## 7. Next Legal Entry

- Implementation phase (separate branch, after review approval)
- NODE_MODEL_PLAN and EDGE_MODEL_PLAN detail the type specifications

---
