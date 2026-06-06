# Z-SkillOS Level 3 invoke_skill Touch Policy

## Status

Z_SKILLOS_LEVEL3_INVOKE_SKILL_TOUCH_POLICY_READY

## Current Policy

invoke_skill remains untouched.

## Rule

No Level 3 branch may modify invoke_skill unless separate explicit approval gate.

## Approved Near-Term Path

isolated observer → audit writer → runtime adapter → adapter tests → adapter merge → only then invoke_skill integration gate

## Future invoke_skill Gate Must Prove

Disabled zero side effects. Enabled never blocks. Observer failure never fails runtime. result_envelope unchanged. No caller warning. production/broker/real_trade blocked. Rollback exists. Human approval recorded.

## Explicit Rejection

Direct hook. Hook without adapter. Hidden hook. Auto-enable. Fail-closed.

## Final

invoke_skill modification remains forbidden.
