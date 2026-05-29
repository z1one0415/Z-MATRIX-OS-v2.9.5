# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.strategy_repair.filter_candidate_rules import REPAIR_CANDIDATE_RULES, apply_candidate_rule
from zmatrix.strategy_repair.repair_metrics import build_repair_metrics
from zmatrix.strategy_repair.schema import DEFAULT_REPAIR_SAFETY

def run_repair_simulation(*, joined: list[dict], horizon: str = "t20") -> dict:
    baseline = build_repair_metrics(joined=joined, horizon=horizon)
    candidates = {}
    for rule_name in REPAIR_CANDIDATE_RULES:
        applied = apply_candidate_rule(joined=joined, rule_name=rule_name)
        metrics = build_repair_metrics(joined=applied["kept"], horizon=horizon)
        candidates[rule_name] = {"rule": applied["rule"], "original_count": applied["original_count"], "kept_count": applied["kept_count"], "kept_rate": applied["kept_count"] / applied["original_count"] if applied["original_count"] else None, "metrics": metrics, "delta": _delta_metrics(baseline, metrics)}
    return {"simulation_version": "V352_REPAIR_SIMULATION_V10", "horizon": horizon.upper(), "baseline": baseline, "candidates": candidates, "safety": dict(DEFAULT_REPAIR_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}

def _delta_metrics(base: dict, new: dict) -> dict:
    def d(k):
        if base.get(k) is None or new.get(k) is None: return None
        return new.get(k) - base.get(k)
    return {"win_rate_delta": d("win_rate"), "median_delta": d("median"), "mean_delta": d("mean"), "trimmed_mean_delta": d("trimmed_mean_5pct"), "top_1pct_contribution_delta": d("top_1pct_contribution")}
