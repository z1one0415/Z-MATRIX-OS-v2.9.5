"""BRD Classifier Adapter v3.2 — connect PIT features to B/R/D or mark BRD_NOT_CONNECTED"""
from __future__ import annotations
from typing import Any

def _safe_float(x, default=0.0):
    try: return float(x) if x is not None else default
    except: return default

def _fallback_brd_not_connected(*, ticker, replay_date, reason="BRD_NOT_CONNECTED"):
    return {"classifier_version":"BRD_CLASSIFIER_ADAPTER_V10","mode":"HISTORICAL_REPLAY_ONLY",
            "ticker":ticker,"replay_date":replay_date,"role":"UNKNOWN","role_confidence":0.0,
            "brd_score":0.0,"hard_gate_passed":False,"decision":"WATCH_ONLY",
            "fallback":True,"fallback_reason":reason,"brd_connected":False,
            "safety":{}, "real_trade_allowed":False,"broker_order_allowed":False}

def run_brd_classifier_adapter(*, ticker, replay_date, pit_features, classifier=None):
    if not pit_features or pit_features.get("feature_status") != "READY":
        return _fallback_brd_not_connected(ticker=ticker, replay_date=replay_date, reason="DATA_GAP")
    if classifier is None:
        return _fallback_brd_not_connected(ticker=ticker, replay_date=replay_date)
    try:
        if callable(classifier): raw = classifier(pit_features)
        elif hasattr(classifier,"classify"): raw = classifier.classify(pit_features)
        else: return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,reason="INVALID_CLASSIFIER_INTERFACE")
        role = raw.get("role","UNKNOWN")
        decision = raw.get("decision","WATCH_ONLY")
        if decision in ("BUY","ENTER","ADD","AUTO_BUY"): decision = "WATCH_ONLY"
        return {"classifier_version":"BRD_CLASSIFIER_ADAPTER_V10","mode":"HISTORICAL_REPLAY_ONLY",
                "ticker":ticker,"replay_date":replay_date,"role":role,
                "role_confidence":_safe_float(raw.get("role_confidence")),
                "brd_score":_safe_float(raw.get("brd_score")),
                "hard_gate_passed":bool(raw.get("hard_gate_passed",False)),
                "decision":decision,"fallback":False,"fallback_reason":"","brd_connected":True,
                "real_trade_allowed":False,"broker_order_allowed":False}
    except Exception as e:
        return _fallback_brd_not_connected(ticker=ticker,replay_date=replay_date,reason=f"CLASSIFIER_ERROR:{str(e)[:80]}")
