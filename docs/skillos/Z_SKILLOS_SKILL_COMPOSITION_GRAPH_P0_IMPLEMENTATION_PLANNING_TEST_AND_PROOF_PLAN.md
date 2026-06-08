# Z-SkillOS Skill Composition Graph P0 Implementation Planning — TEST & PROOF PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the proof categories, test strategies, invariant coverage, and test vectors
for verifying the Skill Composition Graph P0 implementation. Minimum: 18 proof categories.

## 2. Proof Categories (>=18)

### Category 1: Node Contract Validation (NC-01 to NC-10)
**Proof**: Every valid node satisfies all 10 NC rules.
**Strategy**: Generate node contracts with intentional violations for each NC rule; verify rejection.

### Category 2: Edge Contract Validation (EC-01 to EC-10)
**Proof**: Every valid edge satisfies all 10 EC rules.
**Strategy**: Generate edges with self-references, escalations, field overlaps; verify all rejected.

### Category 3: DAG Topology — Single Node Accepted
**Proof**: Graph with 1 valid node, 0 edges is accepted.
**Strategy**: Build single-node graph; verify depth=1, node_count=1, no cycles.

### Category 4: DAG Topology — Two Nodes Sequential Accepted
**Proof**: Graph with 2 valid nodes, 1 valid edge A->B is accepted.
**Strategy**: Build A->B graph; verify edge_count=1, depth=2, no cycles.

### Category 5: DAG Topology — Three Nodes Rejected
**Proof**: Graph with 3 nodes is rejected.
**Strategy**: Attempt 3-node graph; verify DAG-02 enforcement.

### Category 6: DAG Topology — Depth 3 Rejected
**Proof**: Graph with depth > 2 is rejected.
**Strategy**: Verify any graph exceeding depth 2 is caught.

### Category 7: Self-Edge Rejection
**Proof**: Node with edge to itself is rejected.
**Strategy**: Build edge with upstream==downstream; verify EC-03 enforcement.

### Category 8: Two-Node Backedge Cycle Detection
**Proof**: Adding B->A to existing A->B creates a cycle.
**Strategy**: Add reverse edge; run Kahn's; verify cycle detection.

### Category 9: Permission Propagation — Equal Tier
**Proof**: Two nodes at same tier (0->0 or 1->1) accepted.
**Strategy**: Build equal-tier graphs; verify acceptance.

### Category 10: Permission Propagation — De-escalation
**Proof**: Upstream tier 1, downstream tier 0 accepted.
**Strategy**: Build 1->0 graphs; verify acceptance.

### Category 11: Permission Escalation Rejected
**Proof**: Upstream tier 0, downstream tier 1 rejected.
**Strategy**: Build 0->1 graph; verify FORBIDDEN with escalation error.

### Category 12: Write Tier Blocked
**Proof**: Any node at tier 4 or 5 rejected in P0.
**Strategy**: Build graphs with EXECUTION/PRODUCTION nodes; verify NC-04.

### Category 13: Evidence Hash — Node Determinism
**Proof**: Same node input always produces same node_evidence_hash.
**Strategy**: Hash same node twice; verify identical.

### Category 14: Evidence Hash — Edge Chain Dependency
**Proof**: Edge hash changes when upstream node hash changes.
**Strategy**: Change upstream output; verify edge hash changes.

### Category 15: Evidence Hash — Graph Decision
**Proof**: Graph decision hash changes when any node/edge changes.
**Strategy**: Modify one field; verify decision hash differs.

### Category 16: Evidence Hash — Rollback Marker
**Proof**: Decision hash differs when rollback_marker is set.
**Strategy**: Compute with and without rollback; verify difference.

### Category 17: Degradation — Node Failure to PLAN_ONLY
**Proof**: Node fails validation but structure valid -> PLAN_ONLY.
**Strategy**: Build valid 1-node graph; inject NC-05 violation; verify PLAN_ONLY.

### Category 18: Degradation — Cycle to NOOP
**Proof**: Cycle detected -> NOOP.
**Strategy**: Build A->B, B->A; verify NOOP with rollback marker.

### Category 19: Field Governance — Allow-List Filtering
**Proof**: Only allowed_data_fields pass through edge handoff.
**Strategy**: Upstream {"a":1,"b":2,"c":3}; allow=["a","c"]; verify {"a":1,"c":3}.

### Category 20: Field Governance — Forbidden Field Blocking
**Proof**: forbidden_data_fields blocked even if in allowed.
**Strategy**: Test EC-05 intersection detection; verify edge rejected.

## 3. Test Vectors

