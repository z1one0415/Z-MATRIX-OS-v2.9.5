# Z-SkillOS Skill Composition Graph P0 Implementation Planning — DEGRADATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for failure degradation in the composition
graph. Covers degradation state machine, fail-closed prohibition, degradation propagation,
rollback markers, and degradation result contracts.

## 2. Degradation State Machine

### 2.1 States

```
               [COMPLETE]  <-- All nodes and edges valid
                    |
                    | node/edge validation failure
                    v
               [PLAN_ONLY]  <-- Graph structure valid but execution not possible
                    |
                    | graph structure invalid (cycles, depth exceeded)
                    v
               [NOOP]       <-- Graph cannot produce any output
```

### 2.2 State Definitions

| State | Meaning | Impact |
|-------|---------|--------|
| COMPLETE | All validations passed; structurally sound | Dry plan produced; no execution |
| PLAN_ONLY | Structure valid but permissions/evidence prevent execution | Dry plan with degradation annotations |
| NOOP | Structure invalid (cycles, depth, etc.) | No output; empty result envelope |

### 2.3 What Degradation Is NOT (FORBIDDEN)

| FORBIDDEN | Reason |
|-----------|--------|
| Fail-closed | Degradation must always produce a result |
| Infinite retry | No retry loops; degrade immediately |
| Silent failure | All degradation recorded with markers |
| Auto-recovery | No automatic escalation or recovery |
| Partial execution | Whole subgraph degrades if any node degrades |

## 3. Degradation Triggers

| Trigger | From | Degradation Path |
|---------|------|------------------|
| Node validation failure (NC-01..NC-10) | Node model | Node -> NOOP; graph -> PLAN_ONLY |
| Edge validation failure (EC-01..EC-10) | Edge model | Edge -> rejected; graph -> PLAN_ONLY |
| Cycle detected (DAG-05) | DAG validator | Graph -> NOOP |
| Depth exceeded (DAG-03) | DAG validator | Graph -> NOOP |
| Node count exceeded (DAG-02) | DAG validator | Graph -> NOOP |
| Permission escalation (PP-02) | Permission validator | Graph -> FORBIDDEN -> PLAN_ONLY |
| Write tier detected (PP-06) | Permission validator | Graph -> FORBIDDEN -> NOOP |
| Evidence hash mismatch | Evidence validator | Graph -> PLAN_ONLY |
| Self-edge detected (EC-03) | Edge model | Edge -> rejected; graph -> PLAN_ONLY |

## 4. Degradation Propagation

### 4.1 Propagation Rule
When any node or edge degrades, all downstream nodes degrade to the same state.
Upstream nodes that completed before the degradation point retain their status.

```python
def propagate_degradation(graph: CompositionGraph, failed_node_id: str) -> None:
    degraded = {failed_node_id}
    changed = True
    while changed:
        changed = False
        for edge in graph.edges:
            if edge.upstream_node_id in degraded and edge.downstream_node_id not in degraded:
                degraded.add(edge.downstream_node_id)
                changed = True
    for node in graph.nodes:
        if node.node_id in degraded:
            node.metadata["degraded"] = True
            node.metadata["degradation_reason"] = f"Upstream node {failed_node_id} degraded"
```

## 5. Rollback Marker

### 5.1 Marker Definition
```python
@dataclass
class RollbackMarker:
    is_set: bool = False
    trigger_node_id: Optional[str] = None
    trigger_reason: Optional[str] = None
    timestamp: Optional[str] = None
    affected_nodes: List[str] = field(default_factory=list)
```

### 5.2 Effect on Decision Hash
When rollback_marker.is_set=True, the decision hash includes the marker, ensuring
degraded graphs have distinct hashes from COMPLETE graphs.

## 6. Degradation Result Contract

Every node must define a degradation_result:
```json
{
  "degradation_result": {
    "status": "DEGRADED",
    "degradation_state": "NOOP",
    "reason": "Permission tier 4 not allowed in P0",
    "original_capability": "z_matrix_execute_trade",
    "fallback_output": {}
  }
}
```

Required fields: status ("DEGRADED"), degradation_state ("NOOP" or "PLAN_ONLY"), reason, original_capability, fallback_output.

## 7. Degradation Controller API

```python
class DegradationController:
    def degrade_node(self, node: CompositionNode, reason: str) -> None:
        node.metadata["degraded"] = True
        node.metadata["degradation_reason"] = reason

    def degrade_graph(self, graph: CompositionGraph, state: DegradationState, reason: str) -> None:
        graph.status = state.value
        graph.rollback_marker.is_set = True
        graph.rollback_marker.trigger_reason = reason

    def is_degraded(self, graph: CompositionGraph) -> bool:
        return graph.rollback_marker.is_set

    def get_effective_state(self, graph: CompositionGraph) -> str:
        if graph.status == "COMPLETE": return "COMPLETE"
        if graph.status == "PLAN_ONLY": return "PLAN_ONLY"
        return "NOOP"
```
