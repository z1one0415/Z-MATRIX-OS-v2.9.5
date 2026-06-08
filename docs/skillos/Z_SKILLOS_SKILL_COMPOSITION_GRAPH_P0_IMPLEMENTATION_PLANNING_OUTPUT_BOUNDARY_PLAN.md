# Z-SkillOS Skill Composition Graph P0 Implementation Planning — OUTPUT BOUNDARY PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for output boundary enforcement in the
composition graph. Covers output schema validation, forbidden field blocking at edge handoff,
result envelope immutability, output truncation, and the full output boundary policy.

## 2. Output Boundary Model

### 2.1 Protection Layers

```
[GRAPH OUTPUT]
  [EDGE HANDOFF FILTER]
    [NODE OUTPUT SCHEMA]
      [RESULT ENVELOPE (immutable)]
```

### 2.2 What the Output Boundary Protects

| Boundary | Protection |
|----------|------------|
| Node output | Enforced against output_schema |
| Edge handoff | Only allowed_data_fields pass; forbidden blocked |
| Result envelope | Immutable after node completion |
| Graph output | Enforced against all node outputs combined |
| Field leakage | No field transits without explicit edge allow-list |

## 3. Node Output Schema Enforcement

```python
def enforce_output_schema(node: CompositionNode, actual_output: dict) -> List[SchemaMismatchError]:
    errors = []
    required_fields = node.output_schema.get("required", [])
    for field in required_fields:
        if field not in actual_output:
            errors.append(SchemaMismatchError(f"Required field '{field}' missing"))
    properties = node.output_schema.get("properties", {})
    for field, value in actual_output.items():
        if field in properties:
            expected_type = properties[field].get("type")
            if expected_type and not _type_matches(value, expected_type):
                errors.append(SchemaMismatchError(
                    f"Field '{field}': expected {expected_type}, got {type(value).__name__}"
                ))
    if not node.output_schema.get("additionalProperties", True):
        extra = set(actual_output.keys()) - set(properties.keys())
        if extra:
            errors.append(SchemaMismatchError(f"Extra fields not allowed: {extra}"))
    return errors
```

## 4. Edge Handoff Filtering

```python
def block_forbidden_fields(edge: CompositionEdge, upstream_output: dict) -> dict:
    filtered = {}
    for field, value in upstream_output.items():
        if field in edge.forbidden_data_fields:
            continue  # Blocked
        if field in edge.allowed_data_fields:
            filtered[field] = value  # Allowed
        # Neither: silently dropped
    return filtered
```

### Field Governance Scenarios

| Allow List | Forbid List | Upstream Output | Filtered Output |
|------------|-------------|-----------------|-----------------|
| ["price"] | [] | {"price":100,"volume":50} | {"price":100} |
| ["price","volume"] | ["volume"] | {"price":100,"volume":50} | {"price":100} |
| ["*"] | [] | {"price":100} | {"price":100} |

## 5. Result Envelope Immutability

```python
class ImmutableResultEnvelope:
    def __init__(self, data: dict):
        self._data = deepcopy(data)
        self._frozen = False

    def freeze(self):
        self._frozen = True

    def __setitem__(self, key, value):
        if self._frozen:
            raise ResultEnvelopeMutationError("Cannot mutate frozen result envelope")
        self._data[key] = value

    @property
    def data(self) -> dict:
        return deepcopy(self._data)
```

### What Immutability Prevents
1. Post-hoc mutation of node output after downstream acceptance
2. Evidence tampering by modifying output to break hash chains
3. Covert data injection after validation
4. Permission bypass via output field elevation

## 6. Output Truncation Boundary

```python
EVIDENCE_TRUNCATION_LIMIT = 1024 * 1024  # 1 MB

def truncate_for_hash(data: dict) -> dict:
    serialized = canonical_json(data)
    if len(serialized) > EVIDENCE_TRUNCATION_LIMIT:
        return {"_truncated": True, "_data": serialized[:EVIDENCE_TRUNCATION_LIMIT]}
    return data
```

Truncation applies to evidence hash computation only, not to actual data flow.

## 7. Output Boundary Policy Rules (OB-01 through OB-07)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| OB-01 | Every node output must conform to declared output_schema | Node-level schema validation |
| OB-02 | Edge handoff drops all fields not in allowed_data_fields | Edge filtering at handoff |
| OB-03 | Edge handoff blocks all fields in forbidden_data_fields | Edge filtering at handoff |
| OB-04 | Result envelope is immutable after node completion | ImmutableResultEnvelope freeze |
| OB-05 | No post-hoc mutation of any node or edge output | Immutability contract |
| OB-06 | Evidence hash uses truncated output if >1MB | Truncation before hashing |
| OB-07 | Allowed and forbidden field lists must not intersect | EC-05 at edge validation |
