# Z-SkillOS Frontend Handoff — Blocked Action Policy

> Version: 1.0.0 | Auth: A4 Agent | 2026-06-12

## Overview

This policy defines actions that are **always blocked** regardless of role permissions.
No role — not even `admin` — can execute these actions through normal frontend flows.

## Blocked Actions

| # | Action | Reason |
|---|--------|--------|
| 1 | `enable_runtime` | Production runtime enablement carries catastrophic blast-radius risk |
| 2 | `enable_runner` | Production runner enablement carries catastrophic blast-radius risk |
| 3 | `enable_paper_trading` | Paper trading enablement bypasses risk controls |
| 4 | `enable_broker` | Broker enablement creates real financial exposure |
| 5 | `enable_production` | Production enablement carries maximum blast-radius risk |

## Enforcement

All 5 blocked actions:
- Map to the 5 dangerous permissions in the role-permission matrix
- Are set to `false` for all 6 roles
- The frontend **MUST NOT** render UI controls for blocked actions when `check_permission() == false`
- The backend **MUST** reject any API call for a blocked action with HTTP 403

## Override Mechanism

In the event of a **production incident** requiring a blocked action:

1. File a production incident ticket
2. Obtain signatures from **two independent admin-role holders**
3. The system operator executes the action via a secure out-of-band channel
4. All override events are logged immutably to the audit trail

### Override Requirements

| Requirement | Value |
|-------------|-------|
| Ticket Type | Production Incident |
| Approvals | 2 admin signatures (independent) |
| Audit Trail | Immutable log entry |
| Expiry | Single-use, time-boxed (max 1 hour) |

## Security Posture

- **Default-Deny**: All dangerous actions require explicit out-of-band approval
- **No Frontend Bypass**: UI controls for blocked actions are never rendered
- **No API Bypass**: Backend enforces the same matrix independently
- **Immutable Audit**: Every blocked-action attempt is logged regardless of role
