# Z-SkillOS Skill Composition Graph P0 Planning — EVIDENCE PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Evidence Propagation Definition

Evidence Propagation is the mechanism by which cryptographic proof of correctness, data integrity,
and decision traceability flows through the composition graph. Every node output, every edge handoff,
and every graph decision is hash-chained. This allows post-hoc audit without persistent storage.

## 2. Hash Chain Architecture

The evidence chain has three levels:

```
Level 1 — Node Evidence:  SHA-256(node output)
Level 2 — Edge Evidence:   SHA-256(node A hash + edge id + timestamp)
Level 3 — Graph Evidence:  SHA-256(all node hashes + all edge hashes + plan id)
```

## 3. Level 1: Node Evidence Hash

### 3.1 Hash Input
```
node_evidence_hash = SHA-256(
  capability_id ||
  node_id ||
  serialized_input ||
  serialized_output ||
  iso8601_timestamp
)
```

### 3.2 Properties
- Deterministic: same inputs always produce same hash
- Immutable: once computed, hash is read-only
- Verifiable: any party can recompute to verify integrity
- Ephemeral: P0 does not persist hashes; in-memory only

### 3.3 Inclusion in Node Output
Every node output envelope must include:
```json
{
  "result": { ... },
  "evidence": {
    "node_evidence_hash": "sha256:abc123...",
    "node_id": "n001",
    "capability_id": "research.financial.news_sentiment@v1.0.0",
    "timestamp": "2026-06-08T16:00:00Z"
  }
}
```

## 4. Level 2: Edge Evidence Hash

### 4.1 Hash Input
```
edge_evidence_hash = SHA-256(
  upstream_node_evidence_hash ||
  edge_id ||
  downstream_node_id ||
  iso8601_handoff_timestamp
)
```

### 4.2 Properties
- Links upstream and downstream evidence
- Records the exact data that crossed the edge
- Timestamp captures the handoff moment
- Edge hash is included in downstream node's input evidence

## 5. Level 3: Graph Decision Hash

### 5.1 Hash Input
```
graph_decision_hash = SHA-256(
  plan_id ||
  sorted_concat(all_node_evidence_hashes) ||
  sorted_concat(all_edge_evidence_hashes) ||
  graph_valid_flag ||
  rollback_marker ||
  iso8601_build_timestamp
)
```

### 5.2 Graph Decision Hash Fields
| Field | Type | Description |
|-------|------|-------------|
| plan_id | string | Unique identifier for this plan |
| node_hashes | string[] | Sorted array of all node evidence hashes |
| edge_hashes | string[] | Sorted array of all edge evidence hashes |
| graph_valid | boolean | Whether the graph passed validation |
| rollback_marker | boolean\|null | Set to true if any node degraded |
| build_timestamp | string | ISO 8601 build time |

## 6. Rollback Marker

The rollback marker is a special field in the graph decision hash:
- Default: `null` (no rollback)
- If any node degrades: set to `true`
- If graph is FORBIDDEN: set to `true`
- Once set, the entire plan is considered invalid
- The marker is included in the decision hash, making tampering detectable

## 7. No Persistence Constraint

P0 evidence hashes exist only in memory for the duration of the plan build. Specifically:
- No file-based evidence storage
- No database evidence storage
- No audit log file writes
- No evidence export to disk
- No network transmission of evidence
- Evidence is discarded when the plan object is garbage-collected

This is intentional: P0 is docs-only and produces no persistent artifacts. Future phases (P3+)
will introduce evidence persistence for audit trails.

## 8. Evidence Chain Verification (Future)

While P0 produces no persistent evidence, the architecture MUST support:
1. Re-computation of any hash from original inputs
2. Detection of tampering via hash mismatch
3. Chain-of-custody traceability from node → edge → graph
4. Independent verification without access to the graph runtime

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|EVIDENCE_PROPAGATION|v1.0.0-draft`
