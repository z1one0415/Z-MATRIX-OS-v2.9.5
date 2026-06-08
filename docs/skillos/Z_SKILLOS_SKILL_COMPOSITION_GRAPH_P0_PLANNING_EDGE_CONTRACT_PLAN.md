# Z-SkillOS Skill Composition Graph P0 Planning — EDGE CONTRACT PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Edge Contract Definition

An Edge Contract governs the data flow between two composition graph nodes. Every edge must
be explicitly declared with allowed data fields, forbidden data fields, evidence handoff rules,
and permission propagation constraints. No hidden data flow is permitted.

## 2. Contract Fields

### 2.1 `upstream_node_id` (string, required)
The source node identifier. Must reference a valid node contract in the same graph.

### 2.2 `downstream_node_id` (string, required)
The target node identifier. Must reference a valid node contract in the same graph.
Must not be equal to upstream_node_id (no self-edge).

### 2.3 `allowed_data_fields` (array of strings, required)
Explicit allow-list of data fields permitted to flow from upstream to downstream.
Any field not in this list is blocked. P0 minimum: at least one field must be listed.

### 2.4 `forbidden_data_fields` (array of strings, required)
Explicit deny-list of data fields that are explicitly blocked even if matched by
broader patterns. Takes precedence over allowed_data_fields.

### 2.5 `evidence_handoff` (object, required)
Cryptographic evidence for the data handoff from upstream to downstream:
- `upstream_output_hash`: SHA-256 of upstream node's output
- `edge_id`: unique edge identifier
- `handoff_timestamp`: ISO 8601 timestamp
- `edge_evidence_hash`: SHA-256 of (upstream_output_hash + edge_id + handoff_timestamp)

### 2.6 `permission_propagation` (object, required)
Permission tier propagation rules:
- `upstream_tier`: integer (from upstream node contract)
- `downstream_tier`: integer (from downstream node contract)
- `propagation_valid`: boolean (true if downstream_tier ≤ upstream_tier)
- `violation_action`: "FORBIDDEN" if propagation_valid is false

### 2.7 `no_hidden_execution` (boolean, required)
Must be `true` in P0. Assertion that no hidden execution paths exist along this edge.
No implicit tool calls. No agent spawning. No side-channel communication.

## 3. Edge Contract Validation Rules

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| EC-01 | upstream_node_id must exist in graph | Compile-time |
| EC-02 | downstream_node_id must exist in graph | Compile-time |
| EC-03 | No self-edge (upstream ≠ downstream) | Compile-time |
| EC-04 | allowed_data_fields must be non-empty | Compile-time |
| EC-05 | All allowed_data_fields must exist in upstream output_schema | Compile-time |
| EC-06 | forbidden_data_fields must not overlap with allowed_data_fields | Compile-time |
| EC-07 | evidence_handoff must contain valid hash structure | Compile-time |
| EC-08 | downstream_tier ≤ upstream_tier (monotonic) | Compile-time |
| EC-09 | If permission violated, edge is FORBIDDEN | Compile-time |
| EC-10 | no_hidden_execution must be true | Compile-time |

## 4. Edge Contract Example (P0 Two-Node Sequential Plan)

```json
{
  "edge_id": "e001",
  "upstream_node_id": "n001",
  "downstream_node_id": "n002",
  "allowed_data_fields": ["sentiment_scores", "analyzed_symbols"],
  "forbidden_data_fields": ["raw_api_responses", "internal_auth_tokens"],
  "evidence_handoff": {
    "upstream_output_hash": "sha256:abc123...",
    "edge_id": "e001",
    "handoff_timestamp": "2026-06-08T16:00:00Z",
    "edge_evidence_hash": "sha256:def456..."
  },
  "permission_propagation": {
    "upstream_tier": 1,
    "downstream_tier": 1,
    "propagation_valid": true,
    "violation_action": null
  },
  "no_hidden_execution": true
}
```

## 5. Edge Degradation Protocol

When an edge fails validation:
1. Edge is marked as FORBIDDEN
2. Downstream node is set to degraded (noop)
3. Graph decision hash includes the FORBIDDEN marker
4. Graph degrades to plan-only (no execution attempted)
5. No data flows across a FORBIDDEN edge
6. Partial results from upstream remain valid but graph is invalid

## 6. Edge Permission Violation Example

```json
{
  "permission_propagation": {
    "upstream_tier": 0,
    "downstream_tier": 1,
    "propagation_valid": false,
    "violation_action": "FORBIDDEN",
    "violation_reason": "Downstream tier 1 exceeds upstream tier 0. Planning tier cannot follow readonly tier without explicit escalation approval."
  }
}
```

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|EDGE_CONTRACT|v1.0.0-draft`
