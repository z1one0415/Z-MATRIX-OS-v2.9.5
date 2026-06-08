# Z-SkillOS Skill Composition Graph P0 Implementation Planning — EVIDENCE PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for evidence propagation through the
composition graph. It covers the SHA-256 hash chain design, deterministic serialization,
node/edge/decision hash computation, test vectors, and chain verification protocol.

## 2. Hash Chain Architecture

### 2.1 Hash Levels

```
Level 1: Node Evidence Hash
  SHA-256(capability_id + input + output + timestamp)
         ↓
Level 2: Edge Evidence Hash
  SHA-256(upstream_node_hash + edge_id + timestamp)
         ↓
Level 3: Graph Decision Hash
  SHA-256(all_node_hashes + all_edge_hashes + plan_id)
```

### 2.2 Hash Composition Rules

| Hash Level | Input Fields | Ordering |
|------------|-------------|----------|
| Node | capability_id, input (sorted keys), output (sorted keys), created_at | Canonical JSON with sorted keys |
| Edge | upstream_node_hash, edge_id, created_at | Canonical JSON with sorted keys |
| Decision | all_node_hashes (sorted by node_id), all_edge_hashes (sorted by edge_id), graph_id | Canonical JSON with sorted keys |

## 3. Deterministic Serialization

### 3.1 Canonical JSON Format

```python
import json
import hashlib

def canonical_json(data: dict) -> str:
    """Serialize dict to deterministic JSON string."""
    return json.dumps(
        data,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=True
    )

def sha256_hex(content: str) -> str:
    """Compute SHA-256 hex digest."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

### 3.2 Determinism Guarantees

1. Dictionary keys are always sorted alphabetically
2. No whitespace padding (compact separators)
3. ASCII encoding only (no Unicode escape issues)
4. Fixed field ordering in compound objects
5. Timestamps normalized to UTC ISO 8601

## 4. Node Evidence Hash

### 4.1 Computation

```python
def compute_node_evidence_hash(
    capability_id: str,
    input_data: dict,
    output_data: dict,
    created_at: str
) -> str:
    payload = {
        "capability_id": capability_id,
        "input": input_data,
        "output": output_data,
        "timestamp": created_at
    }
    return sha256_hex(canonical_json(payload))
```

### 4.2 Test Vectors

| Test | Input | Expected Hash Behavior |
|------|-------|----------------------|
| TV-N-01 | Same input twice | Identical hashes |
| TV-N-02 | Different input | Different hashes |
| TV-N-03 | Different timestamp | Different hashes |
| TV-N-04 | Dict key order different | Identical hashes (sorted keys) |
| TV-N-05 | Empty input/output | Deterministic hash of empty dicts |

## 5. Edge Evidence Hash

### 5.1 Computation

```python
def compute_edge_evidence_hash(
    upstream_node_hash: str,
    edge_id: str,
    created_at: str
) -> str:
    payload = {
        "upstream_node_hash": upstream_node_hash,
        "edge_id": edge_id,
        "timestamp": created_at
    }
    return sha256_hex(canonical_json(payload))
```

### 5.2 Test Vectors

| Test | Input | Expected Hash Behavior |
|------|-------|----------------------|
| TV-E-01 | Same upstream hash twice | Identical edge hashes |
| TV-E-02 | Different upstream hash | Different edge hashes |
| TV-E-03 | Different edge_id | Different hashes |
| TV-E-04 | Evidence handoff validation | edge.evidence_handoff == computed edge hash |

## 6. Graph Decision Hash

### 6.1 Computation

```python
def compute_decision_hash(
    node_hashes: Dict[str, str],
    edge_hashes: Dict[str, str],
    graph_id: str,
    rollback_marker: bool = False
) -> str:
    sorted_node_hashes = [node_hashes[nid] for nid in sorted(node_hashes.keys())]
    sorted_edge_hashes = [edge_hashes[eid] for eid in sorted(edge_hashes.keys())]
    payload = {
        "node_hashes": sorted_node_hashes,
        "edge_hashes": sorted_edge_hashes,
        "graph_id": graph_id,
        "rollback_marker": rollback_marker
    }
    return sha256_hex(canonical_json(payload))
```

### 6.2 Rollback Marker

When any node degrades, `rollback_marker = True` is set in the decision hash input.
This ensures the decision hash is different for degraded graphs, preventing
accidental acceptance of a degraded plan as complete.

### 6.3 Test Vectors

| Test | Input | Expected Hash Behavior |
|------|-------|----------------------|
| TV-D-01 | Same graph twice | Identical decision hash |
| TV-D-02 | Different plan_id | Different decision hash |
| TV-D-03 | rollback_marker=True | Different hash vs False |
| TV-D-04 | Node hash order different | Identical (sorted by node_id) |
| TV-D-05 | Degraded graph | Different hash; rollback_marker embedded |

## 7. Chain Verification Protocol

### 7.1 Full Chain Verification

```python
def verify_evidence_chain(graph: CompositionGraph) -> List[HashMismatchError]:
    errors = []

    # Verify all node hashes
    computed_node_hashes = {}
    for node in graph.nodes:
        computed = compute_node_evidence_hash(
            node.capability_id, node.metadata.get("input", {}),
            node.metadata.get("output", {}), node.created_at
        )
        computed_node_hashes[node.node_id] = computed

    # Verify all edge hashes reference correct upstream nodes
    computed_edge_hashes = {}
    for edge in graph.edges:
        expected = compute_edge_evidence_hash(
            computed_node_hashes[edge.upstream_node_id],
            edge.edge_id, edge.created_at
        )
        computed_edge_hashes[edge.edge_id] = expected
        if not hmac.compare_digest(edge.evidence_handoff, expected):
            errors.append(HashMismatchError(
                f"Edge {edge.edge_id}: handoff hash mismatch"
            ))

    # Verify decision hash
    computed_decision = compute_decision_hash(
        computed_node_hashes, computed_edge_hashes,
        graph.graph_id, graph.rollback_marker
    )
    if not hmac.compare_digest(graph.decision_hash, computed_decision):
        errors.append(HashMismatchError("Decision hash mismatch"))

    return errors
```

### 7.2 Evidence Chain Properties

| Property | Guarantee |
|----------|-----------|
| Immutability | Hashes are computed once at build time; never recomputed |
| Tamper Detection | Any modification to node/edge/graph changes all downstream hashes |
| Determinism | Same inputs always produce same hashes |
| Ephemeral | No persistent storage; in-memory only in P0 |
