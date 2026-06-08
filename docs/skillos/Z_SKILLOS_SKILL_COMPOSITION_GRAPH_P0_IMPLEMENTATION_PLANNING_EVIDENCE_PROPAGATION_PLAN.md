# Z-SkillOS Skill Composition Graph P0 Implementation Planning — EVIDENCE PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for evidence propagation through the
composition graph. Covers SHA-256 hash chain design, deterministic serialization,
node/edge/decision hash computation, test vectors, and chain verification protocol.

## 2. Hash Chain Architecture

### 2.1 Hash Levels

```
Level 1: Node Evidence Hash
  SHA-256(capability_id + input + output + timestamp)
         |
         v
Level 2: Edge Evidence Hash
  SHA-256(upstream_node_hash + edge_id + timestamp)
         |
         v
Level 3: Graph Decision Hash
  SHA-256(all_node_hashes + all_edge_hashes + plan_id)
```

### 2.2 Hash Composition Rules

| Hash Level | Input Fields | Ordering |
|------------|-------------|----------|
| Node | capability_id, input (sorted keys), output (sorted keys), created_at | Canonical JSON sorted keys |
| Edge | upstream_node_hash, edge_id, created_at | Canonical JSON sorted keys |
| Decision | all_node_hashes (sorted by node_id), all_edge_hashes (sorted by edge_id), graph_id | Canonical JSON sorted keys |

## 3. Deterministic Serialization

### 3.1 Canonical JSON Format

```python
import json, hashlib

def canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True)

def sha256_hex(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

### 3.2 Determinism Guarantees
1. Dictionary keys always sorted alphabetically
2. No whitespace padding (compact separators)
3. ASCII encoding only
4. Fixed field ordering in compound objects
5. Timestamps normalized to UTC ISO 8601

## 4. Node Evidence Hash

```python
def compute_node_evidence_hash(capability_id: str, input_data: dict,
                               output_data: dict, created_at: str) -> str:
    payload = {"capability_id": capability_id, "input": input_data,
               "output": output_data, "timestamp": created_at}
    return sha256_hex(canonical_json(payload))
```

### Test Vectors
| Test | Expected |
|------|----------|
| Same input twice | Identical hashes |
| Different input | Different hashes |
| Different timestamp | Different hashes |
| Dict key order different | Identical (sorted keys) |

## 5. Edge Evidence Hash

```python
def compute_edge_evidence_hash(upstream_node_hash: str, edge_id: str, created_at: str) -> str:
    payload = {"upstream_node_hash": upstream_node_hash, "edge_id": edge_id, "timestamp": created_at}
    return sha256_hex(canonical_json(payload))
```

## 6. Graph Decision Hash

```python
def compute_decision_hash(node_hashes: Dict[str, str], edge_hashes: Dict[str, str],
                          graph_id: str, rollback_marker: bool = False) -> str:
    sorted_nodes = [node_hashes[nid] for nid in sorted(node_hashes.keys())]
    sorted_edges = [edge_hashes[eid] for eid in sorted(edge_hashes.keys())]
    payload = {"node_hashes": sorted_nodes, "edge_hashes": sorted_edges,
               "graph_id": graph_id, "rollback_marker": rollback_marker}
    return sha256_hex(canonical_json(payload))
```

### 6.1 Rollback Marker
When any node degrades, rollback_marker=True is set. This ensures degraded graph hashes differ
from complete graph hashes, preventing accidental acceptance of degraded plans.

## 7. Chain Verification Protocol

```python
def verify_evidence_chain(graph: CompositionGraph) -> List[HashMismatchError]:
    errors = []
    computed_node_hashes = {}
    for node in graph.nodes:
        computed_node_hashes[node.node_id] = compute_node_evidence_hash(
            node.capability_id, node.metadata.get("input", {}),
            node.metadata.get("output", {}), node.created_at
        )
    computed_edge_hashes = {}
    for edge in graph.edges:
        expected = compute_edge_evidence_hash(
            computed_node_hashes[edge.upstream_node_id], edge.edge_id, edge.created_at
        )
        computed_edge_hashes[edge.edge_id] = expected
        if not hmac.compare_digest(edge.evidence_handoff, expected):
            errors.append(HashMismatchError(f"Edge {edge.edge_id}: hash mismatch"))
    computed_decision = compute_decision_hash(
        computed_node_hashes, computed_edge_hashes, graph.graph_id, graph.rollback_marker
    )
    if not hmac.compare_digest(graph.decision_hash, computed_decision):
        errors.append(HashMismatchError("Decision hash mismatch"))
    return errors
```

### Chain Properties
| Property | Guarantee |
|----------|-----------|
| Immutability | Hashes computed once at build; never recomputed |
| Tamper Detection | Any modification changes all downstream hashes |
| Determinism | Same inputs always produce same hashes |
| Ephemeral | No persistent storage; in-memory only in P0 |
