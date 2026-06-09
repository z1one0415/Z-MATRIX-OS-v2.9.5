#!/usr/bin/env python3
"""F6.2.2 File-Based Row Count and Coverage Audit — reads real CSV, no hardcoded values."""
import csv, json
from pathlib import Path

CSV_PATH = Path("research/factor_library/reviews/batch_004/f6_2_tushare_pit_fundamental_ingestion/f6_2_fundamental_signal_scores.csv")
OUTDIR = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit")

def main():
    rows = []
    factors_seen = set()
    tickers_seen = set()
    dates_seen = set()
    roles_seen = set()

    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            factors_seen.add(row["factor_id"])
            tickers_seen.add(row["ticker"])
            dates_seen.add(row["rebalance_date"])
            roles_seen.add(row["signal_role"])

    expected_factors = {"F06","F07","F08","F12","F13","F14","F15"}
    expected_tickers = {"000977","002050","002472","601899"}
    forbidden_tickers = {"588000"}

    result = {
        "total_rows": len(rows),
        "expected_rows": 28,
        "row_count_match": len(rows) == 28,
        "factors_found": sorted(factors_seen),
        "factors_expected": sorted(expected_factors),
        "factors_match": factors_seen == expected_factors,
        "tickers_found": sorted(tickers_seen),
        "tickers_expected": sorted(expected_tickers),
        "tickers_match": tickers_seen == expected_tickers,
        "etf_588000_present": "588000" in tickers_seen,
        "etf_588000_correctly_absent": "588000" not in tickers_seen,
        "rebalance_dates": sorted(dates_seen),
        "all_rebalance_date_2026_05_06": dates_seen == {"2026-05-06"},
        "signal_roles": sorted(roles_seen),
        "all_signal_role_factors_only": roles_seen == {"FACTOR_SIGNAL_ONLY"},
        "verdict": "PASS" if (
            len(rows) == 28 and
            factors_seen == expected_factors and
            tickers_seen == expected_tickers and
            dates_seen == {"2026-05-06"} and
            roles_seen == {"FACTOR_SIGNAL_ONLY"} and
            "588000" not in tickers_seen
        ) else "FAIL"
    }

    outfile = OUTDIR / "v13_f6_2_2_file_based_row_count_and_coverage_audit.json"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"✅ Row count: {len(rows)}/28 | Factors: {len(factors_seen)}/7 | Tickers: {len(tickers_seen)}/4 | ETF 588000 absent: {'588000' not in tickers_seen}")

if __name__ == "__main__":
    main()
