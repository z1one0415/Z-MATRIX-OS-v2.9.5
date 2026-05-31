"""Physical Signal Quality Checker v1.2 — validate incoming signals"""
def check_signal_quality(signal: dict) -> dict:
    issues = []
    status = "PASS"
    if not signal.get("source_id"):
        issues.append("missing source_id")
        status = "DATA_INSUFFICIENT"
    if not signal.get("evidence_hash"):
        issues.append("missing evidence_hash")
        status = "DATA_INSUFFICIENT"
    if signal.get("external_api_used"):
        issues.append("external_api_used must be false")
        status = "REJECTED"
    if status == "PASS" and not signal.get("source_health_ref"):
        issues.append("missing source_health_ref")
        status = "DEGRADED"
    return {"quality_status": status, "issues": issues}
