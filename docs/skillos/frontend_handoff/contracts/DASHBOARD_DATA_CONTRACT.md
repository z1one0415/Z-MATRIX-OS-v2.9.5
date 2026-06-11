# Dashboard Data Contract — A1 Contract

## Status: FROZEN

- **Seal**: A1_CONTRACT_FREEZE
- **Version**: v0.1.0-rc
- **Contract File**: `skillos/frontend_handoff/contracts/dashboard_contract.json`
- **Frozen Date**: 2026-06-12

## Dashboard Summary Schema

The `/api/dashboard/summary` endpoint returns a single `DashboardSummary` object with:

| Field | Type | Description |
|:--|:--|:--|
| system_health | object | Health status, uptime, version info |
| gate_summary | object | Aggregate gate counts (passed/failed/pending/blocked) |
| component_status | object | Per-component status map |
| recent_activity | array | Activity feed (max 20 entries) |
| readonly | boolean | Always `true` (const) |

## Component Status Values

Each component returns one of:
- `ok` — Operating normally
- `degraded` — Partial functionality
- `error` — Component failure
- `disabled_default` — Feature disabled by default (research_report, z9_review)
- `blocked` — Safety boundary enforced

## Summary Cards (4 cards)

| Card | Type | Data Source |
|:--|:--|:--|
| System Health | Status badge (green/amber/red) | system_health.status |
| Gate Status | Summary table | gate_summary |
| Component Overview | Status grid | component_status |
| Recent Activity | Feed list (max 20) | recent_activity |

## Gate Status Indicators

| Status | Icon | Color | Meaning |
|:--|:--|:--|:--|
| passed | check_circle | green | Gate check passed |
| failed | x_circle | red | Gate check failed |
| pending | clock | amber | Gate check pending |
| blocked | shield_off | red | Gate permanently blocked |
| skipped | skip_forward | grey | Gate was skipped |

## Activity Entry Types

| Type | Description |
|:--|:--|
| gate_check | Gate pass/fail event |
| pipeline_run | Pipeline started/completed/aborted |
| component_status_change | Component went ok→degraded or vice versa |
| audit_event | Any audited action |
| seal_change | Contract seal applied or changed |
| system_event | Generic system notification |

## Forbidden Fields

The dashboard contract contains NO:
- buy, sell, order, position
- broker_action, runtime_enable, production_enable
- paper_trading_start, alpha_claim
- Any trading or execution-related fields

## Compliance Verification

- [x] 4 summary cards defined
- [x] 8 component status fields (all Z-SkillOS components)
- [x] 5 gate status indicators with icons and colors
- [x] 6 activity entry types
- [x] No forbidden fields present
- [x] readonly: true enforced
