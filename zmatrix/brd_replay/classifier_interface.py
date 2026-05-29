# allowlist: forbidden-token-definition
"""Classifier Interface — normalize B/R/D classifier output for v3.2 replay"""
from __future__ import annotations
from typing import Any

VALID_BRD_ROLES = {"A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","UNKNOWN"}
VALID_DECISIONS = {"WATCH_ONLY","VALIDATE","NO_ACTION","D_REJECT","DATA_GAP"}

def _sf(x, d=0.0):
    try: return float(x) if x is not None else d
    except: return d

def normalize_brd_classifier_output(raw):
    raw = raw or {}
    role = raw.get("role") or raw.get("current_role") or raw.get("investment_role") or "UNKNOWN"
    if role not in VALID_BRD_ROLES: role = "UNKNOWN"
    decision = raw.get("decision") or raw.get("action") or "WATCH_ONLY"
    if decision in ("BUY","ENTER","ADD","AUTO_BUY","SELL","CLOSE","AUTO_SELL"): decision = "WATCH_ONLY"
    if decision not in VALID_DECISIONS: decision = "WATCH_ONLY"
    hgp = bool(raw.get("hard_gate_passed") or raw.get("financial_hard_gate_passed") or raw.get("passed") or False)
    if role == "D_REJECT": hgp = False; decision = "D_REJECT"
    return {"role":role,"decision":decision,"role_confidence":_sf(raw.get("role_confidence") or raw.get("confidence")),
            "brd_score":_sf(raw.get("brd_score") or raw.get("score")),
            "hard_gate_passed":hgp,"reason_codes":raw.get("reason_codes",[]),
            "source_raw":raw,"real_trade_allowed":False,"broker_order_allowed":False}
