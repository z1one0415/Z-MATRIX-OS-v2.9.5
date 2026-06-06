# Z-SkillOS v1.3 Telemetry Privacy Boundary Spec

## Status

Z_SKILLOS_V1_3_TELEMETRY_PRIVACY_BOUNDARY_SPEC_READY

## Allowed Telemetry

skill_id, contract_id, schema_validation_result, input_hash, output_hash, golden_match_status, semantic_drift_status, runtime_duration_bucket, non-sensitive error category.

## Forbidden Telemetry

Raw user prompt, raw private user data, broker/trading credentials, account identifiers, production secrets, real_trade execution data, uncontrolled payload dumps, PII.

## Privacy Rules

Hash before persist. Redact before write. No raw prompt. No account/broker/trading identifiers. No export outside approved audit path.

## Required Future Tests

Forbidden fields rejected. Redaction before write. No raw prompt/secrets/broker identifiers persisted.

## Final

Specified, not implemented.
