# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_observation.temporal_instability_attributor import attribute_temporal_instability
from zmatrix.regime_observation.pool_resilience_deep_dive import deep_dive_pool_resilience
from zmatrix.regime_observation.sector_data_auditor import audit_sector_data, profile_sector_exposure
from zmatrix.regime_observation.matrix_clock_metadata_auditor import audit_matrix_clock_metadata
from zmatrix.regime_observation.zg18_conflict_observer import observe_zg18_conflicts
from zmatrix.regime_observation.o3_paper_fallback_study import build_o3_paper_fallback_study
from zmatrix.regime_observation.policy import validate_regime_observation_report
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def build_regime_observation_report(*, replay_report: dict, anti_overfit_report: dict, governance_report: dict) -> dict:
    pr = replay_report.get("policy_results") or replay_report.get("candidate_results") or {}
    all_rows = []
    for p in pr.values(): all_rows.extend(p.get("kept_rows") or p.get("kept") or []); all_rows.extend(p.get("downgraded_rows") or p.get("downgraded") or [])
    temporal = attribute_temporal_instability(anti_overfit_report=anti_overfit_report)
    pool = deep_dive_pool_resilience(replay_report=replay_report, governance_report=governance_report)
    sector_audit = audit_sector_data(rows=all_rows)
    sector_profile = profile_sector_exposure(rows=all_rows)
    clock = audit_matrix_clock_metadata(rows=all_rows)
    fps = replay_report.get("full_sample_pass_policies") or []
    conflict = observe_zg18_conflicts(full_sample_pass_policies=fps)
    fallback = build_o3_paper_fallback_study(pool_deep_dive=pool)
    report = {"report_version":"V358_REGIME_OBSERVATION_POOL_RESILIENCE_REPORT_V10","mode":"OBSERVATION_ONLY","temporal_instability_attribution":temporal,"pool_resilience_deep_dive":pool,"sector_data_audit":sector_audit,"sector_exposure_profile":sector_profile,"matrix_clock_metadata_audit":clock,"zg18_conflict_observation":conflict,"o3_paper_fallback_study":fallback,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"z9_auto_calibration_write_allowed":False,"g18_conflict_resolver_write_allowed":False,"o3_conditional_runtime_enabled":False,"fallback_pool_generation_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
    report["policy_violations"] = validate_regime_observation_report(report)
    sector_s = sector_audit.get("sector_data_status"); clock_s = clock.get("matrix_clock_status")
    pool_w = any(r.get("pool_resilience_deep_status")!="POOL_RESILIENCE_PASS" for r in pool.get("policy_pool_deep_results",{}).values())
    report["final_observation_status"] = "OBSERVATION_WARNING_SECTOR_DATA_INSUFFICIENT" if sector_s=="SECTOR_DATA_INSUFFICIENT" else "OBSERVATION_WARNING_CLOCK_DATA_INSUFFICIENT" if clock_s=="MATRIX_CLOCK_DATA_INSUFFICIENT" else "OBSERVATION_WARNING_POOL_CONCENTRATION" if pool_w else "OBSERVATION_READY"
    report["recommended_next_step"] = {"OBSERVATION_READY":"v3.5.9 Observation Portfolio Simulation Gate","OBSERVATION_WARNING_SECTOR_DATA_INSUFFICIENT":"v3.5.9 Sector Data Enrichment","OBSERVATION_WARNING_CLOCK_DATA_INSUFFICIENT":"v3.5.9 Matrix Clock Metadata Enrichment","OBSERVATION_WARNING_POOL_CONCENTRATION":"v3.5.9 Pool Resilience Repair / O3 Paper Fallback Study"}.get(report["final_observation_status"],"Fix observation policy violations before v3.5.9")
    return report
