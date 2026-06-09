"""Stage C: Materialize V13.F5.5.3.1 Minimal Signal Scores.

Computes factor scores for F21/F24/F30/F31 using ONLY pre-rebalance price data.
Does NOT read forward_return or outcome labels.
"""
import json, csv, math
from pathlib import Path
from datetime import date

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")

REBALANCE_DATE = date(2026, 5, 6)
ELIGIBLE_FACTORS = ["F21", "F24", "F30", "F31"]
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"


def load_pre_rebalance_prices():
    """Load price data strictly BEFORE rebalance date, keyed by ticker."""
    data = {}  # ticker -> list of {date, open, high, low, close, volume}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d < REBALANCE_DATE:
                ticker = row["ticker"]
                if ticker not in data:
                    data[ticker] = []
                data[ticker].append({
                    "date": d,
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": int(row["volume"])
                })
    # Sort by date
    for ticker in data:
        data[ticker].sort(key=lambda x: x["date"])
    return data


def get_label_tickers():
    """Get tickers from label panel (NOT reading forward_return)."""
    tickers = set()
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            tickers.add(row["ticker"])
    return sorted(tickers)


def compute_f21_trend_persistence(bars):
    """F21: TREND_PERSISTENCE_QUALITY - ratio of consecutive same-direction days."""
    if len(bars) < 5:
        return 0.0
    returns = [(bars[i]["close"] - bars[i-1]["close"]) / bars[i-1]["close"]
               for i in range(1, len(bars))]
    if not returns:
        return 0.0
    # Count max consecutive same-sign streak
    max_streak = 1
    current_streak = 1
    for i in range(1, len(returns)):
        if (returns[i] >= 0) == (returns[i-1] >= 0):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    return round(max_streak / len(returns), 6)


def compute_f24_volatility_compression(bars):
    """F24: VOLATILITY_COMPRESSION_BREAKOUT - recent vs long-term volatility ratio."""
    if len(bars) < 10:
        return 0.0
    returns = [(bars[i]["close"] - bars[i-1]["close"]) / bars[i-1]["close"]
               for i in range(1, len(bars))]
    # Recent 5-day std vs full-period std
    recent = returns[-5:] if len(returns) >= 5 else returns
    full = returns
    std_recent = (sum((r - sum(recent)/len(recent))**2 for r in recent) / len(recent))**0.5
    std_full = (sum((r - sum(full)/len(full))**2 for r in full) / len(full))**0.5
    if std_full == 0:
        return 0.0
    # Lower ratio = more compressed = higher signal (invert for ranking)
    return round(1.0 - (std_recent / std_full), 6)


def compute_f30_volume_price_confirmation(bars):
    """F30: VOLUME_PRICE_CONFIRMATION - correlation between returns and volume changes."""
    if len(bars) < 5:
        return 0.0
    returns = [(bars[i]["close"] - bars[i-1]["close"]) / bars[i-1]["close"]
               for i in range(1, len(bars))]
    vol_changes = [(bars[i]["volume"] - bars[i-1]["volume"]) / max(bars[i-1]["volume"], 1)
                   for i in range(1, len(bars))]
    n = min(len(returns), len(vol_changes))
    if n < 3:
        return 0.0
    r = returns[:n]
    v = vol_changes[:n]
    mean_r = sum(r) / n
    mean_v = sum(v) / n
    cov = sum((r[i] - mean_r) * (v[i] - mean_v) for i in range(n)) / n
    std_r = (sum((x - mean_r)**2 for x in r) / n)**0.5
    std_v = (sum((x - mean_v)**2 for x in v) / n)**0.5
    if std_r == 0 or std_v == 0:
        return 0.0
    return round(cov / (std_r * std_v), 6)


def compute_f31_downside_tail_risk(bars):
    """F31: DOWNSIDE_TAIL_RISK - negative of max drawdown (higher = less risk)."""
    if len(bars) < 5:
        return 0.0
    prices = [b["close"] for b in bars]
    peak = prices[0]
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (p - peak) / peak
        if dd < max_dd:
            max_dd = dd
    # Invert: less drawdown = higher score
    return round(-max_dd, 6)


FACTOR_FUNCTIONS = {
    "F21": compute_f21_trend_persistence,
    "F24": compute_f24_volatility_compression,
    "F30": compute_f30_volume_price_confirmation,
    "F31": compute_f31_downside_tail_risk,
}


def rank_and_bucket(scores):
    """Rank scores (1=best/highest) and assign bucket (quintile 1-5)."""
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])  # descending
    ranked = {}
    for i, (ticker, score) in enumerate(sorted_items):
        rank = i + 1
        bucket = min(5, max(1, math.ceil(rank * 5 / len(sorted_items))))
        ranked[ticker] = {"score": score, "rank": rank, "bucket": bucket}
    return ranked


def main():
    prices = load_pre_rebalance_prices()
    tickers = get_label_tickers()

    # Verify all tickers have price data
    for t in tickers:
        if t not in prices or len(prices[t]) < 5:
            print(f"WARNING: Insufficient data for {t}")

    # Compute and write signals for each factor
    all_rows = []
    factor_summaries = []

    for factor_id in ELIGIBLE_FACTORS:
        compute_fn = FACTOR_FUNCTIONS[factor_id]
        raw_scores = {}
        for ticker in tickers:
            bars = prices.get(ticker, [])
            raw_scores[ticker] = compute_fn(bars)

        ranked = rank_and_bucket(raw_scores)

        # Write per-factor CSV
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
                    "source_artifact_ref": f"research/factor_library/factors/{factor_id}/factor_manifest.json",
                    "signal_role": SIGNAL_ROLE
                }
                w.writerow(row)
                rows.append(row)
                all_rows.append(row)

        factor_summaries.append({
            "factor_id": factor_id,
            "rows_generated": len(rows),
            "tickers_covered": len(tickers),
            "score_range": [min(r["score"] for r in ranked.values()),
                            max(r["score"] for r in ranked.values())]
        })
        print(f"Written: {csv_path} ({len(rows)} rows)")

    # Write manifest
    manifest = {
        "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-SCORES-MANIFEST",
        "status": "V13_F5_5_3_1_SIGNAL_SCORES_GENERATED",
        "base_commit": "d9895da",
        "rebalance_date": REBALANCE_DATE.isoformat(),
        "materialized_factors": ELIGIBLE_FACTORS,
        "ticker_count": len(tickers),
        "tickers": tickers,
        "rows_per_factor": len(tickers),
        "total_signal_rows": len(all_rows),
        "signal_role": SIGNAL_ROLE,
        "source_data": "data/price_bars (pre-rebalance only)",
        "forward_return_used_for_signal": False,
        "outcome_label_used_for_signal": False,
        "written_to_feature_store": False,
        "factor_summaries": factor_summaries
    }

    manifest_path = OUT / "v13_f5_5_3_1_signal_scores_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Written: {manifest_path}")
    print(f"Total rows: {len(all_rows)}")


if __name__ == "__main__":
    main()
