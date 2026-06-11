# Gate State Registry

## Purpose

The Gate State Registry maintains a complete audit of all decision gates in a gate chain. Each gate records its status, parent/child relationships, blocked actions, evidence references, and safety flags. This is the authoritative source for frontend gate matrix rendering.

## Schema

Refer to `skillos/frontend_handoff/state_registry/gate_state_schema.json` for the authoritative JSON Schema definition.

## Gate Status Enum

| Status | Meaning |
|:--|:--|
| `PASS` | Gate passed cleanly |
| `PASS_WITH_NOTE` | Gate passed with advisory note |
| `PASS_WITH_SEMANTIC_FIELD_NOTE` | Gate passed with semantic field annotation |
| `BLOCKED` | Gate is blocked; cannot proceed |
| `PENDING` | Gate has not yet been evaluated |
| `ABORTED` | Gate evaluation was aborted |
| `DEGRADED` | Gate passed but in degraded mode |
| `DISABLED_DEFAULT` | Gate is disabled by default |
| `MERGED_AND_SEALED` | Gate passed, merged, and sealed immutable |

## Gate Fields

| Field | Type | Description |
|:--|:--|:--|
| `gate_id` | string | Unique gate identifier (e.g., `F7.0-logical-reconcile`) |
| `stage` | integer | Sequential stage number in chain |
| `commit` | string | Git commit SHA for this gate |
| `parent_commit` | string | Git commit SHA of parent gate |
| `status` | enum | Gate status (see Status Enum above) |
| `scope` | string | Scope description of what this gate validates |
| `allowed_next_entries` | array | List of gate_ids allowed to follow |
| `blocked_actions` | array | List of actions blocked by this gate |
| `evidence_refs` | array | References to evidence chain nodes |
| `created_at` | datetime | ISO 8601 timestamp of gate creation |
| `human_decision_required` | boolean | Whether a human decision is required |
| `promotion_allowed` | boolean | Whether factor promotion is allowed beyond this gate |
| `alpha_claim_allowed` | boolean | Whether alpha claims are allowed beyond this gate |
| `runner_enabled` | boolean | Whether the pipeline runner is active for this gate |
| `paper_trading_allowed` | boolean | Whether paper trading is allowed beyond this gate |
| `production` | boolean | Whether this is a production gate |
| `broker_runtime` | enum | `none`, `paper`, `live`, `both` |
| `real_trade` | boolean | Whether real trades are permitted beyond this gate |

## F7.2 Gate Chain

The canonical F7.2 formal validation gate chain consists of 11 gates (stage 0 through stage 10):

| Stage | gate_id | Commit | Status |
|:--:|:--|:--|:--|
| 0 | `F7.0-logical-reconcile` | `e636dcfa` | MERGED_AND_SEALED |
| 1 | `F7.2-planning-review` | `e1373225` | MERGED_AND_SEALED |
| 2 | `F7.2-execution-plan` | `6de8802d` | MERGED_AND_SEALED |
| 3 | `F7.2-execution-auth` | `c1d1e38d` | MERGED_AND_SEALED |
| 4 | `F7.2-final-exec-auth` | `2448124e` | MERGED_AND_SEALED |
| 5 | `F7.2-human-val-auth` | `597aaa32` | MERGED_AND_SEALED |
| 6 | `F7.2-val-readonly` | `ea80ff9a` | MERGED_AND_SEALED |
| 7 | `F7.2-val-audit` | `b9f77abb` | MERGED_AND_SEALED |
| 8 | `F7.2-safety-patch` | `18429840` | MERGED_AND_SEALED |
| 9 | `F7.2-human-interpret` | `4dcef2ab` | MERGED_AND_SEALED |
| 10 | `F7.2-decision-gate` | `03c8de6e` | MERGED_AND_SEALED |

## Safety Constraints

All gates in the F7.2 chain enforce:
- `promotion_allowed`: `false` everywhere
- `alpha_claim_allowed`: `false` everywhere
- `paper_trading_allowed`: `false` everywhere
- `production`: `false` everywhere
- `broker_runtime`: `"none"` everywhere
- `real_trade`: `false` everywhere
- `runner_enabled`: `true` only at stage 6 (`F7.2-val-readonly`)

## API Endpoint

```
GET /api/gate-state
```

Returns a `GateStateDemo` object conforming to `gate_state_schema.json`.

## Fixture Location

`tests/skillos/frontend_handoff/state_registry/gate_state_demo.json` — complete F7.2 gate chain with audited commit SHAs and correct statuses.
