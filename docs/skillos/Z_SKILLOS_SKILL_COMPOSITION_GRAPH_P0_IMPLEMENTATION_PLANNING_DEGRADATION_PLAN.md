# Z-SkillOS Skill Composition Graph P0 Implementation Planning — DEGRADATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for failure degradation in the composition
graph. It covers the degradation state machine, fail-closed prohibition, degradation propagation,
rollback markers, and degradation result contracts for every node.

## 2. Degradation State Machine

### 2.1 States

```
               ┌──────────┐
     build() → │ COMPLETE │ ← All nodes and edges valid
               └────┬─────┘
                    │ node/edge validation failure
                    ▼
               ┌──────────┐
               │PLAN_ONLY │ ← Graph structure valid but execution not possible
               └────┬─────┘
                    │ graph structure invalid (cycles, depth exceeded, etc.)
                    ▼
               ┌──────────┐
               │  NOOP    │ ← Graph cannot produce any output
               └──────────┘
```

### 2.2 State Definitions

| State | Meaning | Impact |
|-------|---------|--------|
| COMPLETE | All validations passed; graph is structurally sound | Dry plan can be produced; no execution |
| PLAN_ONLY | Graph structure is valid but permissions/evidence/contracts prevent execution | Dry plan produced with degradation annotations |
| NOOP | Graph structure is invalid (cycles, depth exceeded, etc.) | No output; empty result envelope |

### 2.3 What Degradation Is NOT

| FORBIDDEN | Reason |
|-----------|--------|
| Fail-closed | Degradation must always produce a result; never block |
| Infinite retry | No retry loops; degrade immediately |
| Silent failure | All degradation must be recorded with markers |
| Auto-recovery | No automatic escalation or recovery logic |
| Partial execution | If any node degrades, the whole subgraph degrades |

## 3. Degradation Triggers

| Trigger | From | Degradation Path |
|---------|------|------------------|
| Node validation failure (NC-01..NC-10) | Node model | Node → NOOP; graph → PLAN_ONLY |
| Edge validation failure (EC-01..EC-10) | Edge model | Edge → rejected; graph → PLAN_ONLY |
| Cycle detected (DAG-05) | DAG validator | Graph → NOOP |
| Depth exceeded (DAG-03) | DAG validator | Graph → NOOP |
| Node count exceeded (DAG-02) | DAG validator | Graph → NOOP |
| Permission escalation (PP-02) | Permission validator | Graph → FORBIDDEN → PLAN_ONLY |
| Write tier detected (PP-06) | Permission validator | Graph → FORBIDDEN → NOOP |
| Evidence hash mismatch | Evidence validator | Graph → PLAN_ONLY |
| Self-edge detected (EC-03) | Edge model | Edge → rejected; graph → PLAN_ONLY |
| Forbidden field intersection (EC-05) | Edge model | Edge → rejected; graph → PLAN_ONLY |

## 4. Degradation Propagation

### 4.1 Propagation Rule

When any node or edge degrades, all downstream nodes in the graph degrade to the same state.
Upstream nodes that completed successfully before the degradation point retain their status.

### 4.2 Propagation Algorithm

```python
def propagate_degradation(graph: CompositionGraph, failed_node_id: str) -> None:
    """Propagate degradation downstream from the failed node."""
    degraded = {failed_node_id}

    # Find all downstream nodes (transitive closure)
    changed = True
    while changed:
        changed = False
        for edge in graph.edges:
            if edge.upstream_node_id in degraded and edge.downstream_node_id not in degraded:
                degraded.add(edge.downstream_node_id)
                changed = True

    # Mark all degraded nodes
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

### 5.2 When to Set

The rollback marker is set when:
1. Any node fails validation with NC rules
2. Any edge fails validation with EC rules
3. DAG topology validation fails
4. Permission escalation is detected
5. Evidence chain is broken

### 5.3 Effect on Decision Hash

When `rollback_marker.is_set = True`, the graph decision hash includes the rollback marker,
ensuring that a degraded graph's decision hash differs from a COMPLETE graph's hash.

## 6. Degradation Result Contract

### 6.1 Per-Node Degradation Result

Every node must define a `degradation_result` field. This is the output produced when the node
degrades instead of completing normally.

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

### 6.2 Required Fields in Degradation Result

| Field | Type | Description |
|-------|------|-------------|
| status | str | Always "DEGRADED" |
| degradation_state | str | "NOOP" or "PLAN_ONLY" |
| reason | str | Human-readable explanation |
| original_capability | str | The capability that would have been invoked |
| fallback_output | dict | The noop/plan-only output |

## 7. Degradation Controller API

```python
class DegradationController:
    """Manages degradation states and propagation."""

    def degrade_node(self, node: CompositionNode, reason: str) -> None:
        """Set a single node to DEGRADED state."""
        node.metadata["degraded"] = True
        node.metadata["degradation_reason"] = reason

    def degrade_graph(self, graph: CompositionGraph,
                      state: DegradationState, reason: str) -> None:
        """Degrade entire graph to a specific state."""
        graph.status = state.value
        graph.rollback_marker.is_set = True
        graph.rollback_marker.trigger_reason = reason

    def is_degraded(self, graph: CompositionGraph) -> bool:
        """Check if graph has been degraded."""
        return graph.rollback_marker.is_set

    def get_effective_state(self, graph: CompositionGraph) -> str:
        """Get the effective execution state of the graph."""
        if graph.status == "COMPLETE":
            return "COMPLETE"
        if graph.status == "PLAN_ONLY":
            return "PLAN_ONLY"
        return "NOOP"
```
