# Z-SkillOS Skill Composition Graph P0 Implementation Planning — TEST & PROOF PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the proof categories, test strategies, invariant coverage, and test vectors
for verifying the Skill Composition Graph P0 implementation. All tests are documentation-level
specifications. Minimum: 18 proof categories.

## 2. Proof Categories (≥18)

### Category 1: Node Contract Validation (NC-01 to NC-10)
**Proof**: Every valid node satisfies all 10 NC rules.
**Test Strategy**: Generate node contracts with intentional violations for each NC rule; verify
rejection with correct error code.
**Invariants**: NC-01 (UUID4), NC-02 (capability_id pattern), NC-03 (adapter path), NC-04 (tier 0-1),
NC-05 (input JSON Schema), NC-06 (output JSON Schema), NC-07 (degradation_result non-null),
NC-08 (ISO 8601), NC-09 (semver), NC-10 (immutability post-build).

### Category 2: Edge Contract Validation (EC-01 to EC-10)
**Proof**: Every valid edge satisfies all 10 EC rules.
**Test Strategy**: Generate edge contracts with self-references, permission escalations, forbidden
field overlaps; verify all rejected.
**Invariants**: EC-01 through EC-10 hold for all accepted edges.

### Category 3: DAG Topology — Single Node Accepted
**Proof**: A graph with exactly 1 valid node and 0 edges is accepted.
**Test Strategy**: Build single-node graph; verify acceptance, depth=1, node_count=1, no cycles.
**Invariant**: DAG-01 through DAG-12 hold for single-node graphs.

### Category 4: DAG Topology — Two Nodes Sequential Accepted
**Proof**: A graph with 2 valid nodes and 1 valid edge A→B is accepted.
**Test Strategy**: Build A→B graph with valid contracts; verify sequential topology.
**Invariant**: Edge count=1, depth=2, node_count=2, no cycles.

### Category 5: DAG Topology — Three Nodes Rejected
**Proof**: A graph with 3 nodes is rejected.
**Test Strategy**: Attempt to build a 3-node graph; verify rejection with node count error.
**Invariant**: DAG-02 enforcement.

### Category 6: DAG Topology — Depth 3 Rejected
**Proof**: A graph with depth > 2 is rejected (requires >2 nodes, which is also rejected).
**Test Strategy**: Verify that any graph exceeding depth 2 is caught.
**Invariant**: DAG-03 enforcement.

### Category 7: Self-Edge Rejection
**Proof**: A node with an edge to itself is rejected.
**Test Strategy**: Build edge with upstream_node_id == downstream_node_id; verify rejection.
**Invariant**: EC-03 enforcement; no self-edges.

### Category 8: Two-Node Backedge Cycle Detection
**Proof**: Adding B→A edge to existing A→B graph creates a cycle.
**Test Strategy**: Add reverse edge; run Kahn's algorithm; verify cycle detection.
**Invariant**: DAG-05; Kahn's algorithm correctly identifies all cycles.

### Category 9: Permission Propagation — Equal Tier
**Proof**: Two nodes at same tier (0→0 or 1→1) are accepted.
**Test Strategy**: Build graphs with equal-tier nodes; verify acceptance.
**Invariant**: downstream_tier ≤ upstream_tier holds.

### Category 10: Permission Propagation — De-escalation
**Proof**: Upstream tier 1, downstream tier 0 is accepted.
**Test Strategy**: Build 1→0 graphs; verify acceptance.
**Invariant**: De-escalation is valid propagation.

### Category 11: Permission Escalation Rejected
**Proof**: Upstream tier 0, downstream tier 1 is rejected.
**Test Strategy**: Build 0→1 graph; verify FORBIDDEN with escalation error.
**Invariant**: Permission escalation never allowed.

### Category 12: Write Tier Blocked
**Proof**: Any node at tier 4 or 5 is rejected in P0.
**Test Strategy**: Build graphs with EXECUTION or PRODUCTION tier nodes; verify rejection.
**Invariant**: P0 max tier = 1 (NC-04).

