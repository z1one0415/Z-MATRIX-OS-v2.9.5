# Z-SkillOS Skill Composition Graph P0 Planning — DAG POLICY PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. DAG Policy Definition

The DAG Policy defines the structural constraints for the Skill Composition Graph. It governs
topology, depth, connectivity, and static validation. P0 enforces the absolute minimum: 1-2 nodes
in strictly sequential configuration with no cycles, no branching, and no dynamic mutation.

## 2. Topology Rules

### 2.1 Node Count Limits
- Minimum nodes per graph: 1 (single-node dry plan)
- Maximum nodes per graph: 2 (two-node sequential plan)
- No graph may contain zero nodes (must have at least one valid node contract)

### 2.2 Edge Count Limits
- Single-node graph: 0 edges
- Two-node graph: exactly 1 edge (from node[0] to node[1])
- No edges between non-consecutive nodes
- No parallel edges (multiple edges between same node pair)

### 2.3 Depth Limit
- Maximum graph depth (longest path): 2
- Single-node graph depth: 1
- Two-node graph depth: 2
- Depth > 2 is BLOCKED in P0

### 2.4 Topology Constraints
- Strictly sequential: nodes form a linear chain n0 → n1
- No branching: each node has at most 1 outgoing edge
- No fan-out: no node can connect to multiple downstream nodes
- No fan-in: no node can receive from multiple upstream nodes
- No merge points: graph is a simple path, not a DAG with convergence

## 3. Cycle Prevention

### 3.1 Compile-Time Cycle Detection
- Algorithm: topological sort validation with Kahn's algorithm
- Any back-edge detected during build is rejected
- Cycle detection runs before any node processing begins

### 3.2 Self-Edge Prohibition
- upstream_node_id must never equal downstream_node_id for any edge
- Enforced at edge contract validation time

### 3.3 Depth-Limited Cycle Prevention
- Since max depth is 2, the only possible cycle is A→A (self-edge) or A→B→A
- A→B→A: B would need an outgoing edge to A, but B is already depth 2, so B's edge to A would create depth 3 → rejected by depth limit
- This makes cycle prevention structurally guaranteed by depth limit

## 4. Static Invariants

| Invariant ID | Description | Enforcement |
|-------------|-------------|-------------|
| DAG-01 | Graph is a valid DAG (no cycles) | Compile-time |
| DAG-02 | Node count ≤ 2 | Compile-time |
| DAG-03 | Depth ≤ 2 | Compile-time |
| DAG-04 | All nodes have valid contracts | Compile-time |
| DAG-05 | All edges have valid contracts | Compile-time |
| DAG-06 | No parallel edges | Compile-time |
| DAG-07 | No self-edges | Compile-time |
| DAG-08 | Graph is connected (if n=2, edge exists) | Compile-time |
| DAG-09 | No isolated nodes (every node has ≥0 edges matching node count) | Compile-time |
| DAG-10 | Graph topology is immutable post-build | Runtime |
| DAG-11 | No dynamic graph mutation | Runtime |
| DAG-12 | No runtime node addition/removal | Runtime |

## 5. Graph Build Sequence

```
1. Validate node contracts (all nodes)
2. Validate edge contracts (all edges)
3. Run compile-time cycle detection
4. Verify depth ≤ 2
5. Verify node count ≤ 2
6. Run permission propagation check
7. Build evidence hash chain
8. Produce PlanStructure { nodes, edges, valid, decision_hash }
9. Return immutable graph object
```

## 6. P0 Graph State Machine

```
[EMPTY] → [NODE_1_VALID] → [GRAPH_VALID_SINGLE]
                              ↓
                         [NODE_2_VALID] → [EDGE_VALID] → [GRAPH_VALID_PAIR]
                         
Any state → [CYCLE_DETECTED] → [GRAPH_REJECTED]
Any state → [DEPTH_EXCEEDED] → [GRAPH_REJECTED]
Any state → [PERMISSION_VIOLATION] → [GRAPH_FORBIDDEN]
```

## 7. Explicit Prohibitions

The following are explicitly prohibited in P0 DAG Policy:
1. No dynamic graph construction at runtime
2. No conditional edge creation
3. No agent-in-the-loop topology decisions
4. No graph hot-reload or live mutation
5. No recursive sub-graph spawning
6. No parallel execution of multiple nodes
7. No auto-escalation of permission tiers
8. No hidden agent loops within node execution

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|DAG_POLICY|v1.0.0-draft`
