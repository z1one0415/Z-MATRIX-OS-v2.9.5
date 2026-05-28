from __future__ import annotations
from zmatrix.regime_attribution.market_regime_builder import build_market_regime
from zmatrix.regime_attribution.sector_phase_builder import build_sector_phase
from zmatrix.regime_attribution.breadth_liquidity_builder import build_breadth_regime
from zmatrix.regime_attribution.regime_feature_joiner import join_regime_features
from zmatrix.regime_attribution.regime_performance_profiler import profile_regime_performance
from zmatrix.regime_attribution.regime_separability_tester import test_regime_separability
from zmatrix.regime_attribution.regime_candidate_miner import mine_regime_candidates
from zmatrix.regime_attribution.policy import validate_regime_attribution_report
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def build_regime_attribution_report(*, joined: list[dict], index_data: dict, max_items: int | None = None) -> dict:
    items = joined[:max_items] if max_items else joined
    idx = index_data.get("000001", index_data.get(list(index_data.keys())[0], {})) if index_data else {}
    enriched = []
    for sample in items:
        mr = build_market_regime(sample=sample, index_data=idx)
        sp = build_sector_phase(sample=sample)
        br = build_breadth_regime()
        feature_status = "READY" if mr.get("regime_data_status")=="READY" else "PARTIAL"
        row = join_regime_features(sample=sample, market_regime=mr, sector_phase=sp, breadth=br, feature_status=feature_status)
        enriched.append(row)
    profile = profile_regime_performance(enriched_rows=enriched)
    separability = test_regime_separability(enriched_rows=enriched)
    candidates = mine_regime_candidates(separability=separability)
    next_step = {"REGIME_SEPARABLE":"v3.5.7 Regime-Conditioned Paper Replay","WEAKLY_REGIME_SEPARABLE":"v3.5.7 Regime Observation Replay","NOT_REGIME_SEPARABLE":"v3.5.7 B-Matrix Reconstruction","DATA_INSUFFICIENT":"v3.5.7 Market Data Enrichment"}.get(separability.get("separability_status"),"v3.5.7")
    report = {"report_version":"V356_MARKET_REGIME_ATTRIBUTION_REPORT_V10","mode":"ATTRIBUTION_ONLY","input_count":len(items),"feature_ready_count":len(enriched),"feature_ready_rate":len(enriched)/len(items) if items else None,"market_regime_counts":profile.get("market_regime_counts",{}),"sector_phase_counts":{},"breadth_regime_counts":{},"liquidity_regime_counts":{},"regime_performance_profile":profile,"regime_separability":separability,"regime_candidates":candidates,"recommended_next_step":next_step,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
    report["policy_violations"] = validate_regime_attribution_report(report)
    return report
