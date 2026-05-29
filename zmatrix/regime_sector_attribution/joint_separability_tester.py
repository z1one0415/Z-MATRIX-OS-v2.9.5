# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY, JOINT_THRESHOLDS

def _perf_score(profiles):
    p = profiles.get("profiles",{}).get("market_regime_x_sector_phase",{})
    vals = [v for v in p.values() if (v.get("count") or 0)>=1000 and v.get("median") is not None]
    if len(vals)<2: return 0.0
    meds = [v["median"] for v in vals]
    return max(0.0,min(1.0,(max(meds)-min(meds))/3.0))

def _conc_score(audit):
    warnings = 1 if audit.get("concentration_status")!="PASS" else 0
    return max(0.0,1.0-warnings)

def _stab_score(st):
    return 1.0 if st.get("temporal_sector_status")=="TEMPORAL_SECTOR_STABLE" else 0.0

def _range_score(ra):
    n = ra.get("range_bound_count",0)
    if not n: return 0.0
    best = ra.get("range_bound_best_sectors",[]); worst = ra.get("range_bound_worst_sectors",[])
    if not best or not worst: return 0.0
    b = best[0][1].get("median"); w = worst[0][1].get("median")
    return max(0.0,min(1.0,(b-w)/3.0)) if b is not None and w is not None else 0.0

def test_joint_separability(*, join_coverage: float, segment_profiles: dict, concentration_audit: dict, temporal_sector_stability: dict, range_bound_analysis: dict) -> dict:
    if join_coverage < JOINT_THRESHOLDS["min_join_coverage"]: status="DATA_INSUFFICIENT"; score=0.0
    else:
        ps=_perf_score(segment_profiles); cs=_conc_score(concentration_audit); ss=_stab_score(temporal_sector_stability); rs=_range_score(range_bound_analysis); js=min(1.0,join_coverage)
        score=ps*0.30+cs*0.20+ss*0.20+rs*0.20+js*0.10
        status = "JOINT_ATTRIBUTION_SEPARABLE" if score>=0.70 else "WEAKLY_JOINT_SEPARABLE" if score>=0.55 else "NOT_JOINT_SEPARABLE"
    return {"tester_version":"V3512_JOINT_SEPARABILITY_TESTER_V10","joint_separability_status":status,"joint_separability_score":score,"scoring_breakdown":{"performance_spread":_perf_score(segment_profiles),"concentration":_conc_score(concentration_audit),"stability":_stab_score(temporal_sector_stability),"range_explain":_range_score(range_bound_analysis),"join_quality":min(1.0,join_coverage)},"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
