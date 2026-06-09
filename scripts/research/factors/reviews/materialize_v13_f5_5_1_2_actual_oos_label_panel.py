"""Stage C: Materialize V13.F5.5.1.2 Actual OOS Label Panel."""
import json, csv
from pathlib import Path
from datetime import date, timedelta

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
OUT.mkdir(parents=True, exist_ok=True)

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
REBALANCE_DATE = date(2026, 5, 6)
LABEL_MONTH = "2026-05"
HORIZONS = [5, 20]  # 60D blocked


def load_prices():
    """Load price data keyed by (ticker, date) -> close."""
    prices = {}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            key = (row["ticker"], date.fromisoformat(row["date"]))
            prices[key] = float(row["close"])
    return prices


def get_trading_days(prices):
    """Get sorted unique trading days."""
    return sorted(set(d for _, d in prices.keys()))


def forward_return(prices, ticker, start_date, horizon, trading_days):
    """Compute forward return from start_date over horizon trading days."""
    start_idx = None
    for i, d in enumerate(trading_days):
        if d == start_date:
            start_idx = i
            break
    if start_idx is None:
        return None
    end_idx = start_idx + horizon
    if end_idx >= len(trading_days):
        return None
    start_price = prices.get((ticker, trading_days[start_idx]))
    end_price = prices.get((ticker, trading_days[end_idx]))
    if start_price is None or end_price is None or start_price == 0:
        return None
    return round((end_price - start_price) / start_price, 6)


def main():
    if not PRICE_BARS.exists() or PRICE_BARS.stat().st_size < 100:
        print("ERROR: No price data available. Cannot materialize labels.")
        return

    prices = load_prices()
    trading_days = get_trading_days(prices)
    tickers = sorted(set(t for t, _ in prices.keys()))

    # Generate label rows
    rows = []
    for ticker in tickers:
        for horizon in HORIZONS:
            ret = forward_return(prices, ticker, REBALANCE_DATE, horizon, trading_days)
            if ret is not None:
                end_idx = trading_days.index(REBALANCE_DATE) + horizon
                rows.append({
                    "ticker": ticker,
                    "rebalance_date": REBALANCE_DATE.isoformat(),
                    "label_month": LABEL_MONTH,
                    "horizon": f"{horizon}D",
                    "forward_return": ret,
                    "label_available_at": trading_days[end_idx].isoformat(),
                    "source_price_start_date": REBALANCE_DATE.isoformat(),
                    "source_price_end_date": trading_days[end_idx].isoformat(),
                    "label_role": "OUTCOME_LABEL_ONLY"
                })

    # Write CSV
    csv_path = OUT / "v13_f5_5_1_2_actual_oos_label_panel.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["ticker", "rebalance_date", "label_month", "horizon",
                      "forward_return", "label_available_at",
                      "source_price_start_date", "source_price_end_date", "label_role"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Write manifest
    manifest = {
        "pipeline_signature": "Z2-V13-F5-5-1-2-ACTUAL-OOS-LABEL-PANEL-MANIFEST",
        "status": "V13_F5_5_1_2_ACTUAL_LABEL_PANEL_GENERATED",
        "base_commit": "db190ff",
        "label_month": LABEL_MONTH,
        "rebalance_date": REBALANCE_DATE.isoformat(),
        "generated_horizons": [f"{h}D" for h in HORIZONS],
        "blocked_horizons": ["60D"],
        "total_rows": len(rows),
        "rows_5D": sum(1 for r in rows if r["horizon"] == "5D"),
        "rows_20D": sum(1 for r in rows if r["horizon"] == "20D"),
        "rows_60D": 0,
        "tickers_count": len(tickers),
        "label_role": "OUTCOME_LABEL_ONLY",
        "written_to_feature_store": False,
        "used_for_factor_calculation": False,
        "used_for_candidate_decision": False,
        "used_for_monitoring_execution": False,
        "source_path": "data/price_bars/daily_bars.csv"
    }

    manifest_path = OUT / "v13_f5_5_1_2_actual_oos_label_panel_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"Written: {csv_path} ({len(rows)} rows)")
    print(f"Written: {manifest_path}")
    print(f"5D rows: {manifest['rows_5D']}, 20D rows: {manifest['rows_20D']}")


if __name__ == "__main__":
    main()
