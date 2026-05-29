# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def _f(x):
    try:
        if x is None: return None
        return float(x)
    except: return None

def audit_temporal_sector_stability(*, joined_rows: list[dict]) -> dict:
    buckets = {}
    for r in joined_rows or []:
        d = str(r.get("entry_date") or r.get("replay_date",""))
        y = d[:4] if len(d)>=4 else "UNKNOWN"
        key = (y, r.get("sector","UNKNOWN"), r.get("sector_phase","UNKNOWN"))
        buckets.setdefault(key,[]).append(r)
    stable = 0; valid = 0
    for rs in buckets.values():
        if len(rs)<100: continue
        valid += 1
        vals = [_f(x.get("actual_return_t20")) for x in rs]; vals = [x for x in vals if x is not None]
        if not vals: continue
        win = len([x for x in vals if x>0])/len(vals); med = sorted(vals)[len(vals)//2]
        if win>=0.50 and med>0: stable+=1
    status = "TEMPORAL_SECTOR_STABLE" if valid>=3 and stable>=3 else "TEMPORAL_SECTOR_UNSTABLE"
    return {"stability_version":"V3512_TEMPORAL_SECTOR_STABILITY_V10","valid_buckets":valid,"stable_buckets":stable,"temporal_sector_status":status,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
