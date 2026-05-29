# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def _f(x,d=0.0):
    try: return d if x is None else float(x)
    except: return d

def classify_sector_phase(*, feature: dict) -> dict:
    r20=_f(feature.get("sector_return_20d")); above20=feature.get("sector_above_ma20"); rel=_f(feature.get("sector_relative_strength_vs_market")); vol=_f(feature.get("sector_volatility_20d"))
    if feature.get("data_quality_status")=="INSUFFICIENT_MEMBERS": phase="UNKNOWN_SECTOR_PHASE"
    elif r20<-15: phase="SECTOR_CRASH"
    elif r20>20 and vol>5: phase="SECTOR_CLIMAX"
    elif r20>5 and above20 and rel>0: phase="SECTOR_ADVANCE"
    elif r20<-5 or not above20: phase="SECTOR_RETREAT"
    elif -5<=r20<=5: phase="SECTOR_RANGE"
    else: phase="UNKNOWN_SECTOR_PHASE"
    return {"phase_version":"V3511_SECTOR_PHASE_CLASSIFIER_V10","sector":feature.get("sector"),"trade_date":feature.get("trade_date"),"sector_phase":phase,"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}

def add_sector_phases(*, sector_features: dict) -> dict:
    out={}
    for sector,rows in (sector_features or {}).items():
        enriched=[]
        for f in rows:
            phase=classify_sector_phase(feature=f); r=dict(f); r["sector_phase"]=phase["sector_phase"]; enriched.append(r)
        out[sector]=enriched
    return {"phase_builder_version":"V3511_SECTOR_PHASE_BUILDER_V10","sector_phase_count":len(out),"sector_features_with_phase":out,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
