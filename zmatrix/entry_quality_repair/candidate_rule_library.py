from __future__ import annotations
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

ENTRY_REPAIR_CANDIDATES = {"keep_high_entry_quality":{"description":"Keep only samples with entry_quality_score >= 65.","lookahead_risk":False,"production_ready":False},"exclude_low_entry_quality":{"description":"Exclude samples with entry_quality_score < 45.","lookahead_risk":False,"production_ready":False},"exclude_downtrend_bounce_trap":{"description":"Exclude DOWNTREND_BOUNCE_TRAP archetype.","lookahead_risk":False,"production_ready":False},"exclude_high_volatility_noise":{"description":"Exclude HIGH_VOLATILITY_NOISE archetype.","lookahead_risk":False,"production_ready":False},"require_above_ma60":{"description":"Require price_above_ma60=True.","lookahead_risk":False,"production_ready":False},"require_healthy_volume":{"description":"Require volume_ratio_5_20 >= 0.8.","lookahead_risk":False,"production_ready":False},"quality_rotation_only":{"description":"Keep only QUALITY_ROTATION archetype.","lookahead_risk":False,"production_ready":False}}

def apply_entry_candidate_rule(*, enriched_rows: list[dict], rule_name: str) -> dict:
    rule = ENTRY_REPAIR_CANDIDATES[rule_name]; kept = []
    for row in enriched_rows or []:
        f = row.get("entry_features",{}); score = row.get("entry_quality_score"); arch = row.get("entry_archetype")
        keep = True
        if rule_name=="keep_high_entry_quality": keep = score is not None and score>=65
        elif rule_name=="exclude_low_entry_quality": keep = score is None or score>=45
        elif rule_name=="exclude_downtrend_bounce_trap": keep = arch!="DOWNTREND_BOUNCE_TRAP"
        elif rule_name=="exclude_high_volatility_noise": keep = arch!="HIGH_VOLATILITY_NOISE"
        elif rule_name=="require_above_ma60": keep = f.get("price_above_ma60") is True
        elif rule_name=="require_healthy_volume": vr=f.get("volume_ratio_5_20"); keep = vr is not None and float(vr)>=0.8
        elif rule_name=="quality_rotation_only": keep = arch=="QUALITY_ROTATION"
        if keep: kept.append(row)
    return {"rule_name":rule_name,"rule":rule,"original_count":len(enriched_rows or []),"kept_count":len(kept),"kept_rate":len(kept)/len(enriched_rows) if enriched_rows else None,"kept":kept,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
