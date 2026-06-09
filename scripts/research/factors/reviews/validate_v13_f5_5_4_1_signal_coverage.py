"""Stage E: Validate V13.F5.5.4.1 Signal Coverage."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")
TARGET_FACTORS = ["F04", "F10", "F11", "F14", "F15", "F16"]
MATERIALIZABLE = ["F04", "F10", "F11"]
BLOCKED = {"F14": "BLOCKED_BY_SOURCE_DATA", "F15": "BLOCKED_BY_SOURCE_DATA",
           "F16": "BLOCKED_BY_SOURCE_DATA"}


def get_label_tickers():
    tickers = set()
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            tickers.add(row["ticker"])
    return sorted(tickers)


def main():
    label_tickers = set(get_label_tickers())
    factor_coverage = {}

    for fid in TARGET_FACTORS:
        if fid in BLOCKED:
            factor_coverage[fid] = {
                "status": BLOCKED[fid],
                "covered_ticker_count": 0,
                "rows": 0,
                "blocked_reason": BLOCKED[fid]
            }
            continue

        csv_path = OUT / f"{fid}_signal_scores.csv"
        if not csv_path.exists():
            factor_coverage[fid] = {
                "status": "BLOCKED_CSV_NOT_FOUND",
                "covered_ticker_count": 0,
                "rows": 0,
                "blocked_reason": "signal_scores_csv_not_found"
            }
            continue

        signal_tickers = set()
        row_count = 0
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                signal_tickers.add(row["ticker"])
                row_count += 1

        covered = signal_tickers & label_tickers
        factor_coverage[fid] = {
            "status": "PASS" if covered == label_tickers else "PARTIAL",
            "covered_ticker_count": len(covered),
            "rows": row_count,
            "blocked_reason": None
        }

    materialized_pass = all(factor_coverage[f]["status"] == "PASS" for f in MATERIALIZABLE)
    total_pass = sum(1 for f in TARGET_FACTORS if factor_coverage[f]["status"] == "PASS")
    total_blocked = sum(1 for f in TARGET_FACTORS if "BLOCKED" in factor_coverage[f]["status"])

    validation = {
        "pipeline_signature": "Z2-V13-F5-5-4-1-SIGNAL-COVERAGE-VALIDATION",
        "status": ("V13_F5_5_4_1_SIGNAL_COVERAGE_PARTIAL" if total_blocked > 0
                   else "V13_F5_5_4_1_SIGNAL_COVERAGE_PASS"),
        "base_commit": "7384266",
        "factor_coverage": factor_coverage,
        "summary": {
            "total_target_factors": len(TARGET_FACTORS),
            "factors_materialized": total_pass,
            "factors_blocked": total_blocked,
            "price_based_all_pass": materialized_pass
        }
    }

    (OUT / "v13_f5_5_4_1_signal_coverage_validation.json").write_text(
        json.dumps(validation, indent=2) + "\n")
    print(f"Written: coverage validation (pass={total_pass}, blocked={total_blocked})")


if __name__ == "__main__":
    main()
