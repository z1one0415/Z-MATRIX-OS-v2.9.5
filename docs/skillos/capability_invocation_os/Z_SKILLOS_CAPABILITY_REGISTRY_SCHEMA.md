# Z-SkillOS Capability Registry Schema

## Status

Z_SKILLOS_CAPABILITY_REGISTRY_SCHEMA_READY

## Scope

FUTURE_PLAN_ONLY. Defines the schema for the Z-MATRIX capability registry. No implementation.

## Registry Entry Schema

| Field | Type | Description |
|:--|:--|:--|
| `skill_id` | String | Unique identifier |
| `module` | String | Z-MATRIX module name |
| `capability_name` | String | Human-readable capability name |
| `purpose` | String | What the capability does |
| `input_schema` | Schema | Expected input structure |
| `output_schema` | Schema | Expected output structure |
| `risk_tier` | Int (0-5) | Tier classification |
| `side_effect_level` | Enum | none/file/network/external |
| `permission_required` | Boolean | Whether explicit permission is needed |
| `evidence_required` | Boolean | Whether evidence must be captured |
| `allowed_callers` | List[String] | Callers permitted to invoke |
| `forbidden_actions` | List[String] | Actions permanently blocked |
| `composition_rules` | Object | How this skill chains with others |
| `rollback_policy` | String | How to undo/rollback |
| `audit_policy` | String | Evidence retention rules |
| `human_approval_required` | Boolean | Whether human must approve |

## No implementation. Level 5 remains BLOCKED.
