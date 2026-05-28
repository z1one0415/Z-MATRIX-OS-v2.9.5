from __future__ import annotations
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

def _f(x,d=0.0):
    try:
        if x is None: return d
        return float(x)
    except: return d

def classify_sector_phase(*, features: dict) -> dict:
    r20 = _f(features.get("sector_return_20d")); above20 = features.get("sector_above_ma20"); rel = _f(features.get("sector_relative_strength_vs_market")); vol = _f(features.get("sector_volatility_20d"))
    if features.get("feature_status")!="READY": phase = "UNKNOWN_SECTOR_PHASE"
    elif r20<-15: phase = "SECTOR_CRASH"
    elif r20>20 and vol>5: phase = "SECTOR_CLIMAX"
    elif r20>5 and above20 is True and rel>0: phase = "SECTOR_ADVANCE"
    elif r20<-5 or above20 is False: phase = "SECTOR_RETREAT"
    elif -5<=r20<=5: phase = "SECTOR_RANGE"
    else: phase = "UNKNOWN_SECTOR_PHASE"
    return {"phase_version":"V359_SECTOR_PHASE_V10","sector_phase":phase,"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
