# allowlist: forbidden-token-definition
from __future__ import annotations
from collections import Counter
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY, POOL_STUDY_THRESHOLDS

def _sf(x,d=None):
    try:
        if x is None: return d
        return float(x)
    except: return d

def deep_dive_pool_resilience(*, replay_report: dict, governance_report: dict) -> dict:
    pr = replay_report.get("policy_results") or replay_report.get("candidate_results") or {}
    gp = governance_report.get("candidate_pool_resilience",{}).get("policy_pool_results",{})
    results = {}
    for name, policy in pr.items():
        kept = policy.get("kept_rows") or policy.get("kept") or []
        dg = policy.get("downgraded_rows") or policy.get("downgraded") or []
        tickers = [r.get("ticker") for r in kept if r.get("ticker")]
        tc = Counter(tickers)
        sectors = [r.get("sector") or r.get("industry") for r in kept if r.get("sector") or r.get("industry")]
        sc = Counter(sectors)
        kc = len(kept)
        tts = max(tc.values())/kc if kc and tc else None
        tss = max(sc.values())/kc if kc and sc else None
        gov = gp.get(name,{}); kr = gov.get("kept_rate") or policy.get("kept_rate")
        reasons = []
        if kr is not None and kr < POOL_STUDY_THRESHOLDS["min_kept_rate_preferred"]: reasons.append("CONCENTRATED_POLICY_RISK")
        if tts is not None and tts > POOL_STUDY_THRESHOLDS["max_concentration_single_ticker"]: reasons.append("TICKER_CONCENTRATION_RISK")
        if tss is not None and tss > POOL_STUDY_THRESHOLDS["max_concentration_single_sector"]: reasons.append("SECTOR_CONCENTRATION_RISK")
        pos_dg = [r for r in dg if _sf(r.get("actual_return_t20"),0) > 0]
        results[name] = {"policy_name":name,"kept_count":kc,"kept_rate":kr,"daily_pool_stats":gov.get("daily_pool_stats",{}),"top_ticker_share":tts,"top_tickers":tc.most_common(10),"top_sector_share":tss,"top_sectors":sc.most_common(10),"sector_concentration_status":"READY" if sc else "DATA_INSUFFICIENT","opportunity_loss_summary":{"downgraded_count":len(dg),"downgraded_positive_count":len(pos_dg),"downgraded_positive_rate":len(pos_dg)/len(dg) if dg else None},"pool_resilience_deep_status":"POOL_RESILIENCE_WARNING" if reasons else "POOL_RESILIENCE_PASS","reasons":reasons,"real_trade_allowed":False,"broker_order_allowed":False}
    return {"deep_dive_version":"V358_POOL_RESILIENCE_DEEP_DIVE_V10","policy_pool_deep_results":results,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
