# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — SCOPE

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Classification: Dry-plan composition graph — NOT runtime, NOT execution

## 2. Scope

### 2.1 In-Scope

This document defines what the B1 Composition Graph Factor Bridge covers:

- Planning the composition DAG that processes A1FactorBridgeResponse
- Defining node models for 8 allowed node types
- Defining edge models for 8 allowed edge types
- Specifying degradation decisions for invalid graph states
- Specifying evidence hash propagation through the DAG
- Planning the a1_factor_bridge_response_node as the sole entry point
- Planning denied context routing (denied context cannot become valid node)
- Planning c1_handoff_marker preservation at composition_summary_node

### 2.2 Out-of-Scope

- Runtime execution of any node
- Real factor invocation
- Direct FactorInvocationResponse consumption (B1 consumes A1FactorBridgeResponse ONLY)
- Any trading, brokering, or alpha signal generation
- Code implementation (planned for future phase)
- Test implementation (planned for future phase)

### 2.3 Future Files (plan only, DO NOT create)

Code files:
- skillos/capability_invocation_os/composition_graph/__init__.py
- skillos/capability_invocation_os/composition_graph/constants.py
- skillos/capability_invocation_os/composition_graph/config.py
- skillos/capability_invocation_os/composition_graph/models.py
- skillos/capability_invocation_os/composition_graph/contracts.py
- skillos/capability_invocation_os/composition_graph/node_builder.py
- skillos/capability_invocation_os/composition_graph/edge_builder.py
- skillos/capability_invocation_os/composition_graph/dag_validator.py
- skillos/capability_invocation_os/composition_graph/evidence.py
- skillos/capability_invocation_os/composition_graph/degradation.py
- skillos/capability_invocation_os/composition_graph/graph.py
- skillos/capability_invocation_os/composition_graph/kill_switch.py

Test files:
- tests/skillos/capability_invocation_os/composition_graph/test_disabled_default.py
- tests/skillos/capability_invocation_os/composition_graph/test_models.py
- tests/skillos/capability_invocation_os/composition_graph/test_node_builder.py
- tests/skillos/capability_invocation_os/composition_graph/test_edge_builder.py
- tests/skillos/capability_invocation_os/composition_graph/test_dag_validator.py
- tests/skillos/capability_invocation_os/composition_graph/test_evidence.py
- tests/skillos/capability_invocation_os/composition_graph/test_degradation.py
- tests/skillos/capability_invocation_os/composition_graph/test_no_forbidden_imports.py

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- B1 is a dry-plan composition graph
- All node types must be from the 8 ALLOWED types only
- All edge types must be from the 8 ALLOWED types only
- 13 BLOCKED node types must never appear in the planned graph
- 8 BLOCKED edge types must never appear in the planned graph
- The graph MUST be a DAG (directed acyclic graph)
- a1_factor_bridge_response_node is the sole bridge entry point

## 5. Forbidden Actions

- NO code, tests, or implementation artifacts
- NO runtime enablement (runtime enablement is not authorized in this phase)
- NO execution of adapters or capabilities
- NO consumption of FactorInvocationResponse directly
- NO creation of research files, runtime_reports, runtime_audit, or data files

## 6. Proof / Review Requirements

- Every scope item must trace to at least one proof item in the Test and Proof Plan
- Scope boundaries must be verifiable by file-system inspection (no code exists)
- All dependency seals must be verifiable against git history

## 7. Next Legal Entry

- FILE_LEVEL_PLAN: detailed per-file planning
- NODE_MODEL_PLAN: node type specifications
- EDGE_MODEL_PLAN: edge type specifications

---
