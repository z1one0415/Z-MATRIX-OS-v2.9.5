from __future__ import annotations
from statistics import median
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY, POOL_RESILIENCE_THRESHOLDS

def _ed(r): return str(r.get("entry_date") or r.get("replay_date") or "UNKNOWN")

def validate_candidate_pool_resilience(*, policy_results: dict) -> dict:
    th = POOL_RESILIENCE_THRESHOLDS; results = {}
    for pn, policy in (policy_results or {}).items():
        kept_rows = policy.get("kept_rows") or policy.get("kept") or []
        orig = policy.get("original_count") or policy.get("input_count") or 0
        kept_count = policy.get("kept_count") or len(kept_rows)
        kr = kept_count/orig if orig else None
        by_day = {}
        for row in kept_rows:
            d = _ed(row); by_day[d] = by_day.get(d,0)+1
        counts = list(by_day.values()); dc = len(by_day)
        small = sum(1 for x in counts if x<th["min_daily_pool_size"])
        sr = small/dc if dc else None
        reasons = []
        if kr is not None and kr<th["min_kept_rate_hard"]: reasons.append("KEPT_RATE_BELOW_HARD_MIN")
        elif kr is not None and kr<th["min_kept_rate_preferred"]: reasons.append("CONCENTRATED_POLICY_RISK")
        if sr is not None and sr>th["max_small_pool_day_rate"]: reasons.append("POOL_THIN_RISK")
        status = "POOL_RESILIENCE_BLOCKED" if "KEPT_RATE_BELOW_HARD_MIN" in reasons else "POOL_RESILIENCE_WARNING" if reasons else "POOL_RESILIENCE_PASS"
        results[pn] = {"policy_name":pn,"original_count":orig,"kept_count":kept_count,"kept_rate":kr,"daily_pool_stats":{"day_count":dc,"zero_pool_days":0,"zero_pool_day_rate":None,"small_pool_days":small,"small_pool_day_rate":sr,"min_daily_pool":min(counts) if counts else 0,"median_daily_pool":median(counts) if counts else 0},"pool_resilience_status":status,"reasons":reasons,"real_trade_allowed":False,"broker_order_allowed":False}
    return {"validator_version":"V357_CANDIDATE_POOL_RESILIENCE_V10","policy_pool_results":results,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
