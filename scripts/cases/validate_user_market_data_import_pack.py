#!/usr/bin/env python3
"""Validate that the user market data import pack is correctly prepared."""
import json, csv
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
PROCESSED = WORKSPACE / "data" / "research_db" / "market_data" / "processed"

EXPECTED_FILES = {
    "core12_daily_price_bar.csv": "Daily price bar for Core 12 tickers",
    "core12_adjustment_factor.csv": "Adjustment factors",
    "benchmark_csi300_price.csv": "CSI300 benchmark price",
    "trading_calendar.csv": "Trading calendar",
}

def main():
    missing = [f for f in EXPECTED_FILES if not (PROCESSED / f).exists()]
    present = [f for f in EXPECTED_FILES if (PROCESSED / f).exists()]

    print("Import Pack Status:")
    print("  Files expected:", len(EXPECTED_FILES))
    print("  Files present: ", len(present))
    print("  Files missing: ", len(missing))

    if missing:
        print()
        print("  Missing files:")
        for f in missing:
            print("    -", f, "(" + EXPECTED_FILES[f] + ")")
        print()
        print("  Place these in:", PROCESSED)
        print("  See docs/cases/CORE_12_REQUIRED_CSV_FILE_LIST.md")

    for f in present:
        count = len((PROCESSED / f).read_text().strip().split("\n")) - 1
        print("  " + f + ":", count, "rows")

    if len(missing) == 0:
        print()
        print("  All files present. Run check_v5_entry_gate.py to check V5 readiness.")
    else:
        print()
        print("  V5 entry blocked until all files are present.")

if __name__ == "__main__":
    main()
