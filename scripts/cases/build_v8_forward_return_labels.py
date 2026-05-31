#!/usr/bin/env python3
"""V8-E: Build expanded forward return labels from V8 price + benchmark CSV."""
import json
import csv
import io
import hashlib
import os
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
LARGE = W / "runtime_reports" / "cases" / "v8_large_data"
LARGE.mkdir(parents=True, exist_ok=True)
CASES = W / "runtime_reports" / "cases"

HORIZONS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}


def load_prices():
    p = {}
    for row in csv.DictReader(
        io.StringIO((PROC / "v8_expanded_daily_price_bar.csv").read_text())
    ):
        t = row["ticker"]
        d = row["trade_date"]
        p.setdefault(t, {})[d] = float(row["close"])
    return p


def load_benchmark():
    b = {}
    for row in csv.DictReader(
        io.StringIO((PROC / "v8_benchmark_csi300_price.csv").read_text())
    ):
        b[row["trade_date"]] = float(row["close"])
    return b


def main():
    prices = load_prices()
    benchmark = load_benchmark()

    trade_dates = sorted(
        set(
            r["trade_date"]
            for r in csv.DictReader(
                io.StringIO(
                    (PROC / "v8_expanded_daily_price_bar.csv").read_text()
                )
            )
        )
    )
    tickers = sorted(prices.keys())
    as_of_dates = trade_dates[60:]

    labels = []
    for ad in as_of_dates:
        i = trade_dates.index(ad)
        for tk in tickers:
            ps = prices.get(tk, {})
            for hn, n in HORIZONS.items():
                ti = i + n
                if ti >= len(trade_dates):
                    continue
                fd = trade_dates[ti]
                ec = ps.get(ad)
                xc = ps.get(fd)
                if not ec or not xc or ec <= 0 or xc <= 0:
                    continue
                bc = benchmark.get(ad)
                bx = benchmark.get(fd)
                fsr = xc / ec - 1
                fbr = bx / bc - 1 if bc and bx and bc > 0 else None
                frr = fsr - fbr if fbr is not None else None
                labels.append(
                    {
                        "as_of_date": ad,
                        "ticker": tk,
                        "horizon": hn,
                        "exit_date": fd,
                        "future_stock_return": round(fsr, 10),
                        "future_relative_return": (
                            round(frr, 10) if frr is not None else None
                        ),
                        "label_status": "REAL_FORWARD_LABEL",
                        "used_as_factor_input": False,
                    }
                )

    j = json.dumps(
        {
            "status": "V8_FORWARD_LABELS_BUILT",
            "stock_count": len(tickers),
            "label_records": len(labels),
            "labels": labels,
        },
        ensure_ascii=False,
    )
    fp = LARGE / "v8_forward_return_labels.json"
    fp.write_text(j)
    fh = hashlib.sha256(j.encode()).hexdigest()
    fsize = os.path.getsize(fp)

    summary = {
        "status": "SUMMARY_ONLY",
        "label_records": len(labels),
        "large_file_hash": fh[:16],
        "large_file_size_mb": round(fsize / 1024 / 1024, 1),
        "committed_to_git": False,
    }
    (CASES / "v8_forward_return_labels_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    print(f"Labels: {len(labels)} records, hash={fh[:16]}")


if __name__ == "__main__":
    main()
