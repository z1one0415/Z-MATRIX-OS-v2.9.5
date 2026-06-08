# Z-SkillOS Skill Composition Graph P0 Implementation Planning — DAG VALIDATOR PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for the DAG Validator — the core validation
engine that enforces the static directed acyclic graph structure. It covers topology validation,
Kahn's algorithm for cycle detection and topological sort, depth enforcement, node count limits,
and all 12 DAG invariants.

## 2. DAG Invariants (DAG-01 through DAG-12)

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| DAG-01 | Graph must have exactly one entry point (no incoming edges) | Build-time |
| DAG-02 | Max node count = 2 in P0 | Build-time rejection |
| DAG-03 | Max depth = 2 (longest path from entry to leaf) | Build-time rejection |
| DAG-04 | Topology must be strictly sequential (no branching) | Build-time |
| DAG-05 | No cycles (verified by Kahn's algorithm) | Build-time |
| DAG-06 | Graph is fully connected (if nodes > 1, edges > 0) | Build-time |
| DAG-07 | Self-edges forbidden (upstream ≠ downstream for all edges) | Build-time |
| DAG-08 | All nodes must be reachable from entry point | Build-time |
| DAG-09 | Graph must have no orphan edges (all edges reference existing nodes) | Build-time |
| DAG-10 | If edge count > 0, edge count = node_count - 1 (linear chain) | Build-time |
| DAG-11 | No fan-out: each node has at most one outgoing edge | Build-time |
| DAG-12 | No fan-in: each node has at most one incoming edge | Build-time |

## 3. Kahn's Algorithm — Topological Sort & Cycle Detection

### 3.1 Algorithm Specification

```python
def kahn_topological_sort(graph: CompositionGraph) -> Tuple[List[str], bool]:
    """
    Returns (topological_order, has_cycle).
    Implements Kahn's algorithm for DAG validation.
    """
    in_degree = {node.node_id: 0 for node in graph.nodes}

    for edge in graph.edges:
        in_degree[edge.downstream_node_id] += 1

    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    order = []

    while queue:
        current = queue.pop(0)
        order.append(current)

        for edge in graph.edges:
            if edge.upstream_node_id == current:
                target = edge.downstream_node_id
                in_degree[target] -= 1
                if in_degree[target] == 0:
                    queue.append(target)

    has_cycle = len(order) != len(graph.nodes)
    return order, has_cycle
```

### 3.2 Cycle Detection Scenarios

| Scenario | Expected Result |
|----------|----------------|
| A→B→A (2-node cycle) | has_cycle=True, graph FORBIDDEN |
| A→A (self-edge) | has_cycle=True, graph FORBIDDEN |
| A→B (no cycle) | has_cycle=False, order=[A, B] |
| Single node, no edges | has_cycle=False, order=[A] |
| A→B→C (3 nodes with A→C) | has_cycle=False but rejected by DAG-02 |

## 4. Depth Enforcement

### 4.1 Depth Computation

```python
def compute_depth(graph: CompositionGraph) -> int:
    if len(graph.nodes) == 0:
        return 0
    if len(graph.nodes) == 1:
        return 1

    # For strictly sequential P0 graphs, depth = node_count
    # check that edges form a linear chain
    depths = {node.node_id: 1 for node in graph.nodes}
    for edge in graph.edges:
        depths[edge.downstream_node_id] = max(
            depths[edge.downstream_node_id],
            depths[edge.upstream_node_id] + 1
        )
    return max(depths.values()) if depths else 0
```

### 4.2 Depth Validation

| Graph | Expected Depth | P0 Accepted? |
|-------|---------------|:------------:|
| Single node, 0 edges | 1 | ✅ |
| 2 nodes, A→B | 2 | ✅ |
| 3 nodes, A→B→C | 3 | ❌ DAG-03 |
| 2 nodes, 0 edges (disconnected) | N/A | ❌ DAG-06 |

## 5. Node Count Enforcement

```python
def check_node_count(graph: CompositionGraph) -> Optional[DepthExceededError]:
    if len(graph.nodes) > 2:
        return DepthExceededError(
            f"Node count {len(graph.nodes)} exceeds P0 max of 2"
        )
    return None
```

## 6. Topology Validation — Full Pipeline

```python
def validate_topology(graph: CompositionGraph) -> List[Exception]:
    errors = []

    # DAG-02: Node count
    if len(graph.nodes) > 2:
        errors.append(DepthExceededError(f"Node count {len(graph.nodes)} > 2"))

    # DAG-09: Orphan edge checks
    node_ids = {n.node_id for n in graph.nodes}
    for edge in graph.edges:
        if edge.upstream_node_id not in node_ids:
            errors.append(GraphValidationError(f"Orphan upstream: {edge.upstream_node_id}"))
        if edge.downstream_node_id not in node_ids:
            errors.append(GraphValidationError(f"Orphan downstream: {edge.downstream_node_id}"))

    # DAG-06: Connectedness
    if len(graph.nodes) > 1 and len(graph.edges) == 0:
        errors.append(GraphValidationError("Graph disconnected"))

    # DAG-05: Cycle detection via Kahn
    _, has_cycle = kahn_topological_sort(graph)
    if has_cycle:
        errors.append(CycleDetectedError("Graph contains at least one cycle"))

    # DAG-03: Depth
    depth = compute_depth(graph)
    if depth > 2:
        errors.append(DepthExceededError(f"Depth {depth} > 2"))

    # DAG-10: Linear chain edge count
    if len(graph.nodes) > 1 and len(graph.edges) != len(graph.nodes) - 1:
        errors.append(GraphValidationError("Non-linear topology"))

    # DAG-11/DAG-12: Fan-out/Fan-in
    out_counts = {}
    in_counts = {}
    for edge in graph.edges:
        out_counts[edge.upstream_node_id] = out_counts.get(edge.upstream_node_id, 0) + 1
        in_counts[edge.downstream_node_id] = in_counts.get(edge.downstream_node_id, 0) + 1
    for count in out_counts.values():
        if count > 1:
            errors.append(GraphValidationError("Fan-out detected"))
    for count in in_counts.values():
        if count > 1:
            errors.append(GraphValidationError("Fan-in detected"))

    return errors
```

## 7. DAG Validator Error Taxonomy

| Error Class | Trigger | DAG Rule |
|-------------|---------|----------|
| CycleDetectedError | Kahn's algorithm detects unprocessed nodes | DAG-05 |
| DepthExceededError | Depth > 2 or node count > 2 | DAG-02, DAG-03 |
| GraphValidationError | Any other topology violation | DAG-01,04,06-12 |
| OrphanEdgeError | Edge references missing node | DAG-09 |
| DisconnectedGraphError | Nodes without connecting edges | DAG-06 |
| FanOutError | Node has >1 outgoing edge | DAG-11 |
| FanInError | Node has >1 incoming edge | DAG-12 |
