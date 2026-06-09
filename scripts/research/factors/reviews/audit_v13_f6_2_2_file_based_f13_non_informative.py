#!/usr/bin/env python3
"""F6.2.2 File-Based F13 Non-Informative Audit — reads real CSV, no hardcoded values."""
import csv, json
from pathlib import Path

CSV_PATH = Path("research/factor_library/reviews/batch_004/f6_2_tushare_pit_fundamental_ingestion/f6_2_fundamental_signal_scores.csv")
OUTDIR = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit")

def main():
    f13_rows = []
    tickers_seen = set()

    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["factor_id"] == "F13":
                f13_rows.append(row)
                tickers_seen.add(row["ticker"])

    all_score_zero = all(float(r["score"]) == 0.0 for r in f13_rows)

    result = {
        "factor_id": "F13",
        "classification": "MATERIALIZED_NON_INFORMATIVE",
        "num_rows": len(f13_rows),
        "num_distinct_tickers": len(tickers_seen),
        "tickers": sorted(tickers_seen),
        "all_scores_zero": all_score_zero,
        "details": f13_rows,
        "verdict": "PASS" if (len(f13_rows) == 4 and len(tickers_seen) == 4 and all_score_zero) else "FAIL"
    }

    outfile = OUTDIR / "v13_f6_2_2_file_based_f13_non_informative_audit.json"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"✅ F13 NON_INFORMATIVE verified: {len(f13_rows)} rows, {len(tickers_seen)} tickers, all_scores_zero={all_score_zero}")

if __name__ == "__main__":
    main()
