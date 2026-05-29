# allowlist: forbidden-token-definition
from __future__ import annotations

BLOCKED_FIELDS = [
 "real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed",
 "auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed",
 "auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed",
 "runtime_injection_allowed","runtime_enabled","external_api_default_on",
 "production_yaml_write_allowed","production_parameter_write_allowed",
 "classifier_production_write_allowed","role_definition_production_write_allowed",
 "legacy_runtime_rewrite_allowed","legacy_module_direct_rewrite_allowed",
 "l2_l3_direct_migration_allowed","legacy_namespace_expansion_allowed",
]

def validate_research_os_rc_report(record: dict) -> list[str]:
    errors = []
    if not isinstance(record,dict): return ["record must be dict"]
    for f in BLOCKED_FIELDS:
        if record.get(f) is True: errors.append(f"{f} must be False")
    if record.get("production_strategy_modified") is True: errors.append("production_strategy_modified must be False")
    if record.get("version_ceiling") != "v3.5.20": errors.append("version_ceiling must be v3.5.20")
    if record.get("next_version_allowed") is True: errors.append("next_version_allowed must be False")
    verdict = record.get("rc_verdict",{})
    if verdict.get("production_ready") is True: errors.append("production_ready must be False")
    s = record.get("safety",{})
    if s and not isinstance(s,dict): errors.append("safety must be dict"); return errors
    for f in BLOCKED_FIELDS:
        if isinstance(s,dict) and s.get(f) is True: errors.append(f"safety.{f} must be False")
    return errors

def collect_policy_violations(*, safety_audit: dict, namespace_audit: dict, evidence_audit: dict) -> list[str]:
    violations = []
    if safety_audit.get("safety_gate_status") != "PASS":
        for v in safety_audit.get("violations",[]): violations.append(f"SAFETY:{v.get('report')}:{v.get('field')}")
    if namespace_audit.get("namespace_status") != "PASS":
        violations.append(f"NAMESPACE:new_legacy_count={namespace_audit.get('new_legacy_violation_count')}")
    if evidence_audit.get("evidence_chain_status") != "READY":
        for m in evidence_audit.get("missing",[]): violations.append(f"EVIDENCE:{m}")
    return violations
