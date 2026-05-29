# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_sector_attribution.joint_segment_profiler import _stats
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def analyze_range_bound_drag(*, joined_rows: list[dict]) -> dict:
    rows = [r for r in joined_rows or [] if r.get("market_regime")=="RANGE_BOUND"]
    by_phase = {}
    for r in rows: by_phase.setdefault(r.get("sector_phase","UNKNOWN"),[]).append(r)
    by_sector = {}
    for r in rows: by_sector.setdefault(r.get("sector","UNKNOWN"),[]).append(r)
    sp = {k:_stats(v) for k,v in by_sector.items()}; pp = {k:_stats(v) for k,v in by_phase.items()}
    best = sorted(sp.items(),key=lambda kv:(kv[1].get("median") is not None, kv[1].get("median") or -999),reverse=True)[:10]
    worst = sorted(sp.items(),key=lambda kv:(kv[1].get("median") is None, kv[1].get("median") or 999))[:10]
    return {"analyzer_version":"V3512_RANGE_BOUND_ANALYZER_V10","range_bound_count":len(rows),"range_bound_by_sector_phase":pp,"range_bound_best_sectors":best,"range_bound_worst_sectors":worst,"secondary_filter_required":True,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
