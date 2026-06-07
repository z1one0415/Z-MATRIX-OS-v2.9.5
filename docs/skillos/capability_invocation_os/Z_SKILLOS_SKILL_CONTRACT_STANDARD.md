# Z-SkillOS Skill Contract Standard

## Status

Z_SKILLOS_SKILL_CONTRACT_STANDARD_READY

## Scope

FUTURE_PLAN_ONLY. Standardized contract schema per Z-MATRIX skill.

## Contract Fields

| Field | Required | Description |
|:--|:--:|:--|
| `identity` | ✅ | skill_id, module, capability_name, version |
| `purpose` | ✅ | What the capability does |
| `inputs` | ✅ | Schema and constraints |
| `outputs` | ✅ | Schema and constraints |
| `side_effects` | ✅ | Files written, network calls, state changes |
| `risk_tier` | ✅ | 0-5 classification |
| `permissions` | ✅ | Required permissions for invocation |
| `preconditions` | ✅ | What must be true before invocation |
| `postconditions` | ✅ | What must be true after invocation |
| `forbidden_actions` | ✅ | Actions permanently blocked |
| `audit_evidence` | ✅ | What evidence must be captured |
| `rollback` | ✅ | How to undo/rollback |
| `composition_constraints` | ✅ | How this skill chains with others |
| `human_gate` | ✅ | Whether human must approve |

## No implementation. Level 5 remains BLOCKED.
