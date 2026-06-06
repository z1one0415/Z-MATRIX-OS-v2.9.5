# Z-SkillOS Level 3 Allowed Files and Forbidden Paths

## Status

Z_SKILLOS_LEVEL3_ALLOWED_FILES_AND_FORBIDDEN_PATHS_READY

## Allowed Future New Files Only

```
zmatrix/agent/skillos_level3_config.py
zmatrix/agent/skillos_level3_shadow_observer.py
zmatrix/agent/skillos_level3_audit_writer.py
zmatrix/agent/skillos_level3_redaction.py
scripts/skillos/verify_level3_disabled_mode.py
tests/skillos/test_level3_disabled_mode.py
tests/skillos/test_level3_shadow_observer.py
tests/skillos/test_level3_redaction.py
docs/skillos/Z_SKILLOS_LEVEL3_IMPLEMENTATION_CLOSEOUT.md
```

## Allowed Future Modified Files

None by default.

## Files Requiring Separate Approval

`zmatrix/agent/skill_invocation.py`, `zmatrix/agent/skill_result_envelope.py`

## Forbidden Paths

production/, broker_runtime/, real_trade/, runtime_reports/, docs/cases/, V12.x parent files, trading execution paths, broker paths, fail-closed enforcement paths.

## Hard Rule

If invoke_skill or result_envelope modification is proposed → stop and open separate approval gate.
