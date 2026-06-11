# Event Log Contract

## Purpose

The Event Log provides a chronological audit trail of all actions, decisions, and state transitions across the Z-Matrix-OS system. Each event records what happened, when, who (or which component) triggered it, the result, and any associated evidence.

## Schema

Refer to `skillos/frontend_handoff/state_registry/event_log_schema.json` for the authoritative JSON Schema definition.

## Event Fields

| Field | Type | Description |
|:--|:--|:--|
| `event_id` | string | Unique event identifier |
| `timestamp` | datetime | ISO 8601 timestamp of the event |
| `action` | string | Action performed (e.g., `gate_passed`, `validation_run`, `abort_triggered`) |
| `source` | string | Component or agent that emitted the event |
| `result` | string | Result of the action (e.g., `PASS`, `FAIL`, `ABORTED`) |
| `gate_id` | string | Associated gate ID (if applicable) |
| `run_id` | string | Associated run ID (if applicable) |
| `commit_sha` | string | Git commit SHA at time of event |
| `details` | string | Additional details about the event |
| `evidence_refs` | array | References to evidence chain nodes |
| `user_triggered` | boolean | Whether triggered by a human user |

## Standard Actions

| Action | Description |
|:--|:--|
| `gate_passed` | A decision gate was passed |
| `gate_blocked` | A decision gate was blocked |
| `gate_sealed` | A passed gate was sealed immutable |
| `validation_run` | A validation pipeline was executed |
| `validation_completed` | A validation pipeline completed |
| `abort_triggered` | An abort was triggered |
| `audit_performed` | An audit was conducted |
| `review_submitted` | A human review was submitted |
| `safety_patch_applied` | A safety patch was applied |
| `chain_sealed` | The entire gate chain was sealed |

## API Endpoint

```
GET /api/audit-trail
```

Returns an `AuditTrailDemo` object conforming to `event_log_schema.json`.

## Ordering

Events are ordered chronologically by `timestamp`. Ties are broken by `event_id` order within the array.

## Integrity

- All events are append-only
- Each event references relevant gate IDs and evidence nodes
- `user_triggered` distinguishes human-initiated events from automated ones
- Events link to the git commit SHA in effect at the time

## Sample Event

```json
{
  "event_id": "EVT-F7.2-001",
  "timestamp": "2026-06-05T00:00:00Z",
  "action": "gate_sealed",
  "source": "A3-state-evidence-registry",
  "result": "MERGED_AND_SEALED",
  "gate_id": "F7.2-decision-gate",
  "commit_sha": "03c8de6e",
  "details": "F7.2 decision gate passed and sealed immutable",
  "evidence_refs": ["ev-F7.2-decision-001"],
  "user_triggered": true
}
```

## Safety

- No real-trade events appear in frontend demo data
- All `user_triggered` events reflect the review/decision gate pattern
- Automated events (e.g., validation runs) have `user_triggered: false`
