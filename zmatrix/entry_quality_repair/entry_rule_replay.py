# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.entry_quality_repair.candidate_rule_library import ENTRY_REPAIR_CANDIDATES, apply_entry_candidate_rule
from zmatrix.entry_quality_repair.repair_metrics import build_entry_repair_metrics
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def run_entry_rule_replay(*, enriched_rows: list[dict], horizon: str = "t20") -> dict:
    baseline = build_entry_repair_metrics(rows=enriched_rows, horizon=horizon)
    candidates = {}
    for rule_name in ENTRY_REPAIR_CANDIDATES:
        applied = apply_entry_candidate_rule(enriched_rows=enriched_rows, rule_name=rule_name)
        metrics = build_entry_repair_metrics(rows=applied["kept"], horizon=horizon)
        candidates[rule_name] = {"rule":applied["rule"],"original_count":applied["original_count"],"kept_count":applied["kept_count"],"kept_rate":applied["kept_rate"],"metrics":metrics,"delta":_delta(baseline,metrics)}
    return {"replay_version":"V355_ENTRY_RULE_REPLAY_V10","horizon":horizon.upper(),"baseline":baseline,"candidates":candidates,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}

def _delta(base, new):
    def d(k): return new[k]-base[k] if base.get(k) is not None and new.get(k) is not None else None
    return {"win_rate_delta":d("win_rate"),"median_delta":d("median"),"mean_delta":d("mean"),"trimmed_mean_delta":d("trimmed_mean_5pct"),"top_1pct_contribution_delta":d("top_1pct_contribution")}
