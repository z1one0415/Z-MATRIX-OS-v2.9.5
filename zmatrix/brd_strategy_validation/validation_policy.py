"""Validation Policy — 13 blocked fields + status validation"""
from __future__ import annotations
_BLOCKED = ["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed",
    "auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed",
    "auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed",
    "runtime_injection_allowed","runtime_enabled","external_api_default_on"]

def validate_v35_report_safety(record):
    e=[]
    if not isinstance(record,dict): return ["record must be dict"]
    for f in _BLOCKED:
        if record.get(f) is True: e.append(f"{f} must be False")
    s=record.get("safety",{}); s={} if s is None else s
    if not isinstance(s,dict): e.append("safety must be dict"); s={}
    for f in _BLOCKED:
        if s.get(f) is True: e.append(f"safety.{f} must be False")
    return e

def validate_v35_validation_status(report):
    e=[]
    if report.get("validation_status")=="STRATEGY_VALIDATION_REPORT_READY":
        if not report.get("brd_connected"): e.append("cannot be ready when brd_connected=False")
        if report.get("fallback_rate") is not None and report["fallback_rate"]>=0.05: e.append("cannot be ready when fallback_rate>=5%")
        if report.get("metrics",{}).get("valid_outcome_count",0)<=0: e.append("cannot be ready without valid outcomes")
    return e
