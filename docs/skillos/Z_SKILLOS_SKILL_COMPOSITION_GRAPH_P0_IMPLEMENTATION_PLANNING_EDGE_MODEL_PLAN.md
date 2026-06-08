# Z-SkillOS Skill Composition Graph P0 Implementation Planning — EDGE MODEL PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the complete implementation specification for the CompositionEdge data model:
data class structure, field governance (allow-list/deny-list), permission propagation checks,
evidence handoff protocol, and validation rules (EC-01 through EC-10).

## 2. Data Model: CompositionEdge

### 2.1 Field Definition

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | edge_id | str (UUID4) | Yes | Globally unique edge identifier |
| 2 | upstream_node_id | str (UUID4) | Yes | Source node identifier |
| 3 | downstream_node_id | str (UUID4) | Yes | Target node identifier |
| 4 | allowed_data_fields | list[str] | Yes | Explicit allow-list of data fields |
| 5 | forbidden_data_fields | list[str] | Yes | Explicit deny-list of data fields |
| 6 | evidence_handoff | str (SHA-256) | Yes | Hash of upstream output for downstream |
| 7 | permission_propagation | dict | Yes | {upstream_tier, downstream_tier, is_valid} |
| 8 | created_at | str (ISO 8601) | Yes | Edge creation timestamp |
| 9 | version | str | Yes | Semantic version of edge contract |
| 10 | metadata | dict | No | Optional key-value metadata |

### 2.2 Edge Contract Rules (EC-01 through EC-10)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| EC-01 | edge_id must be a valid UUID4 string | Build-time validation |
| EC-02 | upstream/downstream node_ids must reference existing nodes | Build-time validation |
| EC-03 | upstream_node_id != downstream_node_id (no self-edges) | Build-time rejection |
| EC-04 | allowed_data_fields must not be empty in P0 | Build-time validation |
| EC-05 | forbidden_data_fields and allowed_data_fields must not intersect | Build-time rejection |
| EC-06 | evidence_handoff must be valid SHA-256 hex (64 chars) | Build-time validation |
| EC-07 | permission_propagation.is_valid must be True | Build-time rejection |
| EC-08 | downstream_node tier <= upstream_node tier | Build-time enforcement |
| EC-09 | created_at must be ISO 8601 format | Build-time validation |
| EC-10 | Edge is immutable after graph build() is called | Runtime enforcement |

## 3. Field Governance Model

### 3.1 Allow-List Semantics
Only fields listed in allowed_data_fields may flow through the edge. Unlisted fields are silently dropped.

### 3.2 Deny-List Semantics
Fields in forbidden_data_fields must never flow through the edge. Intersection with allow-list triggers EC-05.

### 3.3 Intersection Logic
```python
def validate_field_governance(self):
    intersection = set(self.allowed_data_fields) & set(self.forbidden_data_fields)
    if intersection:
        raise EdgeValidationError("EC-05", f"Field intersection: {intersection}")
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
    return {"upstream_tier": upstream_tier, "downstream_tier": downstream_tier,
            "is_valid": is_valid,
            "reason": None if is_valid else f"Escalation: {upstream_tier} -> {downstream_tier}"}
```

## 5. Evidence Handoff Protocol

```python
def compute_evidence_handoff(self, upstream_node_hash: str) -> str:
    payload = {"upstream_node_hash": upstream_node_hash, "edge_id": self.edge_id, "timestamp": self.created_at}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
```

## 6. Edge Lifecycle

```
[Create] -> [Validate EC-01..EC-10] -> [Add to Graph] -> [Graph.build()] -> [Frozen]
                                                                              |
                                                                              +- success -> [COMPLETE]
                                                                              +- failure -> [DEGRADE with edge_marker]
```

## 7. Edge Cases

| Case | Behavior |
|------|----------|
| Self-edge (A->A) | Rejected at EC-03 |
| Non-existent node reference | Rejected at EC-02 |
| Empty allowed_data_fields | Accepted (no data flows) |
| Forbidden field in handoff data | Filtered out silently |
| Intersection allowed/forbidden | Rejected at EC-05 |
| Upstream tier 0, downstream tier 1 | Rejected at EC-08 (escalation) |
| Duplicate edge_id in graph | Rejected at graph build time |
| Invalid SHA-256 hex | Rejected at EC-06 |
