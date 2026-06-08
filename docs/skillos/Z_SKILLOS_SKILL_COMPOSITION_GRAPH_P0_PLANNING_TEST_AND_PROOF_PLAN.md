# Z-SkillOS Skill Composition Graph P0 Planning — TEST & PROOF PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Test & Proof Definition

This document defines the proof categories and test strategies for verifying the Skill Composition
Graph P0 contracts, policies, and invariants. All tests are documentation-level specifications;
no implementation exists in P0. Minimum: 18 proof categories.

## 2. Proof Categories

### Category 1: Node Contract Validation
**Proof**: Every node in a valid graph satisfies all 10 NC rules.
**Test Strategy**: Generate node contracts with intentional violations (missing fields, invalid schemas,
wrong tier) and verify rejection.
**Invariant**: NC-01 through NC-10 hold for all accepted nodes.

### Category 2: Edge Contract Validation
**Proof**: Every edge in a valid graph satisfies all 10 EC rules.
**Test Strategy**: Generate edge contracts with permission escalations, forbidden field overlaps,
self-references; verify all rejected.
**Invariant**: EC-01 through EC-10 hold for all accepted edges.

### Category 3: DAG Topology — Single Node
**Proof**: A graph with exactly 1 valid node and 0 edges is accepted.
**Test Strategy**: Build single-node graphs with valid contracts; verify acceptance and PlanStructure.
**Invariant**: DAG-01 through DAG-12 hold for single-node graphs.

### Category 4: DAG Topology — Two Nodes Sequential
**Proof**: A graph with 2 valid nodes and 1 valid edge is accepted.
**Test Strategy**: Build A→B graphs with valid contracts; verify sequential topology.
**Invariant**: Edge count = 1, depth = 2, no cycles.

### Category 5: DAG Topology — Three Nodes Rejected
**Proof**: A graph with 3 nodes is rejected.
**Test Strategy**: Attempt to build a 3-node graph; verify rejection with DEPTH_EXCEEDED.
**Invariant**: DAG-02 and DAG-03 enforcement.

### Category 6: Cycle Detection — Self-Edge
**Proof**: A node with an edge to itself is rejected.
**Test Strategy**: Build edge with upstream_node_id == downstream_node_id; verify rejection.
**Invariant**: EC-03 enforcement; no self-edges.

### Category 7: Cycle Detection — Two-Node Backedge
**Proof**: A→B with an additional B→A edge creates a cycle.
**Test Strategy**: Attempt to add reverse edge in 2-node graph; verify rejection.
**Invariant**: Kahn's algorithm detects cycle; graph is FORBIDDEN.

### Category 8: Permission Propagation — Equal Tier
**Proof**: Two nodes at same tier (1→1 or 0→0) are accepted.
**Test Strategy**: Build graphs with equal-tier nodes; verify acceptance.
**Invariant**: downstream_tier ≤ upstream_tier holds.

### Category 9: Permission Propagation — De-escalation
**Proof**: Upstream tier 1, downstream tier 0 is accepted.
**Test Strategy**: Build 1→0 graphs; verify acceptance and edge propagation_valid.
**Invariant**: De-escalation is valid propagation.

### Category 10: Permission Propagation — Escalation Rejected
**Proof**: Upstream tier 0, downstream tier 1 is rejected.
**Test Strategy**: Build 0→1 graphs; verify rejection with FORBIDDEN.
**Invariant**: Permission escalation is never allowed.

### Category 11: Permission Propagation — Write Tier Blocked
**Proof**: Any node at tier 4 or 5 is rejected in P0.
**Test Strategy**: Build graphs with EXECUTION or PRODUCTION tier nodes; verify rejection.
**Invariant**: P0 max tier = 1.

### Category 12: Evidence Propagation — Node Hash Determinism
**Proof**: Same node input always produces same node_evidence_hash.
**Test Strategy**: Hash same node twice; verify identical hashes.
**Invariant**: Hash function is deterministic.

### Category 13: Evidence Propagation — Edge Hash Chain
**Proof**: Edge hash includes upstream node hash.
**Test Strategy**: Change upstream output; verify edge hash changes.
**Invariant**: Edge hash is cryptographically linked to upstream.

### Category 14: Evidence Propagation — Graph Decision Hash
**Proof**: Graph decision hash includes all node and edge hashes.
**Test Strategy**: Change any node output; verify graph hash changes.
**Invariant**: Graph hash is a Merkle-root-like aggregate.

### Category 15: Evidence Propagation — Rollback Marker
**Proof**: Degraded node sets rollback_marker in graph hash.
**Test Strategy**: Trigger node degradation; verify rollback_marker = true.
**Invariant**: Rollback marker is included in graph decision hash.

### Category 16: Failure Degradation — NOOP
**Proof**: Node failure produces NOOP degradation at D1 level.
**Test Strategy**: Inject failure; verify D1 degradation output.
**Invariant**: Failed node returns noop marker, not exception.

### Category 17: Failure Degradation — PLAN_ONLY
**Proof**: Permission violation degrades entire graph to PLAN_ONLY.
**Test Strategy**: Trigger permission escalation; verify D2 degradation.
**Invariant**: Graph produces plan structure but no execution.

### Category 18: Failure Degradation — Partial Invalidation
**Proof**: In A→B, if A succeeds and B fails, graph is PARTIALLY_VALID.
**Test Strategy**: Make node B fail; verify A's result preserved, B degraded.
**Invariant**: Upstream results survive downstream failure.

### Category 19: Output Boundary — No Side Effects
**Proof**: Graph produces no files, no console output, no network calls.
**Test Strategy**: Audit node contracts: allowed_side_effects must be [].
**Invariant**: All P0 node contracts have empty side effects list.

### Category 20: Output Boundary — result_envelope Immutability
**Proof**: No node can modify the result_envelope fields.
**Test Strategy**: Verify envelope schema is fixed; verify no mutation paths.
**Invariant**: result_envelope structure is constant across all graph outputs.

### Category 21: Loop Prevention — Static DAG Guarantee
**Proof**: No valid P0 graph can contain a cycle.
**Test Strategy**: Exhaustive enumeration of all 1-2 node configurations; verify no cycles.
**Invariant**: Kahn's algorithm reports NO_CYCLES for all valid P0 graphs.

### Category 22: Forbidden Actions — All Coverable
**Proof**: All 18+ forbidden actions are detectable by at least one proof category.
**Test Strategy**: Map each forbidden action to a proof category.
**Invariant**: No forbidden action lacks a corresponding proof.

## 3. Test Strategy Summary

| Aspect | Approach |
|--------|----------|
| Contract tests | Generate valid/invalid contracts; verify acceptance/rejection |
| Topology tests | Enumerate all 1-2 node configurations; verify depth/node count limits |
| Permission tests | All tier permutations (0,1) × (0,1); verify monotonic rule |
| Evidence tests | Hash determinism, chain integrity, tamper detection |
| Degradation tests | Inject failures at node/edge/graph level; verify correct degradation |
| Output boundary tests | Audit side effects; verify envelope immutability |
| Loop tests | Structural proof: max 2 nodes + 1 edge = no cycles possible |

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|TEST_AND_PROOF|v1.0.0-draft`
