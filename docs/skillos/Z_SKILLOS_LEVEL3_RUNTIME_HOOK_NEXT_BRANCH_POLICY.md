# Z-SkillOS Level 3 Runtime Hook Next Branch Policy

## Status

Z_SKILLOS_LEVEL3_RUNTIME_HOOK_NEXT_BRANCH_POLICY_READY

## Next Legal Branch

`feature/skillos-level3-runtime-adapter-prep`

## May Add

adapter module, disabled verifier, adapter tests, closeout, merge readiness.

## May Not Modify

invoke_skill, result_envelope, production/, broker_runtime/, real_trade/, runtime_reports/, data/, V12.x parent files.

## Required Behavior

Disabled: zero side effects. Enabled: CONTINUE. No result_envelope mutation. No blocking. No warning. No production/broker/real_trade.

## Final

Adapter prep only. No direct invoke_skill hook.
