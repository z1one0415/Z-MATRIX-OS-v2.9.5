"""Stage C: Run V13.F5.5.2.1 Directional Spread Diagnostic.

Joins signal scores with outcome labels and computes top-minus-bottom spread.
This is the FIRST time we cross factor signals with actual forward returns.
"""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")
SIGNAL_DIR = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
FACTORS = ["F21", "F24", "F30", "F31"]


def load_labels():
    """Load labels keyed by (ticker, horizon) -> forward_return."""
    labels = {}
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            key = (row["ticker"], row["horizon"])
            labels[key] = float(row["forward_return"])
    return labels


def load_signal(factor_id):
    """Load signal scores keyed by ticker -> {score, rank, bucket}."""
    signals = {}
    csv_path = SIGNAL_DIR / f"{factor_id}_signal_scores.csv"
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            signals[row["ticker"]] = {
                "score": float(row["score"]),
                "rank": int(row["rank"]),
                "bucket": int(row["bucket"])
            }
    return signals


def compute_spread(signals, labels, horizon):
    """Compute top-minus-bottom directional spread for a given horizon.

    With 5 tickers (buckets 1-5):
    - Top group: bucket 1-2 (top 2 ranked)
    - Bottom group: bucket 4-5 (bottom 2 ranked)
    """
    top_returns = []
    bottom_returns = []
    all_pairs = []

    for ticker, sig in signals.items():
        ret = labels.get((ticker, horizon))
        if ret is None:
            continue
        all_pairs.append((sig["bucket"], ret))
        if sig["bucket"] <= 2:
            top_returns.append(ret)
        elif sig["bucket"] >= 4:
            bottom_returns.append(ret)

    if not top_returns or not bottom_returns:
        return None

    top_mean = sum(top_returns) / len(top_returns)
    bottom_mean = sum(bottom_returns) / len(bottom_returns)
    spread = top_mean - bottom_mean

    # Sign consistency: proportion where higher bucket -> lower return
    sign_consistent = 0
    total_pairs = 0
    for i in range(len(all_pairs)):
        for j in range(i + 1, len(all_pairs)):
            b1, r1 = all_pairs[i]
            b2, r2 = all_pairs[j]
            if b1 != b2:
                total_pairs += 1
                # Higher bucket should have lower return (bucket 1 = best signal)
                if (b1 < b2 and r1 > r2) or (b1 > b2 and r1 < r2):
                    sign_consistent += 1

    sign_ratio = sign_consistent / total_pairs if total_pairs > 0 else 0.0

    return {
        "spread": round(spread, 6),
        "top_mean_return": round(top_mean, 6),
        "bottom_mean_return": round(bottom_mean, 6),
        "top_count": len(top_returns),
        "bottom_count": len(bottom_returns),
        "sign_consistency": round(sign_ratio, 4),
        "usable_ticker_count": len(all_pairs)
    }


def main():
    labels = load_labels()

    factor_diagnostics = []
    for factor_id in FACTORS:
        signals = load_signal(factor_id)

        diag_5d = compute_spread(signals, labels, "5D")
        diag_20d = compute_spread(signals, labels, "20D")

        factor_diagnostics.append({
            "factor_id": factor_id,
            "5D_spread": diag_5d,
            "20D_spread": diag_20d,
            "signal_available": True,
            "diagnostic_status": "COMPUTED"
        })

    diagnostic = {
        "pipeline_signature": "Z2-V13-F5-5-2-1-DIRECTIONAL-SPREAD-DIAGNOSTIC",
        "status": "V13_F5_5_2_1_DIRECTIONAL_SPREAD_DIAGNOSTIC_COMPUTED",
        "base_commit": "ecaf0a4",
        "sample_scope": "MICRO_SAMPLE_5_TICKERS",
        "formal_oos_validation_executed": False,
        "formal_statistical_inference_allowed": False,
        "rank_ic_reported_as_formal_evidence": False,
        "candidate_state_change_allowed": False,
        "monitoring_scope": FACTORS,
        "horizons_computed": ["5D", "20D"],
        "ticker_count": 5,
        "factor_diagnostics": factor_diagnostics,
        "summary": {
            "factors_with_spread_computed": sum(1 for fd in factor_diagnostics
                                                if fd["5D_spread"] is not None),
            "factors_with_positive_5D_spread": sum(1 for fd in factor_diagnostics
                                                    if fd["5D_spread"] and fd["5D_spread"]["spread"] > 0),
            "factors_with_positive_20D_spread": sum(1 for fd in factor_diagnostics
                                                     if fd["20D_spread"] and fd["20D_spread"]["spread"] > 0)
        },
        "sample_warning": "5 tickers is FAR below minimum for formal inference (>=475 tickers, >=6 OOS months)",
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_1_directional_spread_diagnostic.json"
    out_path.write_text(json.dumps(diagnostic, indent=2) + "\n")
    print(f"Written: {out_path}")
    for fd in factor_diagnostics:
        s5 = fd["5D_spread"]["spread"] if fd["5D_spread"] else "N/A"
        s20 = fd["20D_spread"]["spread"] if fd["20D_spread"] else "N/A"
        print(f"  {fd['factor_id']}: 5D={s5}, 20D={s20}")


if __name__ == "__main__":
    main()