### Category 13: Evidence Hash — Node Determinism
**Proof**: Same node input always produces same node_evidence_hash.
**Test Strategy**: Hash same node twice; verify identical hashes.
**Invariant**: Hash function is deterministic; canonical JSON guarantees.

### Category 14: Evidence Hash — Edge Chain Dependency
**Proof**: Edge hash changes when upstream node hash changes.
**Test Strategy**: Change upstream output; verify edge hash changes.
**Invariant**: Edge hash includes upstream node hash.

### Category 15: Evidence Hash — Graph Decision
**Proof**: Graph decision hash changes when any node/edge changes.
**Test Strategy**: Modify one field; verify decision hash differs.
**Invariant**: Decision hash includes all node and edge hashes.

### Category 16: Evidence Hash — Rollback Marker
**Proof**: Decision hash differs when rollback_marker is set.
**Test Strategy**: Compute decision hash with and without rollback; verify difference.
**Invariant**: Rollback marker affects decision hash.

### Category 17: Degradation — Node Failure to PLAN_ONLY
**Proof**: When a node fails validation but graph structure is valid, state → PLAN_ONLY.
**Test Strategy**: Build valid 1-node graph; inject NC-05 violation; verify PLAN_ONLY.
**Invariant**: Degradation produces a result; never fail-closed.

### Category 18: Degradation — Cycle to NOOP
**Proof**: When a cycle is detected, graph → NOOP.
**Test Strategy**: Build A→B, B→A; verify NOOP with rollback marker.
**Invariant**: Structural invalid degrades to NOOP.

### Category 19: Field Governance — Allow-List Filtering
**Proof**: Only allowed_data_fields pass through edge handoff.
**Test Strategy**: Upstream outputs {"a":1,"b":2,"c":3}; allow=["a","c"]; verify {"a":1,"c":3}.
**Invariant**: Edge filtering drops unlisted fields.

### Category 20: Field Governance — Forbidden Field Blocking
**Proof**: forbidden_data_fields are blocked even if in allowed_data_fields.
**Test Strategy**: Test EC-05 intersection detection; verify edge rejected.
**Invariant**: Forbidden fields never pass.

## 3. Test Vector Suite

### 3.1 Hash Test Vectors

```python
# TV-HASH-01: Node hash determinism
def test_node_hash_determinism():
    node1 = CompositionNode(capability_id="read_stock_price", ...)
    node2 = CompositionNode(capability_id="read_stock_price", ...)  # identical
    assert node1.compute_evidence_hash({}, {}) == node2.compute_evidence_hash({}, {})

# TV-HASH-02: Node hash changes with different input
def test_node_hash_input_sensitivity():
    node = CompositionNode(capability_id="read_stock_price", ...)
    h1 = node.compute_evidence_hash({"symbol": "AAPL"}, {})
    h2 = node.compute_evidence_hash({"symbol": "GOOGL"}, {})
    assert h1 != h2

# TV-HASH-03: Edge hash chain
def test_edge_hash_includes_upstream():
    n_hash = "abc123..."
    edge = CompositionEdge(upstream_node_id="n1", downstream_node_id="n2", ...)
    h1 = edge.compute_evidence_handoff(n_hash)
    h2 = edge.compute_evidence_handoff("def456...")
    assert h1 != h2
```

### 3.2 Permission Test Vectors

```python
# TV-PERM-01: Equal tier accepted
def test_equal_tier_accepted():
    assert check_monotonic(0, 0) == True
    assert check_monotonic(1, 1) == True

# TV-PERM-02: Escalation rejected
def test_escalation_rejected():
    assert check_monotonic(0, 1) == False
    assert check_monotonic(0, 4) == False
```

### 3.3 DAG Test Vectors

```python
# TV-DAG-01: Single node valid
def test_single_node_valid():
    g = CompositionGraph()
    g.add_node(valid_node())
    errors = g.validate()
    assert len(errors) == 0

# TV-DAG-02: Two-node sequential valid
def test_two_node_valid():
    g = CompositionGraph()
    g.add_node(node_a); g.add_node(node_b)
    g.add_edge(edge_ab)
    errors = g.validate()
    assert len(errors) == 0
```

