# Run State Registry

## Purpose

The Run State Registry tracks pipeline execution runs across the Z-Matrix-OS system. It records run identifiers, execution status, stage-level timing, abort reasons, and safety flags for the frontend handoff dashboard.

## Schema

Refer to `skillos/frontend_handoff/state_registry/run_state_schema.json` for the authoritative JSON Schema definition.

## Fields

| Field | Type | Description |
|:--|:--|:--|
| `run_id` | string | Unique run identifier (e.g., `RUN-20260612-001`) |
| `pipeline_name` | string | Pipeline name (e.g., `F7.2-formal-validation`) |
| `status` | enum | `NOT_STARTED`, `RUNNING`, `PAUSED`, `COMPLETED`, `ABORTED`, `DEGRADED`, `TIMED_OUT` |
| `created_at` | datetime | ISO 8601 creation timestamp |
| `started_at` | datetime | ISO 8601 start timestamp |
| `completed_at` | datetime | ISO 8601 completion timestamp |
| `duration_seconds` | number | Total run duration in seconds |
| `abort_reason` | string | Reason for abort (if status is `ABORTED`) |
| `abort_source` | string | Component that triggered the abort |
| `stages` | array | Ordered list of pipeline stages with timing |
| `runtime_enabled` | boolean | Whether pipeline runtime is enabled |
| `runner_enabled` | boolean | Whether pipeline runner is enabled |
| `commit_sha` | string | Git commit SHA at time of run |
| `tags` | array | Categorization tags |

## Stage Objects

Each stage in the `stages` array contains:

| Field | Type | Description |
|:--|:--|:--|
| `stage_id` | string | Stage identifier |
| `name` | string | Human-readable stage name |
| `status` | enum | `NOT_STARTED`, `RUNNING`, `COMPLETED`, `FAILED`, `SKIPPED`, `ABORTED` |
| `started_at` | datetime | Stage start timestamp |
| `completed_at` | datetime | Stage completion timestamp |
| `duration_seconds` | number | Stage duration |
| `error` | string | Error message (if failed) |

## API Endpoint

```
GET /api/run-state
```

Returns a `RunStateDemo` object conforming to `run_state_schema.json`.

## Safety Constraints

Per the Scope Lock:
- `runtime_enabled` is `false` in all frontend demo data
- `runner_enabled` is `false` in all frontend demo data
- No real pipeline executions occur through the frontend

## Fixture Location

`tests/skillos/frontend_handoff/state_registry/gate_state_demo.json` — for related gate chain data.
