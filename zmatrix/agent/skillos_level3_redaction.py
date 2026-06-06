"""Telemetry redaction for SkillOS Level 3. Default deny for unknown/forbidden fields."""

ALLOWED_TELEMETRY_FIELDS = {
    "event_id", "skill_id", "contract_id",
    "schema_validation_result", "input_hash", "output_hash",
    "golden_match_status", "semantic_drift_status",
    "runtime_duration_bucket", "non_sensitive_error_category",
    "created_by",
}

FORBIDDEN_TELEMETRY_FIELDS = {
    "raw_prompt", "raw_user_data", "raw_output_payload",
    "account_id", "broker_id", "trading_credentials",
    "production_secret", "real_trade_payload",
    "personally_identifying_data",
}


def redact_telemetry(payload: dict) -> dict:
    """Redact telemetry payload. Rejects forbidden and unknown fields. Returns allowlisted subset."""
    result = {}
    for key, value in payload.items():
        if key in FORBIDDEN_TELEMETRY_FIELDS:
            raise ValueError(f"forbidden telemetry field: {key}")
        if key not in ALLOWED_TELEMETRY_FIELDS:
            raise ValueError(f"unknown telemetry field: {key}")
        result[key] = value
    return result
