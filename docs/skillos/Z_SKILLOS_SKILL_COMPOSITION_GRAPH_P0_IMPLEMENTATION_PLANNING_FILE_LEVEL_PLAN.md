# Z-SkillOS Skill Composition Graph P0 Implementation Planning — FILE LEVEL PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document specifies the complete file-level implementation plan for the Skill Composition Graph P0.
It defines the directory structure, module responsibilities, public API surfaces, import hierarchy,
and inter-module dependency graph. No code files exist; all paths are future targets.

## 2. Directory Structure

```
skillos/capability_invocation_os/composition/
├── __init__.py                              # Package init, public API
├── models/
│   ├── __init__.py                          # Model subpackage init
│   ├── node.py                              # CompositionNode model
│   ├── edge.py                              # CompositionEdge model
│   └── graph.py                             # CompositionGraph model
├── validators/
│   ├── __init__.py                          # Validator subpackage init
│   ├── dag_validator.py                     # DAG structure + cycle detection
│   ├── permission_validator.py              # Tier enforcement
│   └── evidence_validator.py               # Hash chain verification
├── policies/
│   ├── __init__.py                          # Policy subpackage init
│   ├── permission_propagation.py            # Monotonic non-increasing rule
│   ├── evidence_propagation.py              # Hash chain propagation
│   ├── loop_prevention.py                   # Depth + cycle guards
│   └── output_boundary.py                   # Schema + field governance
├── degradation/
│   ├── __init__.py                          # Degradation subpackage init
│   └── degradation_controller.py            # State machine, markers
└── tests/
    ├── __init__.py                          # Test subpackage init
    └── test_composition_graph.py            # Comprehensive test suite
```

Total: 17 files planned. Zero files implemented in P0.

## 3. Module Responsibilities

### 3.1 models/node.py — CompositionNode
- **Purpose**: Data model for a single capability node in the composition graph.
- **Exports**: `CompositionNode`, `NodeContract`, `NodeValidationError`
- **Fields**: capability_id, module_adapter_id, permission_tier, input_schema, output_schema, degradation_result, node_id, created_at, version, metadata
- **Methods**: `validate()`, `to_dict()`, `compute_evidence_hash()`
- **Dependencies**: None (leaf module)

### 3.2 models/edge.py — CompositionEdge
- **Purpose**: Data model for a directed edge between two composition nodes.
- **Exports**: `CompositionEdge`, `EdgeContract`, `EdgeValidationError`
- **Fields**: edge_id, upstream_node_id, downstream_node_id, allowed_data_fields, forbidden_data_fields, evidence_handoff, permission_propagation, created_at, version, metadata
- **Methods**: `validate()`, `to_dict()`, `compute_evidence_hash()`, `check_permission_propagation()`
- **Dependencies**: models/node.py (for node_id references)

### 3.3 models/graph.py — CompositionGraph
- **Purpose**: Container for the full composition graph: nodes + edges + metadata.
- **Exports**: `CompositionGraph`, `GraphBuildError`, `GraphValidationError`
- **Fields**: graph_id, plan_id, nodes, edges, depth, status, created_at, version, decision_hash, rollback_marker
- **Methods**: `add_node()`, `add_edge()`, `build()`, `validate()`, `compute_decision_hash()`
- **Dependencies**: models/node.py, models/edge.py

### 3.4 validators/dag_validator.py — DAG Validator
- **Purpose**: Static DAG structure validation and cycle detection.
- **Exports**: `DAGValidator`, `CycleDetectedError`, `DepthExceededError`
- **Invariants**: DAG-01 through DAG-12
- **Dependencies**: models/graph.py

### 3.5 validators/permission_validator.py — Permission Validator
- **Exports**: `PermissionValidator`, `PermissionEscalationError`, `WriteTierBlockedError`
- **Dependencies**: models/node.py, models/edge.py

### 3.6 validators/evidence_validator.py — Evidence Validator
- **Exports**: `EvidenceValidator`, `HashMismatchError`, `HashDeterminismError`
- **Dependencies**: models/node.py, models/edge.py, models/graph.py