```python
# TV-HASH-01: Node hash determinism
def test_node_hash_determinism():
    n1 = CompositionNode(capability_id="read_stock", ...)
    n2 = CompositionNode(capability_id="read_stock", ...)  # identical
    assert n1.compute_evidence_hash({}, {}) == n2.compute_evidence_hash({}, {})

# TV-HASH-02: Node hash input sensitivity
def test_node_hash_input_sensitivity():
    node = CompositionNode(...)
    assert node.compute_evidence_hash({"s":"AAPL"},{}) != node.compute_evidence_hash({"s":"GOOGL"},{})

# TV-PERM-01: Equal tier accepted
def test_equal_tier():
    assert check_monotonic(0, 0) and check_monotonic(1, 1)

# TV-PERM-02: Escalation rejected
def test_escalation():
    assert not check_monotonic(0, 1)
    assert not check_monotonic(0, 4)

# TV-DAG-01: Single node valid
def test_single_node():
    g = CompositionGraph(); g.add_node(valid_node())
    assert len(g.validate()) == 0

# TV-DAG-02: Two-node valid
def test_two_node():
    g = CompositionGraph()
    g.add_node(n_a); g.add_node(n_b); g.add_edge(e_ab)
    assert len(g.validate()) == 0
```

## 4. Forbidden Actions Coverage (>=18)

| # | Forbidden Action | Proof Category |
|---|------------------|:---:|
| 1 | Real capability execution | All (P0 plan-only) |
| 2 | Hidden tool calls | Cat 1 (NC-02 adapter) |
| 3 | Dynamic graph modification | Cat 1 (NC-10 immutability) |
| 4 | Recursive composition | Cat 8 (cycle detection) |
| 5 | Auto-permission escalation | Cat 11 (escalation) |
| 6 | Result envelope mutation | Cat 1 (NC-10) + OB rules |
| 7 | Fail-closed behavior | Cat 17-18 (degradation) |
| 8 | Z-MATRIX integration | All (standalone) |
| 9 | Persistent evidence storage | All (ephemeral only) |
| 10 | Network calls | Cat 1 (adapter validation) |
| 11 | File system writes | Cat 1 (capability validation) |
| 12 | Database queries | Cat 1 (adapter validation) |
| 13 | Sub-agent spawning | Cat 1 (capability registry) |
| 14 | Unregistered capability paths | Cat 1 (NC-02, NC-03) |
| 15 | Write-tier node execution | Cat 12 (tier blocking) |
| 16 | Dynamic depth interpretation | Cat 6 (compile-time depth) |
| 17 | Conditional topology | Cat 3-4 (static topology) |
| 18 | Evidence hash mutation | Cat 13 (hash determinism) |
| 19 | Non-deterministic serialization | Cat 13 (canonical JSON) |
| 20 | Circular dependency | Cat 8 (Kahn's algorithm) |

## 5. Edge Case Coverage

| Edge Case | Category |
|-----------|:---:|
| Empty input_schema | Cat 1 |
| Empty output_schema | Cat 1 |
| Duplicate node_id | Cat 1 |
| Duplicate edge_id | Cat 2 |
| Orphan edge (missing node) | Cat 2 |
| Zero-node graph | Edge case |
| Future/past timestamp | Cat 1 |
| Invalid UUID format | Cat 1 |
| Degradation result is {} | Cat 1 |

## 6. Test Execution Plan (P1+)

| Phase | Tests | Coverage Target |
|-------|-------|:---:|
| P1.1 | Node model unit tests | 100% line + branch |
| P1.2 | Edge model unit tests | 100% line + branch |
| P1.3 | DAG validator unit tests | 100% line + branch |
| P1.4 | Permission validator unit tests | 100% line + branch |
| P1.5 | Evidence validator unit tests | 100% line + branch |
| P1.6 | Policy integration tests | All policy rules |
| P1.7 | Degradation scenario tests | All degradation paths |
| P1.8 | E2E graph build tests | Full pipeline |

## 7. Proof Completeness Matrix

| Layer | Proof Cats | NC/EC Rules | DAG Rules | Policy Rules |
|-------|:---:|:---:|:---:|:---:|
| Node Model | 1, 9-13, 17 | NC-01..NC-10 | — | PP-01,PP-06 |
| Edge Model | 2, 7, 19-20 | EC-01..EC-10 | — | PP-02,OB-03 |
| DAG Validator | 3-6, 8, 18 | — | DAG-01..DAG-12 | LP-01..LP-08 |
| Permission | 9-12 | — | — | PP-01..PP-06 |
| Evidence | 13-16 | — | — | All hash rules |
| Degradation | 17-18 | — | — | All degradation |
| Output Boundary | 19-20 | — | — | OB-01..OB-07 |
