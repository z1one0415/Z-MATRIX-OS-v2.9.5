# Z-SkillOS Level 3 Telemetry Redaction Contract

## Status

Z_SKILLOS_LEVEL3_TELEMETRY_REDACTION_CONTRACT_READY

## Allowed Telemetry

skill_id, contract_id, schema_validation_result, input_hash, output_hash, golden_match_status, semantic_drift_status, runtime_duration_bucket, non_sensitive_error_category.

## Forbidden Telemetry

Raw user prompt, raw private user data, broker/trading credentials, account identifiers, production secrets, real_trade execution data, uncontrolled payload dumps, PII.

## Redaction Rules

Redact before persist. Hash before persist where possible. Reject unknown fields by default. No raw prompt/output/secrets persistence. No broker/real_trade identifiers.

## Required Future Tests

test_redaction_rejects_raw_prompt/user_data/credentials/unknown_fields. test_redaction_allows_only_contract_fields. test_redaction_before_write.

## Final

Telemetry redaction contract ready. No implementation in this gate.
