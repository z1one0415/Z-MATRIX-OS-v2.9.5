from __future__ import annotations
from zmatrix.research_os_rc.schema import DEFAULT_RESEARCH_OS_RC_SAFETY

FULL_BLOCKED = ["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed","auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed","auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed","runtime_injection_allowed","runtime_enabled","external_api_default_on","production_yaml_write_allowed","production_parameter_write_allowed","classifier_production_write_allowed","role_definition_production_write_allowed","legacy_runtime_rewrite_allowed","legacy_module_direct_rewrite_allowed","l2_l3_direct_migration_allowed","legacy_namespace_expansion_allowed"]

def audit_safety_gates(*, reports: dict) -> dict:
    violations = []
    for name,report in (reports or {}).items():
        if not isinstance(report,dict): continue
        for f in FULL_BLOCKED:
            if report.get(f) is True: violations.append({"report":name,"field":f,"value":True})
            s = report.get("safety",{})
            if isinstance(s,dict) and s.get(f) is True: violations.append({"report":name,"field":f"safety.{f}","value":True})
    return {"auditor_version":"V3520_SAFETY_GATE_AUDITOR_V10","checked_report_count":len(reports or {}),"safety_violation_count":len(violations),"violations":violations[:100],"safety_gate_status":"PASS" if not violations else "FAIL","real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_RESEARCH_OS_RC_SAFETY)}
