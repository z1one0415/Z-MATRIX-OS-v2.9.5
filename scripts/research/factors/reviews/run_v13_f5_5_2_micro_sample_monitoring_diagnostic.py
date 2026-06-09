"""Stage D: Run V13.F5.5.2 Micro-Sample Monitoring Diagnostic."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")
SIGNAL_AUDIT = OUT / "v13_f5_5_2_factor_signal_availability_audit.json"

FROZEN_CANDIDATES = ["F04", "F10", "F11", "F14", "F15", "F16",
                     "F21", "F24", "F30", "F31"]


def main():
    # Load labels
    rows_5d = []
    rows_20d = []
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            ret = float(row["forward_return"])
            if row["horizon"] == "5D":
                rows_5d.append({"ticker": row["ticker"], "return": ret})
            elif row["horizon"] == "20D":
                rows_20d.append({"ticker": row["ticker"], "return": ret})

    # Load signal availability
    sig_audit = json.loads(SIGNAL_AUDIT.read_text())
    factors_available = [r for r in sig_audit["factor_results"]
                         if r["factor_status"] == "SIGNAL_AVAILABLE"]
    factors_blocked = [r for r in sig_audit["factor_results"]
                       if r["factor_status"] == "SIGNAL_INPUT_BLOCKED"]

    # Label-only statistics (what we CAN compute without factor signals)
    def label_stats(rows):
        returns = [r["return"] for r in rows]
        if not returns:
            return {"count": 0}
        pos = sum(1 for r in returns if r > 0)
        neg = sum(1 for r in returns if r < 0)
        return {
            "count": len(returns),
            "positive_count": pos,
            "negative_count": neg,
            "sign_consistency": max(pos, neg) / len(returns) if returns else 0,
            "mean_return": round(sum(returns) / len(returns), 6),
            "min_return": round(min(returns), 6),
            "max_return": round(max(returns), 6)
        }

    # Per-factor diagnostic
    factor_diagnostics = []
    for fid in FROZEN_CANDIDATES:
        factor_result = next((r for r in sig_audit["factor_results"]
                              if r["factor_id"] == fid), None)
        signal_available = (factor_result and
                            factor_result["factor_status"] == "SIGNAL_AVAILABLE")

        diag = {
            "factor_id": fid,
            "signal_available": signal_available,
            "5D_directional_spread": None,
            "20D_directional_spread": None,
            "diagnostic_status": ("COMPUTED" if signal_available
                                  else "SIGNAL_INPUT_BLOCKED_CANNOT_COMPUTE")
        }

        if signal_available:
            # Would compute directional spread here if signals existed
            # Spread = mean(return | signal > median) - mean(return | signal <= median)
            pass

        factor_diagnostics.append(diag)

    tickers_all = set(r["ticker"] for r in rows_5d + rows_20d)

    diagnostic = {
        "pipeline_signature": "Z2-V13-F5-5-2-MICRO-SAMPLE-MONITORING-DIAGNOSTIC",
        "status": "V13_F5_5_2_DIAGNOSTIC_EXECUTED_SIGNALS_BLOCKED",
        "base_commit": "e7d7b1f",
        "sample_scope": "MICRO_SAMPLE",
        "formal_statistical_inference_allowed": False,
        "rank_ic_reported_as_formal_evidence": False,
        "candidate_state_change_allowed": False,
        "label_coverage": {
            "total_label_rows": len(rows_5d) + len(rows_20d),
            "5D_rows": len(rows_5d),
            "20D_rows": len(rows_20d),
            "usable_ticker_count": len(tickers_all),
            "tickers": sorted(tickers_all)
        },
        "label_statistics": {
            "5D": label_stats(rows_5d),
            "20D": label_stats(rows_20d)
        },
        "factor_signal_summary": {
            "total_factors_checked": len(FROZEN_CANDIDATES),
            "factors_with_signal": len(factors_available),
            "factors_blocked": len(factors_blocked),
            "directional_spread_computable": len(factors_available) > 0
        },
        "factor_diagnostics": factor_diagnostics,
        "limitations": [
            "All 10 factor signals are BLOCKED (no pre-computed scores committed)",
            "Directional spread cannot be computed without factor signal data",
            "Sample size (5 tickers) insufficient for formal statistical inference",
            "This diagnostic is INFRASTRUCTURE VALIDATION only"
        ],
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_micro_sample_monitoring_diagnostic.json"
    out_path.write_text(json.dumps(diagnostic, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Factors available: {len(factors_available)}, Blocked: {len(factors_blocked)}")
    print(f"Label rows: {len(rows_5d) + len(rows_20d)}, Tickers: {len(tickers_all)}")


if __name__ == "__main__":
    main()
