# Z-SkillOS Skill Composition Graph P0 Implementation Planning — OUTPUT BOUNDARY PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for output boundary enforcement in the
composition graph. It covers output schema validation, forbidden field blocking at edge handoff,
result envelope immutability, output truncation, and the full output boundary policy.

## 2. Output Boundary Model

### 2.1 What the Output Boundary Protects

| Boundary | Protection |
|----------|------------|
| Node output | Enforced against node's output_schema |
| Edge handoff | Only allowed_data_fields pass; forbidden_data_fields blocked |
| Result envelope | Immutable after node completion; no post-hoc mutation |
| Graph output | Enforced against all node outputs combined |
| Field leakage | No field can transitively flow without explicit edge allow-list entry |

### 2.2 Boundary Layers

```
┌─────────────────────────────────────────────┐
│                GRAPH OUTPUT                  │
│  ┌───────────────────────────────────────┐  │
│  │          EDGE HANDOFF FILTER          │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │       NODE OUTPUT SCHEMA        │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │    RESULT ENVELOPE        │  │  │  │
│  │  │  │    (immutable)            │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## 3. Node Output Schema Enforcement

### 3.1 Schema Validation

```python
def enforce_output_schema(node: CompositionNode, actual_output: dict) -> List[SchemaMismatchError]:
    """Validate actual output against node's declared output_schema."""
    errors = []

    # Check required fields
    required_fields = node.output_schema.get("required", [])
    for field in required_fields:
        if field not in actual_output:
            errors.append(SchemaMismatchError(
                f"Required output field '{field}' missing"
            ))

    # Check field types
    properties = node.output_schema.get("properties", {})
    for field, value in actual_output.items():
        if field in properties:
            expected_type = properties[field].get("type")
            if expected_type and not _type_matches(value, expected_type):
                errors.append(SchemaMismatchError(
                    f"Field '{field}': expected {expected_type}, got {type(value).__name__}"
                ))

    # Check additional properties
    if not node.output_schema.get("additionalProperties", True):
        allowed_fields = set(properties.keys())
        extra_fields = set(actual_output.keys()) - allowed_fields
        if extra_fields:
            errors.append(SchemaMismatchError(
                f"Extra output fields not allowed: {extra_fields}"
            ))

    return errors
```

### 3.2 Schema Constraints in P0

| Constraint | Value |
|------------|-------|
| JSON Schema version | draft-07 or later |
| Max output size | Not enforced in P0 (no execution) |
| Nesting depth | Not enforced in P0 (JSON Schema handles) |
| Circular references | FORBIDDEN (JSON Schema does not support) |

## 4. Edge Handoff Filtering

### 4.1 Forbidden Field Blocking

```python
def block_forbidden_fields(edge: CompositionEdge, upstream_output: dict) -> dict:
    """Filter upstream output through edge's field governance."""
    filtered = {}

    for field, value in upstream_output.items():
        # Block: field is in forbidden list
        if field in edge.forbidden_data_fields:
            continue
        # Allow: field is in allowed list
        if field in edge.allowed_data_fields:
            filtered[field] = value
        # Neither: field is silently dropped

    return filtered
```

### 4.2 Field Governance Scenarios

| Allow List | Forbid List | Upstream Output | Filtered Output |
|------------|-------------|-----------------|-----------------|
| ["price"] | [] | {"price": 100, "volume": 50} | {"price": 100} |
| ["price", "volume"] | ["volume"] | {"price": 100, "volume": 50} | {"price": 100} |
| ["price", "volume"] | ["price", "volume"] | {"price": 100, "volume": 50} | EC-05 rejection |
| [] | [] | {"price": 100} | {} |
| ["*"] | [] | {"price": 100, "volume": 50} | {"price": 100, "volume": 50} |

## 5. Result Envelope Immutability

### 5.1 Immutability Contract

The result envelope (the output produced by a node after processing) is immutable once set.
This is a core safety property that prevents:

1. **Post-hoc mutation**: Changing node output after it was accepted by downstream
2. **Evidence tampering**: Modifying output to break hash chains
3. **Covert data injection**: Injecting data into the output stream after validation
4. **Permission bypass**: Elevating output fields to bypass permission checks

### 5.2 Enforcement

```python
class ImmutableResultEnvelope:
    """Wrapper that prevents mutation after finalization."""

    def __init__(self, data: dict):
        self._data = deepcopy(data)
        self._frozen = False

    def freeze(self):
        self._frozen = True

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        if self._frozen:
            raise ResultEnvelopeMutationError(
                "Cannot mutate frozen result envelope"
            )
        self._data[key] = value

    @property
    def data(self) -> dict:
        return deepcopy(self._data)
```

## 6. Output Truncation Boundary

### 6.1 Evidence Hash Truncation

For evidence hash computation, large outputs may need truncation to a fixed boundary:

```python
EVIDENCE_TRUNCATION_LIMIT = 1024 * 1024  # 1 MB

def truncate_for_hash(data: dict) -> dict:
    """Truncate data to a safe size for evidence hash computation."""
    serialized = canonical_json(data)
    if len(serialized) > EVIDENCE_TRUNCATION_LIMIT:
        truncated = serialized[:EVIDENCE_TRUNCATION_LIMIT]
        return {"_truncated": True, "_data": truncated}
    return data
```

### 6.2 Truncation Policy

| Policy | Value |
|--------|-------|
| Truncation applies to | Evidence hash computation only |
| Truncation does NOT apply to | Actual data flowing through edges |
| Truncation marker | `_truncated: true` in hash input |
| Truncation is | Deterministic (same output → same truncation) |

## 7. Output Boundary Policy (OB-01 through OB-07)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| OB-01 | Every node output must conform to its declared output_schema | Node-level schema validation |
| OB-02 | Edge handoff drops all fields not in allowed_data_fields | Edge filtering at handoff time |
| OB-03 | Edge handoff blocks all fields in forbidden_data_fields | Edge filtering at handoff time |
| OB-04 | Result envelope is immutable after node completion | ImmutableResultEnvelope freeze |
| OB-05 | No post-hoc mutation of any node or edge output | Immutability contract |
| OB-06 | Evidence hash uses truncated output if >1MB | Truncation before hashing |
| OB-07 | Allowed and forbidden field lists must not intersect | EC-05 at edge validation |
