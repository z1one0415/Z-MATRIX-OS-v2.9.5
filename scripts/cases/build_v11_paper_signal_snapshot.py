#!/usr/bin/env python3
"""V11-C: Build paper signal snapshot — MIXED direction enforces zero buckets."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"
L = W / "runtime_reports" / "cases" / "v8_large_data"


def main():
    fv_data = json.loads((L / "v8_expanded_factor_values.json").read_text())
    wl = json.loads((C / "v11_candidate_factor_watchlist.json").read_text())
    selector=json.loads((C/"v11_5_forward_compatible_as_of_date.json").read_text())
    latest_ad = selector.get("selected_as_of_date") or max(r["as_of_date"] for r in fv_data["records"])
    is_historical = selector.get("ready_for_historical_snapshot", False)

    snapshots = []
    for wi in wl["watch_items"]:
        fid = wi["factor_id"]
        rd = wi["rankic_direction"]
        vals = []
        for r in fv_data["records"]:
            if r["as_of_date"] == latest_ad and fid in r.get("factor_values", {}):
                vals.append((r["ticker"], r["factor_values"][fid]["value"]))
        vals.sort(key=lambda x: x[1])
        n = len(vals)

        if rd == "NEGATIVE":
            bot = [t for t, v in vals[: max(1, n // 5)]]
            top = [t for t, v in vals[-max(1, n // 5) :]]
            interp = "Lower values paper-observed as favorable under NEGATIVE RankIC."
            s = {
                "favored_bucket": bot,
                "comparison_bucket": top,
                "favored_bucket_size": len(bot),
                "comparison_bucket_size": len(top),
                "bucket_direction": "LOW_FACTOR_VALUE_FAVORED",
                "bucket_policy": "OBSERVATION_ONLY_NO_TRADE",
            }
        elif rd == "POSITIVE":
            top = [t for t, v in vals[-max(1, n // 5) :]]
            bot = [t for t, v in vals[: max(1, n // 5)]]
            interp = "Higher values paper-observed as favorable under POSITIVE RankIC."
            s = {
                "favored_bucket": top,
                "comparison_bucket": bot,
                "favored_bucket_size": len(top),
                "comparison_bucket_size": len(bot),
                "bucket_direction": "HIGH_FACTOR_VALUE_FAVORED",
                "bucket_policy": "OBSERVATION_ONLY_NO_TRADE",
            }
        else:  # MIXED or MISSING
            interp = "MIXED/MISSING RankIC direction: no preferred bucket generated."
            s = {
                "favored_bucket": [],
                "comparison_bucket": [],
                "favored_bucket_size": 0,
                "comparison_bucket_size": 0,
                "bucket_direction": "NO_PREFERRED_DIRECTION",
                "bucket_policy": "OBSERVATION_ONLY_NO_PREFERRED_DIRECTION",
            }

        snapshots.append(
            {
                "watch_id": wi["watch_id"],
                "factor_id": fid,
                "horizon": wi["horizon"],
                "rankic_direction": rd,
                "as_of_date": latest_ad,"as_of_date_policy":"HISTORICAL_FORWARD_COMPATIBLE" if is_historical else "LATEST_AVAILABLE","forward_compatible":is_historical,
                "universe_count": n,
                "signal_interpretation": interp,
                **s,
                "investment_action": "NONE",
            }
        )

    snap = {
        "status": "V11_PAPER_SIGNAL_SNAPSHOT_BUILT",
        "as_of_date": latest_ad,"as_of_date_policy":"HISTORICAL_FORWARD_COMPATIBLE" if is_historical else "LATEST_AVAILABLE","forward_compatible":is_historical,
        "candidate_factor_count": len(snapshots),
        "universe_count": len(set(r["ticker"] for r in fv_data["records"])),
        "snapshots": snapshots,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    json.dump(
        snap, open(C / "v11_paper_signal_snapshot.json", "w"), indent=2
    )
    mixed = [s for s in snapshots if s["rankic_direction"] == "MIXED"]
    print(
        f"Signal snapshot: {len(snapshots)} items @ {latest_ad} "
        f"| MIXED={len(mixed)} all_zero={all(s['favored_bucket_size']==0 for s in mixed)}"
    )


if __name__ == "__main__":
    main()
