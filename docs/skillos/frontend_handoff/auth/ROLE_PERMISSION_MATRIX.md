# Z-SkillOS Frontend Handoff — Role-Permission Matrix

> Version: 1.0.0 | Auth: A4 Agent | 2026-06-12

## Overview

6 roles × 16 permissions authorization matrix for the Z-SkillOS frontend handoff release candidate.
All dangerous permissions default to `FALSE` for all roles.

## Roles

| # | Role | Description |
|---|------|-------------|
| 1 | **viewer** | Read-only access to dashboards, reports, and evidence chains |
| 2 | **analyst** | Viewer + ability to acknowledge risks |
| 3 | **reviewer** | Analyst + ability to approve planning gates and interpretation reviews |
| 4 | **approver** | Reviewer + ability to approve promotion eligibility reviews |
| 5 | **admin** | All non-dangerous permissions; no dangerous actions without OOB approval |
| 6 | **system_auditor** | View-all-only; no write/approve/execute permissions |

## Permissions

### View Permissions (6)

| Permission | Description |
|------------|-------------|
| `can_view_dashboard` | Access the main dashboard view |
| `can_view_factor_library` | Browse factor library contents |
| `can_view_reports` | Read generated reports |
| `can_view_reviews` | Read review records |
| `can_view_evidence_chain` | Inspect evidence chain data |
| `can_view_gate_state` | View gate state transitions |

### Action Permissions (4)

| Permission | Description |
|------------|-------------|
| `can_acknowledge_risk` | Acknowledge and sign off on risk items |
| `can_approve_planning_gate` | Approve planning gate transitions |
| `can_approve_interpretation_review` | Approve interpretation review outcomes |
| `can_approve_promotion_eligibility_review` | Approve promotion eligibility reviews |

### Dangerous Permissions (5) — ALWAYS FALSE

| Permission | Description |
|------------|-------------|
| `can_enable_runtime` | Enable production runtime |
| `can_enable_runner` | Enable production runner |
| `can_enable_paper_trading` | Enable paper trading mode |
| `can_enable_broker` | Enable broker connection |
| `can_enable_production` | Enable full production mode |

## Full Matrix

| Permission | viewer | analyst | reviewer | approver | admin | sys_auditor |
|------------|:------:|:-------:|:--------:|:--------:|:-----:|:-----------:|
| can_view_dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_view_factor_library | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_view_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_view_reviews | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_view_evidence_chain | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_view_gate_state | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| can_acknowledge_risk | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| can_approve_planning_gate | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| can_approve_interpretation_review | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| can_approve_promotion_eligibility_review | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| can_enable_runtime | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| can_enable_runner | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| can_enable_paper_trading | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| can_enable_broker | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| can_enable_production | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Design Principles

1. **Least Privilege**: Each role gets only the permissions strictly required for its function.
2. **Dangerous-by-Default**: All production/execution capabilities default to `false`.
3. **Out-of-Band Escalation**: Enabling dangerous permissions requires a signed incident ticket with two admin signatures.
4. **Progressive Trust**: Roles form a strict inheritance chain: viewer ⊂ analyst ⊂ reviewer ⊂ approver ⊂ admin.
