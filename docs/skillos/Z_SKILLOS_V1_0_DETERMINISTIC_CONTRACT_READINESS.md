# Z-SkillOS v1.0 Deterministic Skill Contract Readiness

## Status

Z_SKILLOS_V1_0_DETERMINISTIC_CONTRACT_READINESS_PREPARED

## Scope

This document defines the upgrade readiness gate for Z-SkillOS v1.0. It does NOT implement v1.0. It establishes what must exist before v1.0 implementation can begin.

## v1.0 Goal

Upgrade Z-SkillOS from "Agent can invoke" to "every invocation is verifiable, reproducible, auditable, and blockable."

Current v0.x state: callable + safe + registered.
Target v1.0 state: callable + safe + registered + deterministic contract.

## Skill Contract Registry

### Target

`data/research_db/agent/registry/skill_contract_registry.json`

### Required Fields per Registered Skill

```json
{
  "skill_id": "DOMAIN.SKILL_NAME",
  "skill_version": "1.0.0",
  "domain": "DOMAIN",
  "risk_level": "R0_READ | R1_ANNOTATE | R2_DRAFT",
  "input_schema": {
    "type": "object",
    "required": ["..."],
    "properties": {}
  },
  "output_schema": {
    "type": "object",
    "required": ["skill_id", "skill_version", "status", "risk_level", "input_hash", "output_hash"],
    "properties": {}
  },
  "status": "ACTIVE | DEPRECATED | SUPERSEDED",
  "write_layers": [],
  "requires_human_review": true,
  "proposal_required": true,
  "semantic_category": "DETERMINISTIC | STRUCTURED_DRAFT | NARRATIVE_RENDERER"
}
```

### Coverage Target

- 100% of 104+ registered skills must have contract entries
- 0 skills without input_schema
- 0 skills without output_schema

## Input Schema Target

Every skill must declare:

- Required input fields with types
- Optional input fields with types and defaults
- Data snapshot binding requirement (where applicable)

Examples:

```json
{
  "ticker": {"type": "string", "pattern": "^[0-9]{6}$"},
  "data_snapshot_id": {"type": "string", "required": false},
  "dry_run": {"type": "boolean", "default": true}
}
```

## Output Schema Target

Every skill invocation must produce:

| Field | Type | Description |
|:--|:--|:--|
| `skill_id` | string | DOMAIN.SKILL_NAME |
| `skill_version` | string | semver |
| `status` | string | SUCCESS / PARTIAL / FAILED / BLOCKED |
| `risk_level` | string | R0/R1/R2 |
| `input_hash` | string | SHA-256 of canonicalized input |
| `output_hash` | string | SHA-256 of deterministic output fields |
| `data_snapshot_id` | string | snapshot binding (or null) |
| `evidence_refs` | list | references to source evidence |
| `safety_envelope` | object | risk flags, blocking reasons |

## Output Structure per Semantic Category

### DETERMINISTIC Skills

```json
{
  "facts": {},
  "checks": {},
  "result": {},
  "skill_id": "...",
  "skill_version": "...",
  "input_hash": "...",
  "output_hash": "..."
}
```

### STRUCTURED_DRAFT Skills

```json
{
  "facts": {},
  "checks": {},
  "judgment_slots": {},
  "narrative": "",
  "safety_envelope": {},
  "evidence_refs": [],
  "skill_id": "...",
  "skill_version": "...",
  "input_hash": "...",
  "output_hash": "..."
}
```

### NARRATIVE_RENDERER Skills

```json
{
  "facts": {},
  "checks": {},
  "judgment_slots": {},
  "narrative": "",
  "safety_envelope": {},
  "evidence_refs": [],
  "skill_id": "...",
  "skill_version": "...",
  "input_hash": "...",
  "output_hash": "..."
}
```

## Invocation Validation

`invoke_skill()` must enforce:

1. `input_schema` validation before execution
2. `output_schema` validation after execution
3. Reject unregistered skill_id
4. Reject mismatched input_schema
5. Flag output without required contract fields
6. Reject invocation where `risk_level > max_risk`

## Data Snapshot Binding

All RESEARCHDB / FACTOR / MATRIX / COUNCIL / PORTFOLIO / WORKFLOW skills must include:

- `data_snapshot_id` in output
- snapshot manifest: market_data + factor + case_registry + source_health versions
- Missing snapshot → `DATA_SNAPSHOT_REQUIRED` status

## Future Verification

### verify_z_skillos_v1_contract.sh (target, not yet created)

Must verify:

1. Skill contract registry exists and is valid JSON
2. 100% of registered skills have contract entries
3. 100% of contract entries have input_schema
4. 100% of contract entries have output_schema
5. `invoke_skill()` enforces input_schema validation
6. `invoke_skill()` enforces output_schema validation
7. Sample invocation produces valid output with all required fields
8. Missing data_snapshot → DATA_SNAPSHOT_REQUIRED

## Implementation Phases (future, not now)

| Phase | Content | When |
|:--|------|------|
| v1.0 | Skill contract registry + input/output schema | After readiness approved |
| v1.1 | Golden Input/Output Lock | After v1.0 verified |
| v1.2 | Semantic Drift Regression | After v1.1 verified |
| v1.3 | Skill Result Ledger | After v1.2 verified |
| v1.4 | Data Snapshot Binding | After v1.3 verified |

## Readiness Decision

v1.0 implementation does NOT start now.

This readiness document defines what must be true before v1.0 can begin.

## Forbidden

- v1.0 code implementation from this readiness phase
- schema enforcement without registry
- contract without verification
- semantic drift without regression tests
- tag
- production / broker / real_trade
