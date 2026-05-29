# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.governance_closeout.no_yaml_mutation_auditor import audit_no_yaml_mutation
from zmatrix.governance_closeout.candidate_pool_resilience_validator import validate_candidate_pool_resilience
from zmatrix.governance_closeout.parameter_change_governance import build_parameter_change_governance
from zmatrix.governance_closeout.matrix_clock_alignment_precheck import precheck_matrix_clock_alignment
from zmatrix.governance_closeout.zg18_conflict_precheck import precheck_zg18_conflict_risk
from zmatrix.governance_closeout.o3_conditional_fallback_planner import build_o3_conditional_fallback_plan
from zmatrix.governance_closeout.policy import validate_governance_closeout_report
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY

def build_governance_closeout_report(*, regime_replay_report: dict, base_ref="6d5f624", head_ref="HEAD") -> dict:
    ya = audit_no_yaml_mutation(base_ref=base_ref, head_ref=head_ref)
    pr = regime_replay_report.get("policy_results") or regime_replay_report.get("candidate_results") or {}
    pool = validate_candidate_pool_resilience(policy_results=pr)
    pg = build_parameter_change_governance(yaml_audit=ya)
    clk = precheck_matrix_clock_alignment(b_matrix_meta=regime_replay_report.get("b_matrix_meta"),r_matrix_meta=regime_replay_report.get("r_matrix_meta"),d_matrix_meta=regime_replay_report.get("d_matrix_meta"),as_of_date=regime_replay_report.get("as_of_date"))
    fps = regime_replay_report.get("full_sample_pass_policies") or []
    cf = precheck_zg18_conflict_risk(policies=fps, market_regime_status=regime_replay_report.get("regime_status"))
    fb = build_o3_conditional_fallback_plan(pool_resilience=pool)
    report = {"report_version":"V357_GOVERNANCE_POOL_RESILIENCE_REPORT_V10","mode":"GOVERNANCE_CLOSEOUT_ONLY","source_regime_replay_report_version":regime_replay_report.get("report_version"),"no_yaml_mutation_audit":ya,"candidate_pool_resilience":pool,"parameter_change_governance":pg,"matrix_clock_alignment_precheck":clk,"zg18_conflict_precheck":cf,"o3_conditional_fallback_plan":fb,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"z9_auto_calibration_write_allowed":False,"g18_conflict_resolver_write_allowed":False,"o3_conditional_runtime_enabled":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
    report["policy_violations"] = validate_governance_closeout_report(report)
    pool_risk = any(r.get("pool_resilience_status")!="POOL_RESILIENCE_PASS" for r in pool.get("policy_pool_results",{}).values())
    report["governance_status"] = "GOVERNANCE_WARNING_POOL_CONCENTRATION" if pool_risk else "GOVERNANCE_WARNING_CLOCK_DATA_INSUFFICIENT" if clk.get("clock_alignment_status")=="DATA_INSUFFICIENT" else "GOVERNANCE_PASS"
    report["recommended_next_step"] = {"GOVERNANCE_PASS":"v3.5.8 Observation Portfolio Simulation Gate","GOVERNANCE_WARNING_POOL_CONCENTRATION":"v3.5.8 Regime Observation + Pool Resilience Study","GOVERNANCE_WARNING_CLOCK_DATA_INSUFFICIENT":"v3.5.8 Data Freshness / Matrix Clock Metadata Enrichment"}.get(report["governance_status"],"Fix governance violations before v3.5.8")
    return report
