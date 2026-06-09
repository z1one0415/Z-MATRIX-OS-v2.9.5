"""Stage C: Materialize V13.F5.5.4.1 Batch1/Batch2 Signal Scores.

Only price-based factors (F04/F10/F11) can be materialized.
F14/F15 (fundamental) and F16 (sentiment) are BLOCKED by source data unavailability.
"""
import json, csv, math
from pathlib import Path
from datetime import date

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")

REBALANCE_DATE = date(2026, 5, 6)
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"

# Only price-based factors can be materialized
MATERIALIZABLE = ["F04", "F10", "F11"]
BLOCKED = {
    "F14": "BLOCKED_BY_SOURCE_DATA",
    "F15": "BLOCKED_BY_SOURCE_DATA",
    "F16": "BLOCKED_BY_SOURCE_DATA"
}


def load_pre_rebalance_prices():
    """Load price data strictly BEFORE rebalance date."""
    data = {}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d < REBALANCE_DATE:
                ticker = row["ticker"]
                if ticker not in data:
                    data[ticker] = []
                data[ticker].append({
                    "date": d,
                    "close": float(row["close"]),
                    "volume": int(row["volume"])
                })
    for t in data:
        data[t].sort(key=lambda x: x["date"])
    return data


def get_label_tickers():
    tickers = set()
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            tickers.add(row["ticker"])
    return sorted(tickers)


def compute_f04_residual_momentum(bars):
    """F04: Cumulative return over t-20 to t-5 (skip recent 5 days for residual)."""
    if len(bars) < 20:
        return 0.0
    start_price = bars[-20]["close"]
    end_price = bars[-5]["close"]
    if start_price == 0:
        return 0.0
    return round((end_price - start_price) / start_price, 6)


def compute_f10_low_volatility(bars):
    """F10: Inverse of 20-day realized volatility (lower vol = higher score)."""
    if len(bars) < 20:
        return 0.0
    returns = [(bars[i]["close"] - bars[i-1]["close"]) / bars[i-1]["close"]
               for i in range(max(1, len(bars)-20), len(bars))]
    if not returns:
        return 0.0
    mean_r = sum(returns) / len(returns)
    variance = sum((r - mean_r)**2 for r in returns) / len(returns)
    std = variance ** 0.5
    if std == 0:
        return 1.0
    return round(1.0 / (1.0 + std * 100), 6)  # normalize to 0-1 range


def compute_f11_short_term_reversal(bars):
    """F11: Negative of 5-day cumulative return (reversal signal)."""
    if len(bars) < 5:
        return 0.0
    start_price = bars[-5]["close"]
    end_price = bars[-1]["close"]
    if start_price == 0:
        return 0.0
    five_day_return = (end_price - start_price) / start_price
    return round(-five_day_return, 6)  # negative = reversal signal


FACTOR_FUNCTIONS = {
    "F04": compute_f04_residual_momentum,
    "F10": compute_f10_low_volatility,
    "F11": compute_f11_short_term_reversal,
}


def rank_and_bucket(scores):
    """Rank scores (1=best/highest) and assign bucket (1-5)."""
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])
    ranked = {}
    for i, (ticker, score) in enumerate(sorted_items):
        rank = i + 1
        bucket = min(5, max(1, math.ceil(rank * 5 / len(sorted_items))))
        ranked[ticker] = {"score": score, "rank": rank, "bucket": bucket}
    return ranked


def main():
    prices = load_pre_rebalance_prices()
    tickers = get_label_tickers()

    all_rows = []
    factor_summaries = []

    # Materialize price-based factors
    for factor_id in MATERIALIZABLE:
        compute_fn = FACTOR_FUNCTIONS[factor_id]
        raw_scores = {}
        for ticker in tickers:
            bars = prices.get(ticker, [])
            raw_scores[ticker] = compute_fn(bars)

        ranked = rank_and_bucket(raw_scores)

        csv_path = OUT / f"{factor_id}_signal_scores.csv"
        rows = []
        with open(csv_path, "w", newline="") as f:
            fieldnames = ["factor_id", "ticker", "rebalance_date", "score",
                          "rank", "bucket", "score_available_at",
                          "source_artifact_ref", "signal_role"]
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for ticker in tickers:
                r = ranked[ticker]
                row = {
                    "factor_id": factor_id,
                    "ticker": ticker,
                    "rebalance_date": REBALANCE_DATE.isoformat(),
                    "score": r["score"],
                    "rank": r["rank"],
                    "bucket": r["bucket"],
                    "score_available_at": REBALANCE_DATE.isoformat(),
                    "source_artifact_ref": f"research/factor_library/sources/{factor_id}/formula_contract.json",
                    "signal_role": SIGNAL_ROLE
                }
                w.writerow(row)
                rows.append(row)
                all_rows.append(row)

        factor_summaries.append({
            "factor_id": factor_id,
            "status": "MATERIALIZED",
            "rows_generated": len(rows),
            "tickers_covered": len(tickers)
        })
        print(f"Written: {csv_path} ({len(rows)} rows)")

    # Document blocked factors
    for factor_id, reason in BLOCKED.items():
        factor_summaries.append({
            "factor_id": factor_id,
            "status": reason,
            "rows_generated": 0,
            "tickers_covered": 0,
            "blocked_reason": reason
        })
        print(f"BLOCKED: {factor_id} ({reason})")

    # Write manifest
    manifest = {
        "pipeline_signature": "Z2-V13-F5-5-4-1-BATCH1-BATCH2-SIGNAL-SCORES-MANIFEST",
        "status": "V13_F5_5_4_1_SIGNAL_SCORES_PARTIAL",
        "base_commit": "7384266",
        "rebalance_date": REBALANCE_DATE.isoformat(),
        "materialized_factors": MATERIALIZABLE,
        "blocked_factors": list(BLOCKED.keys()),
        "blocked_reasons": BLOCKED,
        "ticker_count": len(tickers),
        "tickers": tickers,
        "rows_per_materializable_factor": len(tickers),
        "total_signal_rows": len(all_rows),
        "signal_role": SIGNAL_ROLE,
        "source_data": "data/price_bars (pre-rebalance only)",
        "forward_return_used_for_signal": False,
        "outcome_label_used_for_signal": False,
        "written_to_feature_store": False,
        "factor_summaries": factor_summaries
    }

    (OUT / "v13_f5_5_4_1_signal_scores_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")
    print(f"\nManifest written. Total materialized rows: {len(all_rows)}")
    print(f"Materialized: {MATERIALIZABLE}, Blocked: {list(BLOCKED.keys())}")


if __name__ == "__main__":
    main()
