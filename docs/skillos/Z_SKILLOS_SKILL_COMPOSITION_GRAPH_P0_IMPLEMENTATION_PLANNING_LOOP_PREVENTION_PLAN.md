# Z-SkillOS Skill Composition Graph P0 Implementation Planning — LOOP PREVENTION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for loop prevention in the composition
graph. It covers cycle detection via Kahn's algorithm, self-edge prevention, depth enforcement,
recursion guards, hidden agent loop detection, and the full loop prevention policy.

## 2. Loop Taxonomy

### 2.1 Loop Types and Prevention

| Loop Type | Description | Prevention Mechanism |
|-----------|-------------|---------------------|
| Self-loop | Node A → Node A | EC-03: upstream ≠ downstream enforced at edge creation |
| Direct cycle | Node A → Node B → Node A | Kahn's algorithm at graph build time |
| Indirect cycle | Node A → B → C → A | Kahn's algorithm catches all cycles regardless of length |
| Depth overflow | Chain longer than P0 max depth | Depth counter enforced at every edge addition |
| Hidden agent loop | Node spawns sub-agent that calls back | FORBIDDEN: no node can spawn sub-agents in P0 |
| Dynamic recursion | Node calls itself recursively | FORBIDDEN: no recursion in P0 |
| Fan-out cycle | A→B, A→C, B→C, C→B | DAG-11: no fan-out; DAG-05: cycle detection |

### 2.2 Which Loops Are Possible in P0?

Given P0 constraints (max 2 nodes, strictly sequential, no branching), only these loops are possible:
1. **Self-loop**: A→A (trivially detectable at edge creation)
2. **Direct cycle**: A→B, B→A (detectable at graph build via Kahn's)
3. **Hidden agent loop**: A spawns internal sub-agent (FORBIDDEN by policy; not a graph structure issue)

## 3. Self-Edge Prevention

### 3.1 Detection

Self-edges are detected at edge creation time — before the edge is added to the graph:

```python
def prevent_self_edge(edge: CompositionEdge) -> Optional[SelfEdgeError]:
    if edge.upstream_node_id == edge.downstream_node_id:
        return SelfEdgeError(
            f"Self-edge detected: {edge.upstream_node_id} → {edge.upstream_node_id}"
        )
    return None
```

### 3.2 Enforcement Chain

```
Edge creation request (A→A)
  → prevent_self_edge() detects self-reference
  → raises SelfEdgeError
  → edge is NOT added to graph
  → graph build continues without this edge
  → if this was the only edge, graph status → NOOP
```

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
        return CycleDetectedError(
            f"Cycle detected. Unprocessed nodes: {unprocessed}. "
            f"This indicates at least one cycle in the graph."
        )
    return None
```

### 4.2 Cycle Scenario: A→B + B→A

| Step | Action | Result |
|------|--------|--------|
| 1 | Add edge A→B | Edge accepted |
| 2 | Add edge B→A | Edge accepted (individually valid) |
| 3 | Graph.build() → Kahn's algorithm | in_degree = {A:1, B:1} |
| 4 | Queue starts empty (no zero in-degree nodes) | |
| 5 | Processed = 0, but len(nodes) = 2 | CycleDetectedError raised |
| 6 | Graph → FORBIDDEN → NOOP | |

## 5. Depth Enforcement

### 5.1 Max Depth = 2

```python
MAX_DEPTH_P0 = 2

def enforce_max_depth(graph: CompositionGraph) -> Optional[DepthExceededError]:
    if len(graph.nodes) == 0:
        return None

    # For strictly sequential graphs in P0, depth == node count
    # but compute properly for robustness
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
        return DepthExceededError(
            f"Graph depth {max_depth} exceeds P0 maximum of {MAX_DEPTH_P0}"
        )
    return None
```

### 5.2 Depth Check Timing

Depth is checked:
1. At every edge addition: early rejection before graph build
2. At graph build time: final verification

## 6. Recursion Guards

### 6.1 Dynamic Recursion Prevention

| Guard | Mechanism |
|-------|-----------|
| No recursive capability invocation | Each node has exactly one capability; no nesting |
| No node re-entry | Once a node's output is computed, it cannot be re-invoked |
| No self-referencing plans | A graph cannot contain itself as a subgraph |
| Max call depth = 1 per node | Each node processes exactly once |

### 6.2 Hidden Agent Loop Prevention

```
FORBIDDEN in P0:
- ❌ Any node spawning a sub-agent
- ❌ Any node making recursive calls to the composition engine
- ❌ Any capability that internally builds another composition graph
- ❌ Any tool call that may trigger agent-like behavior
- ❌ Any dynamic capability resolution at runtime
```

## 7. Loop Prevention Policy (LP-01 through LP-08)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| LP-01 | No self-edges (upstream ≠ downstream) | EC-03 at edge creation |
| LP-02 | No cycles (Kahn's algorithm) | DAG-05 at graph build |
| LP-03 | Max depth = 2 | Depth counter at every edge addition |
| LP-04 | Max node count = 2 | Node counter at every node addition |
| LP-05 | No hidden agent loops | Policy; no sub-agent spawning API exposed |
| LP-06 | No dynamic recursion | Policy; capabilities are atomic |
| LP-07 | No fan-out (single outgoing edge per node) | DAG-11 at graph build |
| LP-08 | No fan-in (single incoming edge per node) | DAG-12 at graph build |
