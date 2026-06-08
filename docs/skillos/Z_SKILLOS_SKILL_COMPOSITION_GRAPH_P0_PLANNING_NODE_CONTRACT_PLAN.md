# Z-SkillOS Skill Composition Graph P0 Planning — NODE CONTRACT PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Node Contract Definition

A Node Contract is the formal specification that every composition graph node must satisfy before
it can participate in any graph. The contract defines a node's identity, capability binding, permission
tier, input/output schemas, and degradation behavior.

## 2. Contract Fields

### 2.1 `capability_id` (string, required)
Unique identifier for the capability this node represents. Must match a registered capability
in the SkillOS Capability Registry. Format: `{domain}.{category}.{name}@{version}`.
Example: `research.financial.equity_analysis@v1.0.0`.

### 2.2 `module_adapter_id` (string, required)
Path to the adapter module in the Capability Invocation OS. Must be a valid filesystem path
relative to the SkillOS adapter directory. Example: `adapters/research/equity_analysis.py`.

### 2.3 `permission_tier` (integer, required)
Numeric tier level for this node. P0 supports only tiers 0 and 1:
- Tier 0: READONLY — can read data but cannot produce plans
- Tier 1: PLANNING — can read data and produce plan structures
- Tier 2+: BLOCKED in P0 — research, advisory, production not accessible

### 2.4 `input_schema` (object, required)
JSON Schema definition for the input this node accepts. Must specify:
- `type`: always "object"
- `properties`: typed field definitions
- `required`: list of required fields
- `additionalProperties`: must be `false` (strict schema)

### 2.5 `output_schema` (object, required)
JSON Schema definition for the output this node produces. Same structure as input_schema.
For P0 dry plans, output is a no-op marker: `{"status": "noop", "node_id": "<id>"}`.

### 2.6 `degradation_result` (object, required)
What this node returns on failure:
- Primary: `{"status": "degraded", "reason": "noop", "node_id": "<id>"}`
- Secondary: `{"status": "degraded", "reason": "plan_only", "graph_id": "<id>"}`
- Never: fail-closed, hang, timeout without resolution

### 2.7 `boundary` (object, required)
Explicit boundary markers for this node:
- `max_input_size_bytes`: maximum input payload size (default: 1048576 = 1MB)
- `max_execution_time_ms`: maximum time for node processing (default: 5000ms)
- `max_output_size_bytes`: maximum output payload size (default: 1048576)
- `allowed_side_effects`: P0 must be empty list `[]`

## 3. Node Contract Validation Rules

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| NC-01 | capability_id must exist in registry | Compile-time |
| NC-02 | module_adapter_id must resolve to valid path | Compile-time |
| NC-03 | permission_tier must be 0 or 1 in P0 | Compile-time |
| NC-04 | input_schema must be valid JSON Schema | Compile-time |
| NC-05 | output_schema must be valid JSON Schema | Compile-time |
| NC-06 | degradation_result must conform to DegradationProtocol | Compile-time |
| NC-07 | boundary fields must be within P0 limits | Compile-time |
| NC-08 | allowed_side_effects must be empty | Compile-time + runtime |
| NC-09 | Node cannot self-reference in degradation_result | Compile-time |
| NC-10 | input_schema.additionalProperties must be false | Compile-time |

## 4. Node Contract Example (P0 Single-Node Dry Plan)

```json
{
  "node_id": "n001",
  "capability_id": "research.financial.news_sentiment@v1.0.0",
  "module_adapter_id": "adapters/research/news_sentiment.py",
  "permission_tier": 1,
  "input_schema": {
    "type": "object",
    "properties": {
      "symbols": {"type": "array", "items": {"type": "string"}},
      "date_range_days": {"type": "integer", "minimum": 1, "maximum": 30}
    },
    "required": ["symbols"],
    "additionalProperties": false
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["noop"]},
      "node_id": {"type": "string"}
    },
    "required": ["status", "node_id"],
    "additionalProperties": false
  },
  "degradation_result": {
    "status": "degraded",
    "reason": "noop",
    "node_id": "n001"
  },
  "boundary": {
    "max_input_size_bytes": 1048576,
    "max_execution_time_ms": 5000,
    "max_output_size_bytes": 1048576,
    "allowed_side_effects": []
  }
}
```

## 5. Node Degradation Protocol

When a node fails, it must follow this protocol:
1. Catch the exception/error
2. Set output to `degradation_result`
3. Set internal `degraded: true` flag
4. Propagate degradation marker upstream to graph
5. Do NOT throw uncaught exceptions
6. Do NOT hang or block
7. Complete within `max_execution_time_ms`

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|NODE_CONTRACT|v1.0.0-draft`
