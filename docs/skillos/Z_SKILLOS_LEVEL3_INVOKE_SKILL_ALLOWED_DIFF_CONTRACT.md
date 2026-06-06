# Z-SkillOS Level 3 invoke_skill Allowed Diff Contract

## Status

Z_SKILLOS_LEVEL3_INVOKE_SKILL_ALLOWED_DIFF_CONTRACT_READY

## Future Allowed Modified File

`zmatrix/agent/skill_invocation.py` — minimal wrapper call only

## Future Allowed New Files

`tests/skillos/test_level3_invoke_skill_integration.py`, `scripts/skillos/verify_level3_invoke_skill_disabled.py`, closeout, merge readiness.

## Still Forbidden

`skill_result_envelope.py`, production/, broker_runtime/, real_trade/, runtime_reports/, data/, V12.x, tag.

## Allowed Change Shape

Minimal optional call to runtime adapter. No return schema change. No result_envelope change. No caller warnings. No blocking. No fail-closed. No trading/broker side effects. No baseline update.

## Final

Future diff must be minimal with disabled-mode equivalence proof.
