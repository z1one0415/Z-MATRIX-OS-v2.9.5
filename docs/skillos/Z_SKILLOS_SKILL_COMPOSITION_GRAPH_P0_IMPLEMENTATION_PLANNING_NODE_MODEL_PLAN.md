# Z-SkillOS Skill Composition Graph P0 Implementation Planning — NODE MODEL PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the complete implementation specification for the CompositionNode data model.
It covers the data class structure, field contracts, validation rules, immutability contract, hash
computation method, and edge-case handling. All specifications are documentation-only in P0.

## 2. Data Model: CompositionNode

### 2.1 Field Definition

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | node_id | str (UUID4) | Yes | Globally unique node identifier |
| 2 | capability_id | str | Yes | Registered capability identifier |
| 3 | module_adapter_id | str | Yes | Path to adapter in capability invocation OS |
| 4 | permission_tier | int (0-5) | Yes | Execution permission level |
| 5 | input_schema | dict (JSON Schema) | Yes | Expected input specification |
| 6 | output_schema | dict (JSON Schema) | Yes | Expected output specification |
| 7 | degradation_result | dict | Yes | Result produced on node failure |
| 8 | created_at | str (ISO 8601) | Yes | Node creation timestamp |
| 9 | version | str | Yes | Semantic version of node contract |
| 10 | metadata | dict | No | Optional key-value metadata |

### 2.2 Permission Tier Enumeration

| Tier | Name | P0 Allowed | Description |
|------|------|:----------:|-------------|
| 0 | READONLY | ✅ | Read-only capability; no state modification |
| 1 | PLANNING | ✅ | Planning-only; creates plans but does not execute |
| 2 | RESEARCH | ❌ | Research analysis; P1+ |
| 3 | ADVISORY | ❌ | Advisory output; P1+ |
| 4 | EXECUTION | ❌ | Write/execute capability; never in P0 |
| 5 | PRODUCTION | ❌ | Production/broker/real_trade; never in P0 |

### 2.3 Node Contract Rules (NC-01 through NC-10)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| NC-01 | node_id must be a valid UUID4 string | Build-time validation |
| NC-02 | capability_id must match registry pattern ^[a-z][a-z0-9_]+$ | Build-time validation |
| NC-03 | module_adapter_id must be a valid filesystem path under composition/ | Build-time validation |
| NC-04 | permission_tier must be 0 or 1 in P0 | Build-time rejection if tier > 1 |
| NC-05 | input_schema must be valid JSON Schema (draft-07 or later) | Build-time validation |
| NC-06 | output_schema must be valid JSON Schema (draft-07 or later) | Build-time validation |
| NC-07 | degradation_result must be present and non-null | Build-time validation |
| NC-08 | created_at must be ISO 8601 format | Build-time validation |
| NC-09 | version must follow semver pattern | Build-time validation |
| NC-10 | Node is immutable after graph build() is called | Runtime enforcement |

## 3. Validation Rules

### 3.1 Node-Level Validation

```python
def validate(self) -> List[NodeValidationError]:
    errors = []
    if not UUID_PATTERN.match(self.node_id):
        errors.append(NodeValidationError("NC-01", "Invalid node_id UUID4"))
    if not CAPABILITY_ID_PATTERN.match(self.capability_id):
        errors.append(NodeValidationError("NC-02", "Invalid capability_id pattern"))
    if not os.path.exists(self.module_adapter_id):
        errors.append(NodeValidationError("NC-03", "Module adapter path not found"))
    if self.permission_tier not in (0, 1):
        errors.append(NodeValidationError("NC-04", f"Tier {self.permission_tier} not allowed in P0"))
    if not self._validate_json_schema(self.input_schema):
        errors.append(NodeValidationError("NC-05", "Invalid input JSON Schema"))
    if not self._validate_json_schema(self.output_schema):
        errors.append(NodeValidationError("NC-06", "Invalid output JSON Schema"))
    if self.degradation_result is None:
        errors.append(NodeValidationError("NC-07", "degradation_result must not be None"))
    if not self._validate_iso8601(self.created_at):
        errors.append(NodeValidationError("NC-08", "Invalid ISO 8601 timestamp"))
    if not SEMVER_PATTERN.match(self.version):
        errors.append(NodeValidationError("NC-09", "Invalid semver version"))
    return errors
```

### 3.2 Pseudo-Code: Evidence Hash

```python
def compute_evidence_hash(self, input_data: dict, output_data: dict) -> str:
    canonical_input = json.dumps(
        {"capability_id": self.capability_id, "input": input_data,
         "output": output_data, "timestamp": self.created_at},
        sort_keys=True, separators=(',', ':')
    )
    return hashlib.sha256(canonical_input.encode('utf-8')).hexdigest()
```

## 4. Immutability Contract

1. After `graph.build()` is called, all nodes become immutable.
2. Any attempt to modify a node field post-build raises `NodeImmutabilityError`.
3. Node immutability is enforced via a frozen flag set at build time.
4. Evidence hash is computed at build time and cached; recomputation with different inputs is forbidden.

## 5. Edge Cases

| Case | Behavior |
|------|----------|
| Duplicate node_id in graph | Rejected at graph build time |
| Missing capability_id in registry | Warning; node is accepted but may fail at execution (P1+) |
| Tier 2-5 node in P0 graph | Rejected at node validation time with NC-04 |
| Empty input_schema | Accepted (no input required) |
| Empty output_schema | Accepted (no output produced) |
| Invalid JSON Schema | Rejected at NC-05/NC-06 |
| None degradation_result | Rejected at NC-07 |
| Future timestamp | Accepted (timestamp is metadata only) |
| Past timestamp | Accepted (timestamp is metadata only) |

## 6. JSON Schema Representation

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["node_id", "capability_id", "module_adapter_id", "permission_tier",
               "input_schema", "output_schema", "degradation_result", "created_at", "version"],
  "properties": {
    "node_id": {"type": "string", "format": "uuid"},
    "capability_id": {"type": "string", "pattern": "^[a-z][a-z0-9_]+$"},
    "module_adapter_id": {"type": "string"},
    "permission_tier": {"type": "integer", "minimum": 0, "maximum": 1},
    "input_schema": {"type": "object"},
    "output_schema": {"type": "object"},
    "degradation_result": {"type": "object"},
    "created_at": {"type": "string", "format": "date-time"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+(-[a-z0-9.]+)?$"},
    "metadata": {"type": "object"}
  }
}
```

## 7. Node Lifecycle

```
[Create] → [Validate (NC-01..NC-10)] → [Add to Graph] → [Graph.build()] → [Frozen]
                                                                              │
                                                                              ├─ success → [COMPLETE]
                                                                              └─ failure → [DEGRADE]
```
