#!/usr/bin/env python3
"""V13.F2.3 — Stage B: generate outcome label panel."""
import csv, json, sys
from pathlib import Path
from collections import defaultdict

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
PRICE_BARS = Path(__file__).resolve().parent.parent.parent.parent / "data" / "price_bars"
RUNTIME.mkdir(parents=True, exist_ok=True)

def load_price_bars(ticker: str) -> list[dict]:
    """Load price bars for a given ticker.
    Price bar files are named <ticker>.csv with ts_code column containing .SZ/.SH suffix."""
    fpath = PRICE_BARS / f"{ticker}.csv"
    if fpath.exists():
        rows = []
        with open(fpath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "trade_date": row["trade_date"],
                    "close": float(row["close"]),
                    "pct_chg": float(row["pct_chg"]) if row["pct_chg"] else 0.0
                })
        return rows
    # Try old format: file named <ticker>.SZ.csv or <ticker>.SH.csv
    for suffix in [".SZ", ".SH"]:
        fpath = PRICE_BARS / f"{ticker}{suffix}.csv"
        if fpath.exists():
            rows = []
            with open(fpath) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append({
                        "trade_date": row["trade_date"],
                        "close": float(row["close"]),
                        "pct_chg": float(row["pct_chg"]) if row["pct_chg"] else 0.0
                    })
            return rows
    return []

def compute_forward_return(rows: list[dict], anchor_date: str, horizon_days: int) -> float | None:
    """Compute forward return from anchor_date over horizon_days trading days."""
    anchor_idx = None
    for i, r in enumerate(rows):
        if r["trade_date"] == anchor_date:
            anchor_idx = i
            break
    if anchor_idx is None:
        return None
    target_idx = anchor_idx + horizon_days
    if target_idx >= len(rows):
        return None
    anchor_close = rows[anchor_idx]["close"]
    target_close = rows[target_idx]["close"]
    if anchor_close == 0:
        return None
    return (target_close - anchor_close) / anchor_close

def get_rebalance_dates_from_panel(panel_path: Path) -> set:
    """Get unique rebalance dates from a factor panel CSV."""
    dates = set()
    if not panel_path.exists():
        return dates
    with open(panel_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.add(row["rebalance_date"])
    return dates

# Rebalance dates from F03/F06 panel intersection
f03_dates = get_rebalance_dates_from_panel(RUNTIME / "f03_industry_relative_strength_panel.csv")
f06_dates = get_rebalance_dates_from_panel(RUNTIME / "f06_fundamental_quality_panel.csv")
all_dates = sorted(f03_dates | f06_dates)

# Get all tickers from both panels
all_tickers = set()
for fname in ["f03_industry_relative_strength_panel.csv", "f06_fundamental_quality_panel.csv"]:
    fpath = RUNTIME / fname
    if fpath.exists():
        with open(fpath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_tickers.add(row["ticker"])

labels = []
tickers_with_kline = set()
for ticker in sorted(all_tickers):
    rows = load_price_bars(ticker)
    if not rows:
        continue
    tickers_with_kline.add(ticker)
    for rebal_date in all_dates:
        ret_20d = compute_forward_return(rows, rebal_date, 20)
        ret_60d = compute_forward_return(rows, rebal_date, 60)
        if ret_20d is not None or ret_60d is not None:
            labels.append({
                "rebalance_date": rebal_date,
                "ticker": ticker,
                "forward_return_20d": ret_20d if ret_20d is not None else "",
                "forward_return_60d": ret_60d if ret_60d is not None else "",
                "label_known_after_rebalance": "true",
                "label_role": "OUTCOME_LABEL_ONLY"
            })

# Write label panel CSV
label_panel_path = RUNTIME / "single_factor_outcome_label_panel.csv"
fieldnames = ["rebalance_date", "ticker", "forward_return_20d", "forward_return_60d",
              "label_known_after_rebalance", "label_role"]
with open(label_panel_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(labels)

# Build report
rebal_dates_covered = sorted(set(l["rebalance_date"] for l in labels))
tickers_covered = sorted(set(l["ticker"] for l in labels))
report = {
    "pipeline_signature": "Z2-V13-F2-3-OUTCOME-LABEL-PANEL",
    "status": "V13_F2_3_OUTCOME_LABEL_PANEL_BUILT",
    "label_panel_built": True,
    "label_role": "OUTCOME_LABEL_ONLY",
    "label_horizons": ["20D", "60D"],
    "label_row_count": len(labels),
    "covered_rebalance_date_count": len(rebal_dates_covered),
    "covered_ticker_count": len(tickers_covered),
    "written_to_factor_panel": False,
    "label_known_after_rebalance": True,
    "forbidden_columns_written_to_factor_panel": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

report_path = RUNTIME / "v13_f2_3_outcome_label_panel_build_report.json"
report_path.write_text(json.dumps(report, indent=2))
print(f"[F2.3-B] Label panel built -> {label_panel_path} ({len(labels)} rows)")
print(f"[F2.3-B] Report -> {report_path}")
sys.exit(0)
