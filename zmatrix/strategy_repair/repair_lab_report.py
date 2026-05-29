# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.strategy_repair.pathology_classifier import classify_dataset_pathology
from zmatrix.strategy_repair.segment_attributor import build_segment_attribution
from zmatrix.strategy_repair.repair_simulator import run_repair_simulation
from zmatrix.strategy_repair.repair_verdict import judge_all_repair_candidates
from zmatrix.strategy_repair.policy import validate_strategy_repair_report

def build_strategy_repair_lab_report(*, joined: list[dict], horizon: str = "t20") -> dict:
    pathology = classify_dataset_pathology(joined=joined, horizon=horizon)
    segment = build_segment_attribution(joined=joined, horizon=horizon)
    simulation = run_repair_simulation(joined=joined, horizon=horizon)
    verdict = judge_all_repair_candidates(simulation=simulation)
    report = {"report_version": "V352_STRATEGY_REPAIR_LAB_REPORT_V10", "mode": "REPAIR_LAB_ONLY", "horizon": horizon.upper(), "pathology": pathology, "segment_attribution": segment, "repair_simulation": simulation, "repair_verdict": verdict, "recommended_next_step": _next_step(verdict), "real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "real_z9_write_allowed": False, "hermes_memory_write_allowed": False, "auto_calibration_allowed": False, "runtime_enabled": False}
    report["policy_violations"] = validate_strategy_repair_report(report)
    return report

def _next_step(verdict: dict) -> str:
    ready = verdict.get("ready_candidates", [])
    return "PROMOTE_READY_CANDIDATES_TO_PAPER_ONLY_REPAIR_REPLAY" if ready else "NO_REPAIR_CANDIDATE_READY_REQUIRES_FEATURE_ATTRIBUTION"
