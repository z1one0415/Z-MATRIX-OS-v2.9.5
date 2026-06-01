#!/usr/bin/env python3
"""V9-D: Build factor selection gate from stability + decay + robustness."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"


def main():
    stability = json.loads(
        (CASES / "v9_formal_factor_stability.json").read_text()
    )
    decay_data = json.loads(
        (CASES / "v9_factor_decay_analysis.json").read_text()
    )
    robustness = json.loads(
        (CASES / "v9_factor_robustness.json").read_text()
    )

    decay_map = {d["factor_id"]: d for d in decay_data["decay_results"]}
    robust_map = {r["factor_id"]: r for r in robustness["robustness_results"]}

    promoted = []
    watch = []
    rejected = []

    for m in stability["metrics"]:
        fid = m["factor_id"]
        h = m["horizon"]
        dec = decay_map.get(fid, {})
        rob = robust_map.get(fid, {})

        evidence = {
            "mean_rankic": m["mean_rankic"],
            "positive_rankic_ratio": m.get("positive_rankic_ratio"),
            "rankic_ir": m.get("rankic_ir"),
            "valid_date_count": m["valid_date_count"],
            "decay_pattern": dec.get("decay_pattern"),
            "robustness_grade": rob.get("robustness_grade"),
        }

        if m["formal_sample_status"] != "SUFFICIENT":
            rejected.append(
                {
                    "factor_id": fid,
                    "horizon": h,
                    "decision": "REJECT_INSUFFICIENT_SAMPLE",
                    "evidence": evidence,
                    "ready_for_alpha_claim": False,
                    "alpha_validated": False,
                }
            )
        elif abs(m.get("mean_rankic", 0)) < 0.015:
            rejected.append(
                {
                    "factor_id": fid,
                    "horizon": h,
                    "decision": "REJECT_NO_SIGNAL",
                    "evidence": evidence,
                    "ready_for_alpha_claim": False,
                    "alpha_validated": False,
                }
            )
        elif rob.get("robustness_grade") in ("WEAK", "REJECT"):
            rejected.append(
                {
                    "factor_id": fid,
                    "horizon": h,
                    "decision": "REJECT_UNSTABLE",
                    "evidence": evidence,
                    "ready_for_alpha_claim": False,
                    "alpha_validated": False,
                }
            )
        elif (
            abs(m.get("mean_rankic", 0)) >= 0.03
            and m.get("positive_rankic_ratio", 0.5) is not None
            and (
                m["positive_rankic_ratio"] >= 0.55
                or m["positive_rankic_ratio"] <= 0.45
            )
            and rob.get("robustness_grade") in ("ROBUST", "REVIEW")
            and dec.get("decay_consistent")
        ):
            promoted.append(
                {
                    "factor_id": fid,
                    "horizon": h,
                    "decision": "PROMOTE_TO_COUNCIL_REVIEW",
                    "evidence": evidence,
                    "ready_for_council_research_review": True,
                    "ready_for_alpha_claim": False,
                    "alpha_validated": False,
                }
            )
        else:
            watch.append(
                {
                    "factor_id": fid,
                    "horizon": h,
                    "decision": "WATCH",
                    "evidence": evidence,
                    "ready_for_alpha_claim": False,
                    "alpha_validated": False,
                }
            )

    all_selections = promoted + watch + rejected
    out = {
        "status": "V9_FACTOR_SELECTION_GATE_BUILT",
        "factor_count": stability["factor_count"],
        "horizon_count": stability["horizon_count"],
        "promoted_factor_count": len(promoted),
        "watch_factor_count": len(watch),
        "rejected_factor_count": len(rejected),
        "selection_results": all_selections,
        "alpha_validated": False,
        "ready_for_alpha_claim": False,
    }
    (CASES / "v9_factor_selection_gate.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False)
    )
    print(
        f"Selection: {len(promoted)} promoted, "
        f"{len(watch)} watch, {len(rejected)} rejected"
    )
    for p in sorted(
        promoted, key=lambda x: abs(x["evidence"]["mean_rankic"]), reverse=True
    )[:5]:
        print(
            f"  PROMOTE: {p['factor_id']}×{p['horizon']} "
            f"RankIC={p['evidence']['mean_rankic']:.4f}"
        )


if __name__ == "__main__":
    main()
