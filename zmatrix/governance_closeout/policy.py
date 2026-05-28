from __future__ import annotations
BLOCKED_FIELDS = ["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed","auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed","auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed","runtime_injection_allowed","runtime_enabled","external_api_default_on","production_yaml_write_allowed","production_parameter_write_allowed","z9_auto_calibration_write_allowed","g18_conflict_resolver_write_allowed","o3_conditional_runtime_enabled"]

def validate_governance_closeout_report(record: dict) -> list[str]:
    errors = []
    if not isinstance(record,dict): return ["record must be dict"]
    for f in BLOCKED_FIELDS:
        if record.get(f) is True: errors.append(f"{f} must be False")
    if record.get("production_strategy_modified") is True: errors.append("production_strategy_modified must be False")
    ya = record.get("no_yaml_mutation_audit",{})
    if ya.get("yaml_mutation_detected") is True: errors.append("production yaml/parameter mutation detected")
    fb = record.get("o3_conditional_fallback_plan",{})
    if fb.get("fallback_pool_generation_allowed") is True: errors.append("fallback_pool_generation_allowed must be False")
    s = record.get("safety",{})
    if s and not isinstance(s,dict): errors.append("safety must be dict"); return errors
    for f in BLOCKED_FIELDS:
        if isinstance(s,dict) and s.get(f) is True: errors.append(f"safety.{f} must be False")
    return errors
