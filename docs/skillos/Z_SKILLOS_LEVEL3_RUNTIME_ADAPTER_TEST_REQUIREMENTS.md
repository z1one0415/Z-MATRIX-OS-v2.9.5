# Z-SkillOS Level 3 Runtime Adapter Test Requirements

## Status

Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_TEST_REQUIREMENTS_READY

## Required Future Tests

**Disabled mode:** default_disabled, no_shadow_call, no_files, no_runtime_reports, no_result_envelope_mutation, no_blocking, no_caller_warning.

**Enabled mode:** calls shadow observer, returns CONTINUE, no_result_envelope_mutation, no_blocking, no_warning, tmp audit path only.

**Failure isolation:** handles observer/writer/redaction exceptions, all return CONTINUE.

**Boundary:** no_invoke_skill_import, no_result_envelope_import, no_production_broker_real_trade.

## Required Future Verify

`python3 scripts/skillos/verify_level3_runtime_adapter_disabled.py` → `Z_SKILLOS_LEVEL3_RUNTIME_ADAPTER_DISABLED_VERIFY_PASS`

## Final

Runtime adapter cannot merge without these tests.
