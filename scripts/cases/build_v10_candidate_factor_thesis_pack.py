#!/usr/bin/env python3
"""V10-D: Build candidate factor thesis pack — with full decay semantics."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    cr = json.loads((C / "v10_research_council_review.json").read_text())
    cands = []
    em = 0
    ci = 0

    for rv in cr["reviews"]:
        if rv["final_research_verdict"] not in ("RESEARCH_APPROVED", "WATCH_ONLY"):
            continue
        ev = rv["evidence"]
        required_keys = [
            "mean_rankic", "rankic_ir", "valid_date_count",
            "decay_pattern", "decay_pattern_basis",
            "rankic_direction", "raw_rankic_trend", "robustness_grade",
        ]
        if any(ev.get(k) is None for k in required_keys):
            em += 1
            continue
        ci += 1
        fid = rv["factor_id"]
        direction = ev.get("rankic_direction", "MIXED")
        pattern = ev.get("decay_pattern", "?")
        thesis = (
            f"Factor {fid} shows a {direction} RankIC signal at {rv['horizon']}; "
            f"absolute signal strength pattern is {pattern} across horizons. "
            "This is a research candidate only, not an investment action."
        )
        cands.append({
            "candidate_id": f"V10_CAND_{ci:03d}",
            "factor_id": fid,
            "horizon": rv["horizon"],
            "research_thesis": thesis,
            "supporting_evidence": {
                "mean_rankic": ev.get("mean_rankic"),
                "rankic_ir": ev.get("rankic_ir"),
                "valid_date_count": ev.get("valid_date_count"),
                "positive_rankic_ratio": ev.get("positive_rankic_ratio"),
                "decay_pattern": ev.get("decay_pattern"),
                "decay_pattern_basis": ev.get("decay_pattern_basis"),
                "rankic_direction": ev.get("rankic_direction"),
                "raw_rankic_trend": ev.get("raw_rankic_trend"),
                "robustness_grade": ev.get("robustness_grade"),
            },
            "counter_arguments": [
                "May be size/liquidity proxy." if ("AMOUNT" in fid or "VOLUME" in fid) else "Signal may not persist.",
                "No transaction cost model yet.",
                "No fundamental cross-validation.",
            ],
            "paper_tracking_required": True,
            "ready_for_alpha_claim": False,
            "alpha_validated": False,
            "investment_action": "NONE",
        })

    tp = {
        "status": "V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT",
        "candidate_count": len(cands),
        "evidence_complete_count": len(cands) - em,
        "evidence_missing_count": em,
        "investment_action_count": 0,
        "candidates": cands,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    json.dump(tp, open(C / "v10_candidate_factor_thesis_pack.json", "w"), indent=2)
    print(f"Thesis: {len(cands)} candidates, {em} evidence_missing")


if __name__ == "__main__":
    main()
