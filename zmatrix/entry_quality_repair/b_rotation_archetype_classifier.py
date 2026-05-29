# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def _f(x, default=0.0):
    try:
        if x is None: return default
        return float(x)
    except Exception: return default

def classify_b_rotation_archetype(*, features: dict, entry_quality_score: int | None = None) -> dict:
    r20=_f(features.get("return_20d")); dd=_f(features.get("drawdown_from_20d_high")); vol=_f(features.get("volatility_20d")); vr=_f(features.get("volume_ratio_5_20"),1.0)
    above20=features.get("price_above_ma20"); above60=features.get("price_above_ma60")
    if above20 and above60 and 3<=r20<=20 and 0.8<=vr<=2 and vol<=5: archetype="QUALITY_ROTATION"
    elif r20<-10 and dd<-10 and not above60: archetype="DOWNTREND_BOUNCE_TRAP"
    elif vol>5: archetype="HIGH_VOLATILITY_NOISE"
    elif vr<0.8: archetype="LOW_VOLUME_WEAKNESS"
    elif r20>20 and vol>4: archetype="OVEREXTENDED_RIGHT_TAIL"
    else: archetype="UNKNOWN_ENTRY_ARCHETYPE"
    return {"archetype_version":"V355_B_ROTATION_ARCHETYPE_V10","archetype":archetype,"entry_quality_score":entry_quality_score,"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
