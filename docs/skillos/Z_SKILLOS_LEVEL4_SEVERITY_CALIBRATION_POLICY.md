# Z-SkillOS Level 4 Severity Calibration Policy

## Status

Z_SKILLOS_LEVEL4_SEVERITY_CALIBRATION_POLICY_READY

## Allowed

INFO (info), NOTICE (low-risk), WARN (review), ESCALATE_REVIEW (human).

## Forbidden

BLOCK, FAIL_CLOSED, TRADE/BROKER/REAL_TRADE_BLOCK, HARD_STOP, AUTO_REJECT.

## Required Inputs

True/false-positive examples, repeated-run/retention/lifecycle evidence, human review threshold, downgrade/rollback rules.

## Rules

No result change. No envelope mutation. No blocking. No broker/real_trade behavior. Downgradeable. Auditable. Rollback-safe.
