#!/usr/bin/env python3
"""V9-B: Factor decay analysis with rankic direction and abs pattern."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    stability = json.loads(
        (C / "v9_formal_factor_stability.json").read_text()
    )
    fids = sorted(set(m["factor_id"] for m in stability["metrics"]))
    horizons = ["T1", "T5", "T10", "T20", "T60"]

    decay_results = []
    for fid in fids:
        h_rics = {}
        for h in horizons:
            m = next(
                (
                    s
                    for s in stability["metrics"]
                    if s["factor_id"] == fid and s["horizon"] == h
                ),
                None,
            )
            if m and m["formal_sample_status"] == "SUFFICIENT":
                h_rics[h] = m["mean_rankic"]

        if len(h_rics) < 2:
            continue

        vals = list(h_rics.values())
        abs_vals = [abs(v) for v in vals]
        best_h = max(h_rics, key=lambda k: abs(h_rics[k]))

        # RankIC direction
        if all(v > 0 for v in vals):
            direction = "POSITIVE"
        elif all(v < 0 for v in vals):
            direction = "NEGATIVE"
        else:
            direction = "MIXED"

        # Raw trend
        if vals == sorted(vals):
            raw_trend = "RAW_MONOTONIC_INCREASING"
        elif vals == sorted(vals, reverse=True):
            raw_trend = "RAW_MONOTONIC_DECREASING"
        else:
            raw_trend = "RAW_NON_MONOTONIC"

        # ABS pattern
        if all(abs(v) < 0.01 for v in vals):
            pattern = "NO_CLEAR_PATTERN"
        elif abs_vals == sorted(abs_vals):
            pattern = "ABS_MONOTONIC_INCREASING"
        elif abs_vals == sorted(abs_vals, reverse=True):
            pattern = "ABS_MONOTONIC_DECREASING"
        elif best_h in ("T1", "T5"):
            pattern = "SHORT_HORIZON_PEAK"
        elif best_h in ("T10", "T20"):
            pattern = "MEDIUM_HORIZON_PEAK"
        elif best_h == "T60":
            pattern = "LONG_HORIZON_PEAK"
        else:
            pattern = "NO_CLEAR_PATTERN"

        decay_results.append(
            {
                "factor_id": fid,
                "rankic_by_horizon": h_rics,
                "best_horizon": best_h,
                "decay_pattern": pattern,
                "decay_pattern_basis": "absolute_rankic_magnitude",
                "rankic_direction": direction,
                "raw_rankic_trend": raw_trend,
                "decay_consistent": len(h_rics) >= 3,
                "ready_for_alpha_claim": False,
                "alpha_validated": False,
            }
        )

    out = {
        "status": "V9_FACTOR_DECAY_ANALYSIS_BUILT",
        "factor_count": len(fids),
        "horizons": horizons,
        "decay_results": decay_results,
        "alpha_validated": False,
    }
    (C / "v9_factor_decay_analysis.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False)
    )
    directions = set(r["rankic_direction"] for r in decay_results)
    print(
        f"Decay: {len(decay_results)} factors, "
        f"directions={directions}, "
        f"patterns={set(r['decay_pattern'] for r in decay_results)}"
    )


if __name__ == "__main__":
    main()
