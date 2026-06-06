# Z-SkillOS Level 3 Audit Retention Test Requirements

## Status

Z_SKILLOS_LEVEL3_AUDIT_RETENTION_TEST_REQUIREMENTS_READY

## Required Future Tests

**Dry-run:** deletes_nothing, reports_eligible, ignores_forbidden.

**Apply:** deletes_scoped_only, respects_retention_days/max_files/max_bytes, deterministic_summary.

**Path safety:** refuses runtime_reports/production/broker/real_trade/data/docs/zmatrix. Refuses parent_traversal/symlink_escape.

**Privacy:** report_no_raw_prompt/user_data/credentials/broker_ids.

**Regression:** level3_disabled_mode, evidence, long_run still pass.

## Required Verify

verify CLI, pytest cleanup/safety.

## Final

No retention implementation may merge without this proof set.
