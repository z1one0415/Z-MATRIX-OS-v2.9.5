"""R-Matrix PIT Builder — cycle/momentum from PIT features"""
from __future__ import annotations
from zmatrix.brd_matrix_pit.schema import DEFAULT_BRD_MATRIX_PIT_SAFETY

def _sf(x,d=0.0):
    try: return float(x) if x is not None else d
    except: return d

def infer_sector_phase(f):
    r20=_sf(f.get("return_20d"));r60=_sf(f.get("return_60d"))
    a20=f.get("above_ma20");a60=f.get("above_ma60")
    vol20=_sf(f.get("volatility_20d"));vr=_sf(f.get("volume_ratio_20d"),1.0)
    if r20>0.12 and r60>0.20 and vr>1.5: return "高潮"
    if r20>0.06 and r60>0.10 and a20 and a60: return "主升"
    if r20>0.03 and a20: return "确认"
    if r20>0 and vr>1.2: return "点火"
    if r20<-0.05 and r60<0: return "退潮"
    if vol20>0.04: return "分歧"
    return "UNKNOWN"

def build_r_matrix_pit(*, ticker, replay_date, pit_features):
    if not pit_features or pit_features.get("feature_status")!="READY":
        return {"matrix_version":"R_MATRIX_PIT_V10","status":"FAIL","r_action_cap":"WAIT",
                "cycle_score":0,"momentum_score":0,"trend_score":0,"sector_phase":"UNKNOWN",
                "reason_codes":["PRICE_FEATURE_DATA_MISSING"],
                "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False}
    f = pit_features.get("features",{})
    r20=_sf(f.get("return_20d"));r60=_sf(f.get("return_60d"))
    a20=bool(f.get("above_ma20"));a60=bool(f.get("above_ma60"));a120=bool(f.get("above_ma120"))
    vr=_sf(f.get("volume_ratio_20d"),1.0);vol60=_sf(f.get("volatility_60d"))
    ms=0
    if r20>0:ms+=25
    if r20>0.05:ms+=25
    if r60>0.08:ms+=25
    if vr>1.1:ms+=25
    ts=0
    if a20:ts+=35
    if a60:ts+=35
    if a120:ts+=30
    cs=int(ms*0.55+ts*0.45)
    phase=infer_sector_phase(f)
    blocked=vol60>0.08 or phase in ("退潮",)
    passed=cs>=55 and not blocked
    rc = ["R_MATRIX_ROTATION_ELIGIBLE"] if passed else (["R_MATRIX_RISK_BLOCKED"] if blocked else ["R_MATRIX_WAIT"])
    return {"matrix_version":"R_MATRIX_PIT_V10","status":"PASS" if passed else "FAIL",
            "r_action_cap":"PAPER_TRACK" if passed else "WAIT",
            "cycle_score":cs,"momentum_score":ms,"trend_score":ts,"sector_phase":phase,
            "reason_codes":rc,"safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