### 3.7 policies/permission_propagation.py
- **Exports**: `PermissionPropagationPolicy`, `PropagationViolationError`
- **Dependencies**: validators/permission_validator.py

### 3.8 policies/evidence_propagation.py
- **Exports**: `EvidencePropagationPolicy`, `ChainBreakError`
- **Dependencies**: validators/evidence_validator.py

### 3.9 policies/loop_prevention.py
- **Exports**: `LoopPreventionPolicy`, `SelfEdgeError`, `CycleDetectedError`, `DepthExceededError`
- **Dependencies**: validators/dag_validator.py

### 3.10 policies/output_boundary.py
- **Exports**: `OutputBoundaryPolicy`, `ForbiddenFieldError`, `SchemaMismatchError`
- **Dependencies**: models/edge.py

### 3.11 degradation/degradation_controller.py
- **Exports**: `DegradationController`, `DegradationState`
- **States**: NOOP, PLAN_ONLY, COMPLETE
- **Dependencies**: models/graph.py

### 3.12 tests/test_composition_graph.py
- **Purpose**: Comprehensive test suite covering all proof categories.
- **Coverage**: >=18 proof categories, all validators, all policies, degradation scenarios

## 4. Import Hierarchy

```
Level 0 (No internal deps):  models/node.py
Level 1 (Depends on L0):     models/edge.py
Level 2 (Depends on L0-1):   models/graph.py
Level 3 (Depends on L2):     validators/dag_validator.py, validators/permission_validator.py, validators/evidence_validator.py
Level 4 (Depends on L3):     policies/permission_propagation.py, policies/evidence_propagation.py, policies/loop_prevention.py, policies/output_boundary.py
Level 5 (Depends on L2):     degradation/degradation_controller.py
Level 6 (Depends on all):    tests/test_composition_graph.py
```

No circular dependencies. Strictly a DAG.

## 5. Public API Surface

The `__init__.py` for `composition/` exports:
```python
from .models.node import CompositionNode, NodeContract, NodeValidationError
from .models.edge import CompositionEdge, EdgeContract, EdgeValidationError
from .models.graph import CompositionGraph, GraphBuildError, GraphValidationError
from .validators.dag_validator import DAGValidator
from .validators.permission_validator import PermissionValidator
from .validators.evidence_validator import EvidenceValidator
from .policies.permission_propagation import PermissionPropagationPolicy
from .policies.evidence_propagation import EvidencePropagationPolicy
from .policies.loop_prevention import LoopPreventionPolicy
from .policies.output_boundary import OutputBoundaryPolicy
from .degradation.degradation_controller import DegradationController, DegradationState
```

## 6. Inter-Module Dependency Graph

```
node.py ───────────────────────────────────────┐
  │                                             │
  ├── edge.py ──────────────────────────┐       │
  │     │                               │       │
  │     ├── graph.py ──────────┐        │       │
  │     │     │                 │        │       │
  │     │     ├── dag_validator.py ── loop_prevention.py
  │     │     ├── permission_validator.py ── permission_propagation.py
  │     │     ├── evidence_validator.py ── evidence_propagation.py
  │     │     └── degradation_controller.py
  │     └── output_boundary.py
  └────────────────────────────────────────────┘
                                    test_composition_graph.py
```

## 7. Implementation Sequencing (P1+)

| Phase | Modules | Priority |
|-------|---------|----------|
| P1.1 | models/node.py, models/edge.py | Foundation data models |
| P1.2 | models/graph.py | Graph container |
| P1.3 | validators/dag_validator.py | Core validation |
| P1.4 | validators/permission_validator.py, validators/evidence_validator.py | Secondary validators |
| P1.5 | All policies (4 modules) | Policy enforcement |
| P1.6 | degradation/degradation_controller.py | Failure handling |
| P1.7 | tests/test_composition_graph.py | Comprehensive test suite |
