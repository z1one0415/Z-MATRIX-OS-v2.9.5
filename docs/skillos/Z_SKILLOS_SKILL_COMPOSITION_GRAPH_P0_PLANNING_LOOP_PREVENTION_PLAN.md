# Z-SkillOS Skill Composition Graph P0 Planning — LOOP PREVENTION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Loop Prevention Definition

Loop Prevention ensures the composition graph remains a strict DAG with no cycles,
no self-references, no hidden agent loops, and no recursive tool invocation. The graph
must be fully analyzable at compile time for all possible loop types.

## 2. Loop Categories Covered

| Category | Description | Detection Method |
|----------|-------------|-----------------|
| L1: Self-Edge | Node connects to itself | Edge contract: upstream == downstream |
| L2: Simple Cycle | A → B → A (2-node cycle) | Kahn's algorithm + depth check |
| L3: Indirect Cycle | A → B → C → A (n-node cycle) | Topological sort (N/A in P0: max 2 nodes) |
| L4: Tool Recursion | Node capability calls itself via graph traversal | Capability call graph analysis |
| L5: Agent Loop | Hidden agent spawns sub-agent that re-enters graph | Static analysis of node implementation |
| L6: Dynamic Recursion | Runtime graph modification creates cycles | Prohibited: graph is immutable post-build |

## 3. P0 Structural Loop Prevention

Since P0 limits graphs to 2 nodes, cycle prevention is structurally guaranteed:

### 3.1 Single-Node Graph
- No edges exist
- Only possible loop: self-edge → prevented by edge contract rule EC-03
- No cycle possible

### 3.2 Two-Node Graph
- One edge: N0 → N1
- Possible loop: N1 → N0 (reverse edge)
- This would create a second edge, but P0 allows exactly 1 edge → rejected by edge count limit
- Even without the edge count limit, N1→N0 would create a depth-3 path (N0→N1→N0) → rejected by depth limit (max 2)
- No cycle possible in valid graph

## 4. Tool Recursion Prevention (L4)

Tool recursion is when a capability invocation within a node triggers another graph execution
that could form a cycle.

### 4.1 Detection
- Build a capability call graph: which capabilities appear in the graph
- Check if any downstream capability calls an upstream capability through the graph
- In P0 with max 2 nodes: check if capability B internally references capability A's graph

### 4.2 Prevention
- `no_hidden_execution` must be `true` for every edge
- No node can invoke a capability that appears in the current graph
- Capability registry lookups are validated against the active graph's node list
- If tool recursion is detected, the graph is FORBIDDEN

## 5. Hidden Agent Loop Prevention (L5)

Hidden agent loops occur when a capability internally spawns an agent that re-invokes the
same graph or any capability within it.

### 5.1 Prevention Mechanism
- All node capabilities are statically analyzed (in P0: documented, not runtime checked)
- Node contracts declare `no_hidden_execution: true`
- Any agent spawning within a capability is considered a tool recursion
- The `allowed_side_effects` field must be empty `[]`

### 5.2 P0 Simplification
P0 produces dry plans only. No capability is actually executed. Therefore:
- No agent can be spawned (no execution paths exist)
- Tool recursion is a theoretical concern only
- Loop prevention is enforced structurally by the DAG policy

## 6. Static DAG Immutability (L6)

The composition graph in P0 is a compile-time artifact:
- Graph topology is immutable after `PlanStructure` is built
- No runtime API to add/remove nodes or edges
- No runtime API to modify node contracts
- No runtime API to modify edge contracts
- No dynamic graph mutation is possible

## 7. Loop Detection Algorithm (Kahn's Algorithm)

```
function detect_cycles(graph):
  in_degree = compute_indegrees(graph)
  queue = nodes_with_indegree_zero(graph)
  visited = 0
  
  while queue not empty:
    node = queue.pop()
    visited += 1
    for each downstream of node:
      in_degree[downstream] -= 1
      if in_degree[downstream] == 0:
        queue.push(downstream)
  
  if visited != total_nodes(graph):
    return CYCLES_DETECTED
  return NO_CYCLES
```

For P0 with max 2 nodes, this is trivially fast and always succeeds for valid graphs.

## 8. Loop Prevention Invariants Summary

| Invariant | Guarantee |
|-----------|-----------|
| No self-edges | EC-03 enforcement |
| No 2-node cycles | Structurally impossible (depth ≤ 2, 1 edge max) |
| No tool recursion | Capability call graph validation |
| No agent loops | no_hidden_execution + no execution in P0 |
| No dynamic cycles | Graph is immutable post-build |
| Static DAG guarantee | Compile-time validation + no mutation API |

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|LOOP_PREVENTION|v1.0.0-draft`
