"""Stage E: Validate V13.F5.5.3.1 Signal Coverage."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")
ELIGIBLE_FACTORS = ["F21", "F24", "F30", "F31"]


def get_label_tickers():
    tickers = set()
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            tickers.add(row["ticker"])
    return sorted(tickers)


def main():
    label_tickers = set(get_label_tickers())
    factor_coverage = {}

    for factor_id in ELIGIBLE_FACTORS:
        csv_path = OUT / f"{factor_id}_signal_scores.csv"
        signal_tickers = set()
        if csv_path.exists():
            with open(csv_path) as f:
                for row in csv.DictReader(f):
                    signal_tickers.add(row["ticker"])

        covered = signal_tickers & label_tickers
        missing = label_tickers - signal_tickers

        factor_coverage[factor_id] = {
            "signal_tickers": len(signal_tickers),
            "label_tickers": len(label_tickers),
            "covered": len(covered),
            "missing": sorted(missing),
            "coverage_complete": len(missing) == 0
        }

    all_complete = all(fc["coverage_complete"] for fc in factor_coverage.values())

    validation = {
        "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-COVERAGE-VALIDATION",
        "status": ("V13_F5_5_3_1_SIGNAL_COVERAGE_PASS" if all_complete
                   else "V13_F5_5_3_1_SIGNAL_COVERAGE_PARTIAL"),
        "base_commit": "d9895da",
        "label_ticker_count": len(label_tickers),
        "covered_factor_count": len(ELIGIBLE_FACTORS),
        "blocked_factor_count": 10,
        "factor_coverage": factor_coverage,
        "all_eligible_factors_complete": all_complete
    }

    out_path = OUT / "v13_f5_5_3_1_signal_coverage_validation.json"
    out_path.write_text(json.dumps(validation, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"All complete: {all_complete}")


if __name__ == "__main__":
    main()
