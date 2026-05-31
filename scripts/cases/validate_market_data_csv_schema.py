#!/usr/bin/env python3
"""Validate market data CSV files against V4 schema."""
import csv, sys, hashlib
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).resolve().parent.parent.parent
PROCESSED = WORKSPACE / "data" / "research_db" / "market_data" / "processed"
CORE12_TICKERS = {"600519","300750","688981","601899","300124","002594","300274","002371","600030","600276","002050","300763"}

REQUIRED = {
    "daily_price_bar": ["ticker","trade_date","open","high","low","close","volume","amount","source_name","source_type","source_file","source_hash","as_of_date","adjusted"],
    "adjustment_factor": ["ticker","trade_date","adjust_factor","factor_type","source_name","source_type","source_file","source_hash","as_of_date"],
    "benchmark_price": ["benchmark_id","trade_date","open","high","low","close","volume","amount","source_name","source_type","source_file","source_hash","as_of_date"],
    "trading_calendar": ["exchange","trade_date","is_open","source_name","source_type","source_file","source_hash","as_of_date"],
}

def detect_type(headers):
    h = set(headers)
    for t, r in REQUIRED.items():
        if set(r).issubset(h): return t
    return None

def validate_row(row, dtype, line_no):
    errors = []
    # Date format
    if "trade_date" in row:
        try: datetime.strptime(row["trade_date"], "%Y-%m-%d")
        except: errors.append(f"Line {line_no}: invalid date {row.get('trade_date')}")
    # Prices positive
    if dtype in ("daily_price_bar", "benchmark_price"):
        for f in ("open","high","low","close"):
            v = float(row.get(f, -1))
            if v <= 0: errors.append(f"Line {line_no}: {f}={v} not positive")
    # High >= max(open,close,low)
    if dtype in ("daily_price_bar", "benchmark_price") and all(f in row for f in ("open","high","low","close")):
        o,c,l,h = float(row["open"]), float(row["close"]), float(row["low"]), float(row["high"])
        if h < max(o,c,l): errors.append(f"Line {line_no}: high={h} < max(open={o},close={c},low={l})")
    # Low <= min
        if l > min(o,c,h): errors.append(f"Line {line_no}: low={l} > min")
    # Volume >= 0
    if "volume" in row and float(row.get("volume",-1)) < 0:
        errors.append(f"Line {line_no}: volume negative")
    # Ticker in Core12
    if dtype == "daily_price_bar" and row.get("ticker","") not in CORE12_TICKERS:
        errors.append(f"Line {line_no}: ticker {row.get('ticker')} not in Core 12")
    # source_type != SYNTHETIC
    if row.get("source_type") == "SYNTHETIC":
        errors.append(f"Line {line_no}: source_type=SYNTHETIC not allowed")
    # source_hash required
    if row.get("source_hash", "") in ("", "<sha256>"):
        errors.append(f"Line {line_no}: source_hash missing or placeholder")
    return errors

def main():
    csv_files = list(PROCESSED.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in processed/. Templates available in templates/.")
        print("Place real market data CSV files in processed/ to validate.")
        return

    all_errors = []
    for f in csv_files:
        reader = csv.DictReader(f.read_text().splitlines())
        dtype = detect_type(reader.fieldnames)
        if not dtype:
            all_errors.append(f"{f.name}: unknown type, headers={reader.fieldnames}")
            continue
        for i, row in enumerate(reader, start=2):
            errs = validate_row(row, dtype, i)
            for e in errs: all_errors.append(f"{f.name}: {e}")

    if all_errors:
        for e in all_errors: print(f"❌ {e}")
        sys.exit(1)
    else:
        print(f"✅ {len(csv_files)} files validated successfully")

if __name__ == "__main__":
    main()
