"""BRD Replay Policy — 13 blocked fields"""
from __future__ import annotations
_BLOCKED = ["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed",
    "auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed",
    "auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed",
    "runtime_injection_allowed","runtime_enabled","external_api_default_on"]

def assert_no_brd_replay_runtime_effects(record):
    v = []
    if not isinstance(record,dict): return ["record must be dict"]
    for f in _BLOCKED:
        if record.get(f) is True: v.append(f"{f} must be False")
    s = record.get("safety",{})
    if s is None: s = {}
    if not isinstance(s,dict): v.append("safety must be dict"); s = {}
    for f in _BLOCKED:
        if s.get(f) is True: v.append(f"safety.{f} must be False")
    return v
