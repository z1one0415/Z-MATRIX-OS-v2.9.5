# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def _f(x, default=0.0):
    try:
        if x is None: return default
        return float(x)
    except Exception: return default

def score_entry_quality(*, features: dict) -> dict:
    score=50; reasons=[]
    if features.get("price_above_ma20") is True: score+=10; reasons.append("ABOVE_MA20")
    else: score-=8; reasons.append("BELOW_MA20")
    if features.get("price_above_ma60") is True: score+=12; reasons.append("ABOVE_MA60")
    else: score-=12; reasons.append("BELOW_MA60")
    r20=_f(features.get("return_20d"))
    if r20<-10: score-=15; reasons.append("RET20_DOWNTREND")
    elif r20>20: score-=8; reasons.append("RET20_OVEREXTENDED")
    elif 3<=r20<=15: score+=10; reasons.append("RET20_HEALTHY_MOMENTUM")
    dd=_f(features.get("drawdown_from_20d_high"))
    if dd<-15: score-=10; reasons.append("DEEP_20D_DRAWDOWN")
    elif dd>-5: score+=5; reasons.append("NEAR_20D_HIGH")
    vol=_f(features.get("volatility_20d"))
    if vol>5: score-=10; reasons.append("HIGH_VOLATILITY")
    elif 1<=vol<=4: score+=5; reasons.append("NORMAL_VOLATILITY")
    vr=features.get("volume_ratio_5_20")
    if vr is not None:
        vr=_f(vr)
        if vr<0.8: score-=8; reasons.append("WEAK_VOLUME")
        elif 0.8<=vr<=2: score+=5; reasons.append("HEALTHY_VOLUME")
    score=max(0,min(100,score))
    bucket="HIGH_ENTRY_QUALITY" if score>=65 else "MID_ENTRY_QUALITY" if score>=45 else "LOW_ENTRY_QUALITY"
    return {"score_version":"V355_ENTRY_QUALITY_SCORE_V10","entry_quality_score":score,"entry_quality_bucket":bucket,"reason_codes":reasons,"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
