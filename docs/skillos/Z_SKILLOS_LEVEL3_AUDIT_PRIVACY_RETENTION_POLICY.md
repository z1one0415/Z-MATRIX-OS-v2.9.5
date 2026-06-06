# Z-SkillOS Level 3 Audit Privacy Retention Policy

## Status

Z_SKILLOS_LEVEL3_AUDIT_PRIVACY_RETENTION_POLICY_READY

## Allowed Retained

event_id, skill_id, contract_id, schema_validation_result, input_hash, output_hash, golden_match_status, semantic_drift_status, runtime_duration_bucket, non_sensitive_error_category, created_by.

## Forbidden Retained

raw_prompt, raw_user_data, raw_output_payload, account_id, broker_id, trading_credentials, production_secret, real_trade_payload, PII.

## Rules

No raw prompt/user/credentials/identifiers/secrets/trade payloads. Unknown rejected. Allowlist before write. Cleanup can't expose deleted content.

## Required Future Tests

Forbidden rejected before write. Retained file allowlist only. Cleanup no forbid copy. Report excludes raw.

## Final

Policy ready. No implementation.
