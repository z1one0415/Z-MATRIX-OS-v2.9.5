# Z-SkillOS Level 3 Audit Cleanup Policy

## Status

Z_SKILLOS_LEVEL3_AUDIT_CLEANUP_POLICY_READY

## Principles

Explicit cleanup. Path-scoped. Never production/broker/real_trade. Never runtime_reports (unless approved). Never source/docs/data/tests/configs. Dry-run mode. Test-covered.

## Future Allowed Path

`runtime_audit/skillos_level3_shadow/`

## Forbidden Paths

runtime_reports, production, broker_runtime, real_trade, data, docs, zmatrix, scripts, tests.

## Required Future Commands

`cleanup_level3_audit_retention.py --dry-run` and `--apply`.

## Required Future Tests

Dry-run deletes nothing. Apply scoped. Refuses forbidden paths. Respects retention days/file count/total bytes.

## Final

Policy only. No implementation.
