# Z-SkillOS Skill Composition Graph P0 Implementation Planning — EDGE MODEL PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the complete implementation specification for the CompositionEdge data model.
It covers the data class structure, field governance (allow-list/deny-list), permission propagation
checks, evidence handoff protocol, and validation rules.

## 2. Data Model: CompositionEdge

### 2.1 Field Definition

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | edge_id | str (UUID4) | Yes | Globally unique edge identifier |
| 2 | upstream_node_id | str (UUID4) | Yes | Source node identifier |
| 3 | downstream_node_id | str (UUID4) | Yes | Target node identifier |
| 4 | allowed_data_fields | list[str] | Yes | Explicit allow-list of data fields |
| 5 | forbidden_data_fields | list[str] | Yes | Explicit deny-list of data fields |
| 6 | evidence_handoff | str (SHA-256) | Yes | Hash of upstream output received by downstream |
| 7 | permission_propagation | dict | Yes | Propagation metadata (upstream_tier, downstream_tier, is_valid) |
| 8 | created_at | str (ISO 8601) | Yes | Edge creation timestamp |
| 9 | version | str | Yes | Semantic version of edge contract |
| 10 | metadata | dict | No | Optional key-value metadata |

### 2.2 Edge Contract Rules (EC-01 through EC-10)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| EC-01 | edge_id must be a valid UUID4 string | Build-time validation |
| EC-02 | upstream_node_id and downstream_node_id must reference existing nodes in graph | Build-time validation |
| EC-03 | upstream_node_id != downstream_node_id (no self-edges) | Build-time rejection |
| EC-04 | allowed_data_fields must not be empty in P0 | Build-time validation |
| EC-05 | forbidden_data_fields and allowed_data_fields must not intersect | Build-time rejection |
| EC-06 | evidence_handoff must be a valid SHA-256 hex string (64 chars) | Build-time validation |
| EC-07 | permission_propagation.is_valid must be True for edge to be accepted | Build-time rejection |
| EC-08 | downstream_node permission_tier ≤ upstream_node permission_tier | Build-time enforcement |
| EC-09 | created_at must be ISO 8601 format | Build-time validation |
| EC-10 | Edge is immutable after graph build() is called | Runtime enforcement |

## 3. Field Governance Model

### 3.1 Allow-List Semantics

The `allowed_data_fields` list defines which upstream output fields the downstream node may receive.
Only fields explicitly listed are permitted to flow through the edge. Any upstream output field not
in the allow-list is silently dropped.

### 3.2 Deny-List Semantics

The `forbidden_data_fields` list defines fields that must never flow through the edge, even if
they appear in the allow-list. If a field appears in both lists, EC-05 triggers and the edge is
rejected. This prevents accidental data leakage.

### 3.3 Intersection Logic

```python
def validate_field_governance(self) -> List[EdgeValidationError]:
    errors = []
    intersection = set(self.allowed_data_fields) & set(self.forbidden_data_fields)
    if intersection:
        errors.append(EdgeValidationError(
            "EC-05", f"Field intersection detected: {intersection}"
        ))
    return errors
```

### 3.4 Handoff Filtering

```python
def filter_handoff_data(self, upstream_output: dict) -> dict:
    handoff = {}
    for field in self.allowed_data_fields:
        if field in upstream_output and field not in self.forbidden_data_fields:
            handoff[field] = upstream_output[field]
    return handoff
```

## 4. Permission Propagation Check

```python
def check_permission_propagation(self, upstream_tier: int, downstream_tier: int) -> dict:
    is_valid = downstream_tier <= upstream_tier
    return {
        "upstream_tier": upstream_tier,
        "downstream_tier": downstream_tier,
        "is_valid": is_valid,
        "reason": None if is_valid else (
            f"Permission escalation: {upstream_tier} → {downstream_tier}"
        )
    }
```

## 5. Evidence Handoff Protocol

### 5.1 Handoff Hash Computation

```python
def compute_evidence_handoff(self, upstream_node_hash: str) -> str:
    canonical = json.dumps(
        {"upstream_node_hash": upstream_node_hash,
         "edge_id": self.edge_id,
         "timestamp": self.created_at},
        sort_keys=True, separators=(',', ':')
    )
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
```

### 5.2 Handoff Verification

```python
def verify_evidence_handoff(self, expected_hash: str) -> bool:
    return hmac.compare_digest(self.evidence_handoff, expected_hash)
```

## 6. Edge Lifecycle

```
[Create] → [Validate (EC-01..EC-10)] → [Add to Graph] → [Graph.build()] → [Frozen]
                                                                              │
                                                                              ├─ success → [COMPLETE]
                                                                              └─ failure → [DEGRADE with edge_marker]
```

## 7. Edge Cases

| Case | Behavior |
|------|----------|
| Self-edge (A→A) | Rejected at EC-03 |
| Non-existent node reference | Rejected at EC-02 |
| Empty allowed_data_fields | Accepted (no data flows) |
| Forbidden field in handoff data | Filtered out silently |
| Intersection of allowed/forbidden | Rejected at EC-05 |
| Upstream tier 0, downstream tier 0 | Accepted (equal tier) |
| Upstream tier 1, downstream tier 0 | Accepted (de-escalation) |
| Upstream tier 0, downstream tier 1 | Rejected at EC-08 (escalation) |
| Duplicate edge_id in graph | Rejected at graph build time |
| Invalid SHA-256 hex in evidence_handoff | Rejected at EC-06 |
