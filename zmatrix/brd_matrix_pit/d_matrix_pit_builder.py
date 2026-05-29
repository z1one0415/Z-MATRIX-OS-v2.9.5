# allowlist: forbidden-token-definition
"""D-Matrix PIT Builder — short event eligibility (conservative, event-data required)"""
from __future__ import annotations
from zmatrix.brd_matrix_pit.schema import DEFAULT_BRD_MATRIX_PIT_SAFETY

def _sf(x,d=0.0):
    try: return float(x) if x is not None else d
    except: return d

def build_d_matrix_pit(*, ticker, replay_date, pit_features, event_snapshot=None):
    if not pit_features or pit_features.get("feature_status")!="READY":
        return {"matrix_version":"D_MATRIX_PIT_V10","status":"FAIL","short_event_eligible":False,
                "event_score":0,"short_momentum_score":0,"risk_score":100,
                "reason_codes":["PRICE_FEATURE_DATA_MISSING"],"event_data_missing":True,
                "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False}
    f = pit_features.get("features",{})
    es = event_snapshot or {}
    r5=_sf(f.get("return_5d"));r20=_sf(f.get("return_20d"))
    vr=_sf(f.get("volume_ratio_20d"),1.0);vol20=_sf(f.get("volatility_20d"))
    has_event = bool(es.get("event_valid"))
    event_score = _sf(es.get("event_score")) if has_event else 0.0
    sms = 0
    if r5>0.03: sms+=35
    if r20>0.05: sms+=25
    if vr>1.5: sms+=30
    if vol20<0.06: sms+=10
    rs = 0
    if vol20>0.08: rs+=40
    if r20>0.25: rs+=40
    if vr>3.0: rs+=20
    eligible = has_event and event_score>=60 and sms>=60 and rs<60
    rc = ["D_MATRIX_EVENT_ELIGIBLE"] if eligible else ["D_MATRIX_NOT_ELIGIBLE"]
    if not has_event: rc.append("EVENT_DATA_MISSING")
    return {"matrix_version":"D_MATRIX_PIT_V10","status":"PASS" if eligible else "FAIL",
            "short_event_eligible":eligible,"event_score":event_score,"short_momentum_score":sms,
            "risk_score":rs,"event_data_missing":not has_event,"reason_codes":rc,
            "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
