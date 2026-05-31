#!/usr/bin/env python3
"""V7-A: Build rolling forward return labels from real CSV data."""
import json, csv, io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"
HORIZONS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}

def main():
    prices = {}
    for row in csv.DictReader(io.StringIO((PROC / "core12_daily_price_bar.csv").read_text())):
        t, d = row["ticker"], row["trade_date"]
        prices.setdefault(t, {})[d] = float(row["close"])
    benchmark = {}
    for row in csv.DictReader(io.StringIO((PROC / "benchmark_csi300_price.csv").read_text())):
        benchmark[row["trade_date"]] = float(row["close"])
    trade_dates = sorted(prices.get("600519", {}).keys())
    REG = json.loads((W / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
    CORE = [c for c in REG if c.get("case_layer") == "CORE"]

    # as_of_dates from factor snapshots (day 61 onward)
    fv = json.loads((CASES / "v6b_price_only_factor_values.json").read_text())
    ads = fv.get("as_of_date_range", [trade_dates[60], trade_dates[-1]])
    i0 = trade_dates.index(ads[0])
    as_of_dates = [trade_dates[i0 + j] for j in range(len(trade_dates) - i0)]

    labels = []
    for ad in as_of_dates:
        if ad not in trade_dates:
            continue
        i = trade_dates.index(ad)
        for c in CORE:
            tk = c["ticker"]
            ps = prices.get(tk, {})
            for hn, n in HORIZONS.items():
                ti = i + n
                if ti >= len(trade_dates):
                    continue
                fd = trade_dates[ti]
                ec = ps.get(ad)
                xc = ps.get(fd)
                bc = benchmark.get(ad)
                bx = benchmark.get(fd)
                if not ec or not xc or ec <= 0 or xc <= 0:
                    continue
                fsr = xc / ec - 1
                fbr = bx / bc - 1 if bc and bx and bc > 0 else None
                frr = fsr - fbr if fbr is not None else None
                labels.append({
                    "as_of_date": ad, "ticker": tk, "case_id": c["case_id"],
                    "horizon": hn, "entry_close": ec, "exit_date": fd,
                    "exit_close": xc, "future_stock_return": round(fsr, 10),
                    "future_benchmark_return": round(fbr, 10) if fbr is not None else None,
                    "future_relative_return": round(frr, 10) if frr is not None else None,
                    "label_status": "REAL_FORWARD_LABEL",
                    "used_as_factor_input": False,
                    "ready_for_alpha_claim": False,
                })

    out = {
        "status": "V7_FORWARD_RETURN_LABELS_BUILT",
        "core_12_cases": len(CORE),
        "as_of_date_count": len(as_of_dates),
        "horizons": list(HORIZONS.keys()),
        "label_records": len(labels),
        "labels": labels,
    }
    (CASES / "v7_forward_return_labels.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Forward labels: {len(labels)} records ({len(as_of_dates)} dates × {len(CORE)} cases × {len(HORIZONS)} horizons)")

if __name__ == "__main__":
    main()
