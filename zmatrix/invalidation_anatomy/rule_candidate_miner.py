from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def mine_conditional_invalidation_candidates(*, separability_report: dict) -> dict:
    status = separability_report.get("separability_status")
    top_features = separability_report.get("top_discriminating_features", [])
    candidates = []
    if status in ("SEPARABLE", "WEAKLY_SEPARABLE"):
        for f in top_features[:3]:
            candidates.append({"candidate_name": f"conditional_exit_by_{f['feature']}", "description": f"Use {f['feature']} at/near invalidation trigger to condition immediate exit vs delayed observation.", "feature": f["feature"], "entry_or_trigger_time_only": True, "lookahead_risk": False, "production_ready": False, "paper_replay_required": True})
    return {"candidate_report_version": "V354_CONDITIONAL_INVALIDATION_CANDIDATES_V10", "source_separability_status": status, "candidate_count": len(candidates), "candidates": candidates, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
