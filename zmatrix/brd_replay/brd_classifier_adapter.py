# allowlist: forbidden-token-definition
"""BRD Classifier Adapter v3.3 — default to real connector, no fake connections"""
from __future__ import annotations
from typing import Any

def _safe_float(x, default=0.0):
    try: return float(x) if x is not None else default
    except: return default

def _fallback_brd_not_connected(*, ticker, replay_date, reason="BRD_NOT_CONNECTED"):
    return {"classifier_version":"BRD_CLASSIFIER_ADAPTER_V11","mode":"HISTORICAL_REPLAY_ONLY",
            "ticker":ticker,"replay_date":replay_date,"role":"UNKNOWN","role_confidence":0.0,
            "brd_score":0.0,"hard_gate_passed":False,"decision":"WATCH_ONLY",
            "fallback":True,"fallback_reason":reason,"brd_connected":False,
            "real_trade_allowed":False,"broker_order_allowed":False}

def run_brd_classifier_adapter(*, ticker, replay_date, pit_features, classifier=None):
    if not pit_features or pit_features.get("feature_status") != "READY":
        return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,reason="DATA_GAP")
    active = classifier
    if active is None:
        from zmatrix.brd_replay.real_brd_connector import build_real_brd_classifier_connector
        active = build_real_brd_classifier_connector()
    try:
        if callable(active): raw = active(pit_features)
        elif hasattr(active,"classify"): raw = active.classify(pit_features)
        else: return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,reason="INVALID_INTERFACE")
        from zmatrix.brd_replay.classifier_interface import normalize_brd_classifier_output
        n = normalize_brd_classifier_output(raw)
        bcd = bool(raw.get("brd_connected")) or raw.get("connector_status")=="CONNECTED"
        if not bcd: return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,
            reason=raw.get("fallback_reason","BRD_NOT_CONNECTED"))
        n.update({"classifier_version":"BRD_CLASSIFIER_ADAPTER_V11","mode":"HISTORICAL_REPLAY_ONLY",
            "ticker":ticker,"replay_date":replay_date,"fallback":False,"brd_connected":True})
        return n
    except Exception as e:
        return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,reason=f"CLASSIFIER_ERROR:{str(e)[:80]}")
