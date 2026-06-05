#!/usr/bin/env python3
"""V12.0: Build Research Signal Snapshot — cross-reference V11.6.1/7/8/9."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def build_factor_summary(oos_outcomes: dict) -> dict:
    """Aggregate OOS outcomes by factor_id+horizon."""
    summary = {}
    for obs in oos_outcomes.get("observations", []):
        fid = obs.get("factor_id", "UNKNOWN")
        horizon = obs.get("horizon", "UNKNOWN")
        key = f"{fid}|{horizon}"
        if key not in summary:
            summary[key] = {"hits": 0, "misses": 0, "total": 0, "rankic_direction": obs.get("rankic_direction", "UNKNOWN")}
        summary[key]["total"] += 1
        if obs.get("direction_hit", False):
            summary[key]["hits"] += 1
        else:
            summary[key]["misses"] += 1
    return summary


def classify_signal(hit_rate: float) -> str:
    if hit_rate >= 0.75:
        return "PROMOTE_TO_RESEARCH_REVIEW"
    elif hit_rate >= 0.50:
        return "OBSERVE"
    elif hit_rate >= 0.30:
        return "DOWNGRADE_TO_RESEARCH_ONLY"
    else:
        return "REJECT"


def walk_forward_support_factor(wf: dict, factor_id: str) -> str:
    """Check walk-forward support across periods."""
    periods = wf.get("periods", [])
    supported = 0
    total = len(periods)
    for p in periods:
        if p.get("calculated_results", 0) >= 30:
            supported += 1
    if total == 0:
        return "NO_WALK_FORWARD_DATA"
    if supported == total:
        return "FULL_SUPPORT"
    elif supported >= 2:
        return "PARTIAL_SUPPORT"
    return "WEAK_SUPPORT"


def cost_adjusted_factor(cost: dict) -> str:
    """Determine cost-adjusted status."""
    if cost.get("cost_model_status") == "RESEARCH_COST_MODEL_V1":
        if cost.get("eligible_for_v12_cost_gate", False):
            return "COST_ELIGIBLE"
        return "COST_MODEL_READY"
    return "COST_PROXY_ONLY"


def main():
    oos_outcomes = load("v11_6_1_oos_paper_outcomes.json")
    cost_model = load("v11_7_closeout.json")
    walk_forward = load("v11_8_walk_forward_tracking_results.json")
    lifecycle_seed = load("v11_9_factor_lifecycle_seed.json")

    factor_summary = build_factor_summary(oos_outcomes)
    lifecycle_states = lifecycle_seed.get("lifecycle_states", {})

    cost_status = cost_adjusted_factor(cost_model)

    signals = []
    for key, summary in sorted(factor_summary.items()):
        fid, horizon = key.split("|")
        total = summary["total"]
        hit_rate = summary["hits"] / total if total > 0 else 0.0

        wf_status = walk_forward_support_factor(walk_forward, fid)
        lifecycle = lifecycle_states.get(fid, "KEEP_OBSERVING")
        signal_state = classify_signal(hit_rate)

        signals.append({
            "research_signal_id": f"V12_RS_{len(signals)+1:03d}",
            "factor_id": fid,
            "horizon": horizon,
            "evidence_sources": [
                "V11_6_1_OOS",
                "V11_8_WALK_FORWARD",
                "V11_9_Z9_SEED",
            ],
            "oos_observation_count": total,
            "direction_hit_count": summary["hits"],
            "direction_miss_count": summary["misses"],
            "direction_hit_rate": round(hit_rate, 4),
            "cost_adjusted_status": cost_status,
            "walk_forward_status": wf_status,
            "z9_lifecycle_state": lifecycle,
            "research_signal_state": signal_state,
            "paper_only": True,
            "investment_action": "NONE",
            "trade_action": "NONE",
            "alpha_validated": False,
        })

    snapshot = {
        "status": "V12_RESEARCH_SIGNAL_SNAPSHOT_BUILT",
        "research_signal_count": len(signals),
        "promoted_count": sum(1 for s in signals if s["research_signal_state"] == "PROMOTE_TO_RESEARCH_REVIEW"),
        "observe_count": sum(1 for s in signals if s["research_signal_state"] == "OBSERVE"),
        "downgrade_count": sum(1 for s in signals if s["research_signal_state"] == "DOWNGRADE_TO_RESEARCH_ONLY"),
        "rejected_count": sum(1 for s in signals if s["research_signal_state"] == "REJECT"),
        "signals": signals,
        "paper_only": True,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(snapshot, open(C / "v12_research_signal_snapshot.json", "w"), indent=2)
    print(f"V12.0 Signal Snapshot: {len(signals)} signals | "
          f"promoted={snapshot['promoted_count']} observe={snapshot['observe_count']} "
          f"downgrade={snapshot['downgrade_count']} rejected={snapshot['rejected_count']}")


if __name__ == "__main__":
    main()
