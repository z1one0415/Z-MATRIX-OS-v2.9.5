# Z-SkillOS Skill Composition Graph P0 Implementation Planning — LOOP PREVENTION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for loop prevention in the composition
graph. Covers cycle detection via Kahn's algorithm, self-edge prevention, depth enforcement,
recursion guards, hidden agent loop detection, and the full loop prevention policy.

## 2. Loop Taxonomy

| Loop Type | Description | Prevention Mechanism |
|-----------|-------------|---------------------|
| Self-loop | Node A -> Node A | EC-03: upstream != downstream |
| Direct cycle | Node A -> Node B -> Node A | Kahn's algorithm at build time |
| Indirect cycle | Node A -> B -> C -> A | Kahn's algorithm catches all |
| Depth overflow | Chain > P0 max depth | Depth counter at every edge |
| Hidden agent loop | Node spawns sub-agent that calls back | FORBIDDEN: no sub-agent spawning |
| Dynamic recursion | Node calls itself recursively | FORBIDDEN: no recursion in P0 |

## 3. Self-Edge Prevention

```python
def prevent_self_edge(edge: CompositionEdge) -> Optional[SelfEdgeError]:
    if edge.upstream_node_id == edge.downstream_node_id:
        return SelfEdgeError(f"Self-edge: {edge.upstream_node_id} -> {edge.upstream_node_id}")
    return None
```

Enforcement chain: Edge creation -> prevent_self_edge() -> SelfEdgeError -> Edge NOT added -> Graph may become NOOP.

## 4. Direct Cycle Prevention via Kahn's Algorithm

### 4.1 Two-Node Backedge Detection

```python
def prevent_cycle(graph: CompositionGraph) -> Optional[CycleDetectedError]:
    in_degree = {node.node_id: 0 for node in graph.nodes}
    for edge in graph.edges:
        in_degree[edge.downstream_node_id] += 1
    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    processed = 0
    while queue:
        current = queue.pop(0)
        processed += 1
        for edge in graph.edges:
            if edge.upstream_node_id == current:
                in_degree[edge.downstream_node_id] -= 1
                if in_degree[edge.downstream_node_id] == 0:
                    queue.append(edge.downstream_node_id)
    if processed != len(graph.nodes):
        unprocessed = [nid for nid, deg in in_degree.items() if deg > 0]
        return CycleDetectedError(f"Cycle detected. Unprocessed: {unprocessed}")
    return None
```

### 4.2 Cycle Scenario: A->B + B->A
| Step | Action | Result |
|------|--------|--------|
| 1 | Add edge A->B | Edge accepted |
| 2 | Add edge B->A | Edge accepted (individually valid) |
| 3 | Graph.build() -> Kahn's | in_degree = {A:1, B:1} |
| 4 | Queue empty (no zero in-degree) | Processed=0 but len(nodes)=2 |
| 5 | CycleDetectedError | Graph -> FORBIDDEN -> NOOP |

## 5. Depth Enforcement

```python
MAX_DEPTH_P0 = 2

def enforce_max_depth(graph: CompositionGraph) -> Optional[DepthExceededError]:
    if len(graph.nodes) == 0: return None
    depths = {node.node_id: 1 for node in graph.nodes}
    changed = True
    while changed:
        changed = False
        for edge in graph.edges:
            new_depth = depths[edge.upstream_node_id] + 1
            if new_depth > depths[edge.downstream_node_id]:
                depths[edge.downstream_node_id] = new_depth
                changed = True
    max_depth = max(depths.values())
    if max_depth > MAX_DEPTH_P0:
        return DepthExceededError(f"Depth {max_depth} exceeds P0 max of {MAX_DEPTH_P0}")
    return None
```

## 6. Recursion Guards

| Guard | Mechanism |
|-------|-----------|
| No recursive capability invocation | Each node has exactly one capability |
| No node re-entry | Once output computed, cannot be re-invoked |
| No self-referencing plans | Graph cannot contain itself as subgraph |
| Max call depth = 1 per node | Each node processes exactly once |

### Hidden Agent Loop Prevention (FORBIDDEN in P0)
- ❌ Any node spawning a sub-agent
- ❌ Any node making recursive calls to the composition engine
- ❌ Any capability that internally builds another composition graph
- ❌ Any tool call that may trigger agent-like behavior
- ❌ Any dynamic capability resolution at runtime

## 7. Loop Prevention Policy Rules (LP-01 through LP-08)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| LP-01 | No self-edges (upstream != downstream) | EC-03 at edge creation |
| LP-02 | No cycles (Kahn's algorithm) | DAG-05 at graph build |
| LP-03 | Max depth = 2 | Depth counter at every edge |
| LP-04 | Max node count = 2 | Node counter at every node |
| LP-05 | No hidden agent loops | Policy; no sub-agent API |
| LP-06 | No dynamic recursion | Policy; capabilities atomic |
| LP-07 | No fan-out (single outgoing edge) | DAG-11 at graph build |
| LP-08 | No fan-in (single incoming edge) | DAG-12 at graph build |
