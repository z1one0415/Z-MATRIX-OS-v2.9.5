# Z-SkillOS Level 3 Audit Lifecycle Policy

## Status

Z_SKILLOS_LEVEL3_AUDIT_LIFECYCLE_POLICY_READY

## States

CREATED → VALIDATED (schema) → RETAINED (bounded) → EXPIRED (eligible for cleanup) → CLEANED (scoped delete). REJECTED (forbidden/invalid). QUARANTINE: not approved.

## Rules

Schema-validated before write. Invalid rejected. Retained bounded. Expired cleaned explicitly. Dry-run capable. No lifecycle affects runtime. No caller warnings. No blocking. No production/broker/real_trade.

## Final

Policy only. No implementation.
