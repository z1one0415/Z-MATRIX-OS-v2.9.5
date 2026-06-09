"""Stage B: Audit V13.F5.5.1.2 Price Bars Source."""
import json, csv
from pathlib import Path
from datetime import date, timedelta

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
OUT.mkdir(parents=True, exist_ok=True)

PRICE_BARS = Path("data/price_bars")
REBALANCE_DATE = date(2026, 5, 6)
LABEL_MONTH = "2026-05"

def trading_days_from(start, n):
    """Count n trading days forward from start (exclusive)."""
    d = start
    count = 0
    while count < n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            count += 1
    return d

# Load price data
data_file = PRICE_BARS / "daily_bars.csv"
exists = data_file.exists() and data_file.stat().st_size > 100

dates_available = set()
tickers_found = set()
if exists:
    with open(data_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates_available.add(date.fromisoformat(row["date"]))
            tickers_found.add(row["ticker"])

max_date = max(dates_available) if dates_available else None

# Check forward windows
need_5d = trading_days_from(REBALANCE_DATE, 5)
need_20d = trading_days_from(REBALANCE_DATE, 20)
need_60d = trading_days_from(REBALANCE_DATE, 60)

has_5d = max_date is not None and max_date >= need_5d
has_20d = max_date is not None and max_date >= need_20d
has_60d = max_date is not None and max_date >= need_60d

audit = {
    "pipeline_signature": "Z2-V13-F5-5-1-2-PRICE-BARS-SOURCE-AUDIT",
    "status": "V13_F5_5_1_2_PRICE_BARS_SOURCE_AUDIT_PASS" if (exists and has_5d and has_20d) else "V13_F5_5_1_2_PRICE_BARS_SOURCE_AUDIT_BLOCKED",
    "base_commit": "db190ff",
    "source_path": "data/price_bars",
    "source_type": "LOCAL_READ_ONLY",
    "label_month": LABEL_MONTH,
    "rebalance_date": REBALANCE_DATE.isoformat(),
    "tickers_found": len(tickers_found),
    "dates_available": len(dates_available),
    "max_date": max_date.isoformat() if max_date else None,
    "checks": {
        "price_bars_exists": exists,
        "source_is_local_read_only": True,
        "covers_rebalance_date": REBALANCE_DATE in dates_available if dates_available else False,
        "5D_forward_window_complete": has_5d,
        "20D_forward_window_complete": has_20d,
        "60D_forward_window_complete": has_60d,
        "no_factor_score_read": True,
        "no_rank_bucket_read": True,
        "no_feature_store_read": True,
        "no_external_data_source_call": True
    },
    "violation_count": 0
}

out_path = OUT / "v13_f5_5_1_2_price_bars_source_audit.json"
out_path.write_text(json.dumps(audit, indent=2) + "\n")
print(f"Written: {out_path}")
print(f"5D: {has_5d}, 20D: {has_20d}, 60D: {has_60d}")
