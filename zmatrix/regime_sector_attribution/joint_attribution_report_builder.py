# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_sector_attribution.regime_sector_joiner import build_regime_sector_joined_rows
from zmatrix.regime_sector_attribution.joint_segment_profiler import profile_joint_segments
from zmatrix.regime_sector_attribution.sector_concentration_auditor import audit_sector_concentration
from zmatrix.regime_sector_attribution.temporal_sector_stability import audit_temporal_sector_stability
from zmatrix.regime_sector_attribution.range_bound_analyzer import analyze_range_bound_drag
from zmatrix.regime_sector_attribution.joint_separability_tester import test_joint_separability
from zmatrix.regime_sector_attribution.joint_candidate_miner import mine_joint_candidates
from zmatrix.regime_sector_attribution.policy import validate_joint_attribution_report
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def build_joint_attribution_report(*, regime_replay_report: dict, sector_basket_report: dict, raw_replay_result: dict) -> dict:
    join = build_regime_sector_joined_rows(raw_replay_result=raw_replay_result, sector_basket_report=sector_basket_report)
    rows = join.get("joined_rows",[])
    profiles = profile_joint_segments(joined_rows=rows)
    concentration = audit_sector_concentration(joined_rows=rows)
    stability = audit_temporal_sector_stability(joined_rows=rows)
    range_analysis = analyze_range_bound_drag(joined_rows=rows)
    separability = test_joint_separability(join_coverage=join.get("join_coverage",0),segment_profiles=profiles,concentration_audit=concentration,temporal_sector_stability=stability,range_bound_analysis=range_analysis)
    candidates = mine_joint_candidates(joint_separability=separability)
    report = {"report_version":"V3512_REGIME_SECTOR_JOINT_ATTRIBUTION_REPORT_V10","mode":"PAPER_ONLY_JOINT_ATTRIBUTION","regime_sector_join":{"total_rows":join.get("total_rows"),"ready_rows":join.get("ready_rows"),"join_coverage":join.get("join_coverage"),"join_status":join.get("join_status")},"joint_segment_profiles":profiles,"sector_concentration_audit":concentration,"temporal_sector_stability":stability,"range_bound_analysis":range_analysis,"joint_separability":separability,"joint_candidates":candidates,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"synthetic_sector_index_production_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
    report["policy_violations"] = validate_joint_attribution_report(report)
    report["attribution_status"] = separability.get("joint_separability_status")
    report["recommended_next_step"] = {"JOINT_ATTRIBUTION_SEPARABLE":"v3.5.13 Regime×Sector Conditional Paper Replay","WEAKLY_JOINT_SEPARABLE":"v3.5.13 Observation Replay","NOT_JOINT_SEPARABLE":"v3.5.13 B-Matrix Reconstruction"}.get(report["attribution_status"],"Fix data")
    return report