## 4. Forbidden Actions Coverage (≥18)

Every forbidden action has a corresponding proof category that verifies it cannot happen:

| # | Forbidden Action | Proof Category |
|---|------------------|:---:|
| 1 | Real capability execution | All (P0 is plan-only) |
| 2 | Hidden tool calls | Category 1 (NC-02 adapter validation) |
| 3 | Dynamic graph modification | Category 1 (NC-10 immutability) |
| 4 | Recursive composition | Category 8 (cycle detection) |
| 5 | Auto-permission escalation | Category 11 (escalation rejection) |
| 6 | Result envelope mutation | Category 1 (NC-10) + OB rules |
| 7 | Fail-closed behavior | Category 17-18 (degradation) |
| 8 | Z-MATRIX integration | All (standalone SkillOS) |
| 9 | Persistent evidence storage | All (ephemeral only) |
| 10 | Network calls | Category 1 (adapter validation) |
| 11 | File system writes | Category 1 (capability validation) |
| 12 | Database queries | Category 1 (adapter validation) |
| 13 | Sub-agent spawning | Category 1 (capability registry) |
| 14 | Unregistered capability paths | Category 1 (NC-02, NC-03) |
| 15 | Write-tier node execution | Category 12 (tier blocking) |
| 16 | Dynamic depth interpretation | Category 6 (compile-time depth) |
| 17 | Conditional topology | Category 3-4 (static topology) |
| 18 | Evidence hash mutation | Category 13 (hash determinism) |
| 19 | Non-deterministic serialization | Category 13 (canonical JSON) |
| 20 | Circular dependency | Category 8 (Kahn's algorithm) |

## 5. Edge Case Coverage

| Edge Case | Category |
|-----------|:---:|
| Empty input_schema | Category 1 |
| Empty output_schema | Category 1 |
| Duplicate node_id | Category 1 |
| Duplicate edge_id | Category 2 |
| Orphan edge (missing node) | Category 2 |
| Zero-node graph | Edge case |
| Graph with nodes but no edges | Category 3 |
| Future timestamp | Category 1 |
| Past timestamp | Category 1 |
| Invalid UUID format | Category 1 |
| Invalid JSON Schema | Category 1 |
| Degradation result is {} | Category 1 |
| Very large output (>1MB) | Category 16 |

## 6. Test Execution Plan (P1+)

| Phase | Tests | Target Coverage |
|-------|-------|:---:|
| P1.1 | Node model unit tests | 100% line, 100% branch |
| P1.2 | Edge model unit tests | 100% line, 100% branch |
| P1.3 | DAG validator unit tests | 100% line, 100% branch |
| P1.4 | Permission validator unit tests | 100% line, 100% branch |
| P1.5 | Evidence validator unit tests | 100% line, 100% branch |
| P1.6 | Policy integration tests | All policy rules |
| P1.7 | Degradation scenario tests | All degradation paths |
| P1.8 | End-to-end graph build tests | Full pipeline |

## 7. Proof Completeness Matrix

| Layer | Proof Categories | NC/EC Rules | DAG Rules | Policy Rules |
|-------|:---:|:---:|:---:|:---:|
| Node Model | Cat 1, 9-13, 17 | NC-01..NC-10 | — | PP-01,PP-06 |
| Edge Model | Cat 2, 7, 19-20 | EC-01..EC-10 | — | PP-02,OB-03 |
| DAG Validator | Cat 3-6, 8, 18 | — | DAG-01..DAG-12 | LP-01..LP-08 |
| Permission | Cat 9-12 | — | — | PP-01..PP-06 |
| Evidence | Cat 13-16 | — | — | All hash rules |
| Degradation | Cat 17-18 | — | — | All degradation rules |
| Output Boundary | Cat 19-20 | — | — | OB-01..OB-07 |
