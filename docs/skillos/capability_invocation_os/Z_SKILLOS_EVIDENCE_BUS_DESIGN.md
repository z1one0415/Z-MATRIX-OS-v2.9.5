# Z-SkillOS Evidence Bus Design

## Status

Z_SKILLOS_EVIDENCE_BUS_DESIGN_READY

## Scope

FUTURE_PLAN_ONLY. End-to-end audit trail infrastructure. No implementation.

## Evidence Record Schema

| Field | Description |
|:--|:--|
| `source_snapshot` | Hash of system state before invocation |
| `input_evidence` | Full input payload hash |
| `intermediate_evidence` | Chain of intermediate results |
| `output_evidence` | Full output payload hash |
| `postcondition_evidence` | Hash of system state after invocation |
| `audit_trace` | Timestamped invocation log |
| `seal_reference` | Reference to the composition seal |
| `rollback_reference` | Reference to rollback state |

## Critical Rules

| Rule | Description |
|:--|:--|
| No evidence deletion | Evidence is append-only |
| No hidden suppression | All evidence is visible in audit |
| Versioned evidence | Each invocation produces versioned evidence |
| Scenario replay | Evidence supports full replay |
| Immutable chain | Evidence chain cannot be modified after seal |

## Evidence Flow

```
Pre-invocation snapshot → Input capture → Intermediate captures → Output capture → Post-invocation snapshot → Seal
```

## No implementation. Level 5 remains BLOCKED.
