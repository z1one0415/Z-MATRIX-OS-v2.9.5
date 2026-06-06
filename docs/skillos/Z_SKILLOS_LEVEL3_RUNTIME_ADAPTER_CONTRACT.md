# Z-SkillOS Level 3 Runtime Adapter Contract

## Status

Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_CONTRACT_READY

## Purpose

Define minimum contract for future Level 3 runtime adapter branch. Does NOT implement.

## Future Branch

`feature/skillos-level3-runtime-adapter-prep`

## Default

SKILLOS_LEVEL3_ENABLED=false

## Future Adapter Requirements

Isolated module. No invoke_skill/result_envelope modification. No runtime blocking/warning. Catches all observer exceptions. Failure returns CONTINUE. No runtime_reports. No production/broker/real_trade. No auto-enable. No fail-closed.

## Future Allowed New Files

`zmatrix/agent/skillos_level3_runtime_adapter.py`, `scripts/skillos/verify_level3_runtime_adapter_disabled.py`, `tests/skillos/test_level3_runtime_adapter.py`, closeout, merge readiness.

## Future Forbidden Modified Files

`skill_invocation.py`, `skill_result_envelope.py`.

## Final

Contract ready. Implementation blocked until separate branch approval.
