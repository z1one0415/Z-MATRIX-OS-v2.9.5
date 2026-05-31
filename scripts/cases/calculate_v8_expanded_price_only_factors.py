#!/usr/bin/env python3
"""V8-D: Calculate expanded (71 stocks) trailing price-only factors."""
import json
import csv
import io
import math
import hashlib
import os
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
LARGE = W / "runtime_reports" / "cases" / "v8_large_data"
LARGE.mkdir(parents=True, exist_ok=True)
CASES = W / "runtime_reports" / "cases"

FACTORS = {
    "MOM_1D": 1, "MOM_5D": 5, "MOM_10D": 10, "MOM_20D": 20, "MOM_60D": 60,
    "REV_1D": 1, "REV_5D": 5,
    "VOLATILITY_20D": 20, "VOLATILITY_60D": 60,
    "MAX_DRAWDOWN_60D": 60,
    "TRAILING_BENCHMARK_RELATIVE_20D": 20,
    "TRAILING_BENCHMARK_RELATIVE_60D": 60,
    "VOLUME_20D_AVG": 20, "VOLUME_60D_AVG": 60,
    "AMOUNT_20D_AVG": 20, "AMOUNT_60D_AVG": 60,
}


def load_data():
    prices = {}
    volumes = {}
    amounts = {}
    for row in csv.DictReader(
        io.StringIO((PROC / "v8_expanded_daily_price_bar.csv").read_text())
    ):
        t = row["ticker"]
        d = row["trade_date"]
        prices.setdefault(t, {})[d] = float(row["close"])
        volumes.setdefault(t, {})[d] = float(row["volume"])
        amounts.setdefault(t, {})[d] = float(row["amount"])
    benchmark = {}
    for row in csv.DictReader(
        io.StringIO((PROC / "v8_benchmark_csi300_price.csv").read_text())
    ):
        benchmark[row["trade_date"]] = float(row["close"])
    return prices, volumes, amounts, benchmark


def stdv(vals):
    if len(vals) < 2:
        return None
    m = sum(vals) / len(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))


def main():
    prices, volumes, amounts, benchmark = load_data()
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

    records = []
    for ad in as_of_dates:
        i = trade_dates.index(ad)
        for tk in tickers:
            ps = prices.get(tk, {})
            vs = volumes.get(tk, {})
            am = amounts.get(tk, {})
            fv = {}
            for fid, n in FACTORS.items():
                st = i - n + 1
                if st < 0:
                    continue
                wd = trade_dates[st : i + 1]
                iend = ad

                # Determine input_start_date based on factor type
                if fid.startswith("MOM_") or fid.startswith(
                    "TRAILING_BENCHMARK_RELATIVE_"
                ):
                    istart = trade_dates[i - n]
                elif fid in ("REV_1D", "REV_5D"):
                    istart = trade_dates[max(0, i - n)]
                else:
                    istart = trade_dates[st]

                val = None
                if fid.startswith("MOM_"):
                    pc = ps.get(trade_dates[st - 1])
                    cc = ps.get(ad)
                    if pc and cc and pc > 0:
                        val = cc / pc - 1
                elif fid == "REV_1D":
                    pc = ps.get(trade_dates[i - 1])
                    cc = ps.get(ad)
                    m = (cc / pc - 1) if pc and cc and pc > 0 else None
                    val = -m if m is not None else None
                elif fid == "REV_5D":
                    s5 = i - 5
                    pc = ps.get(trade_dates[s5]) if s5 >= 0 else None
                    cc = ps.get(ad)
                    m = (cc / pc - 1) if pc and cc and pc > 0 else None
                    val = -m if m is not None else None
                elif fid.startswith("VOLATILITY_"):
                    dr = []
                    prev = None
                    for d in wd:
                        cm = ps.get(d)
                        if prev and cm and prev > 0:
                            dr.append(cm / prev - 1)
                        prev = cm
                    val = stdv(dr) if dr else None
                elif fid == "MAX_DRAWDOWN_60D":
                    pk = -1e9
                    md = 1.0
                    for d in wd:
                        cl = ps.get(d)
                        if cl is None:
                            continue
                        if cl > pk:
                            pk = cl
                        if pk > 0:
                            md = min(md, cl / pk - 1)
                    val = md if md < 1.0 else 0.0
                elif fid.startswith("TRAILING_BENCHMARK_RELATIVE_"):
                    ps2 = ps.get(trade_dates[st - 1])
                    cs2 = ps.get(ad)
                    pb = benchmark.get(trade_dates[st - 1])
                    cb = benchmark.get(ad)
                    if ps2 and cs2 and ps2 > 0 and pb and cb and pb > 0:
                        val = (cs2 / ps2 - 1) - (cb / pb - 1)
                elif fid.startswith("VOLUME_"):
                    vl = [vs.get(d) for d in wd if vs.get(d) is not None]
                    val = sum(vl) / len(vl) if vl else None
                elif fid.startswith("AMOUNT_"):
                    al = [am.get(d) for d in wd if am.get(d) is not None]
                    val = sum(al) / len(al) if al else None
                else:
                    val = None

                if val is not None:
                    fv[fid] = {
                        "value": round(val, 10),
                        "truth_status": "REAL_READ_ONLY",
                        "lookback_days": n,
                        "input_start_date": istart,
                        "input_end_date": iend,
                        "as_of_date": ad,
                        "uses_future_data": False,
                        "calculation_formula": f"trailing_{fid}",
                    }
            if fv:
                records.append(
                    {
                        "as_of_date": ad,
                        "ticker": tk,
                        "factor_values": fv,
                        "ready_for_alpha_claim": False,
                    }
                )

    # Write large file (local only)
    j = json.dumps(
        {
            "status": "V8_EXPANDED_FACTOR_VALUES_CALCULATED",
            "factor_count": len(FACTORS),
            "stock_count": len(tickers),
            "as_of_date_count": len(as_of_dates),
            "records": records,
        },
        ensure_ascii=False,
    )
    fp = LARGE / "v8_expanded_factor_values.json"
    fp.write_text(j)
    fh = hashlib.sha256(j.encode()).hexdigest()
    fsize = os.path.getsize(fp)

    nvals = sum(len(r["factor_values"]) for r in records)
    exp_count = len(as_of_dates) * len(tickers) * len(FACTORS)
    coverage = round(nvals / exp_count, 4)

    summary = {
        "status": "SUMMARY_ONLY",
        "factor_records": len(records),
        "factor_values": nvals,
        "coverage": coverage,
        "large_file_hash": fh[:16],
        "large_file_size_mb": round(fsize / 1024 / 1024, 1),
        "committed_to_git": False,
    }
    (CASES / "v8_expanded_factor_values_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    print(
        f"Factor rebuild: {len(records)} records, {nvals} values, "
        f"coverage={coverage}, hash={fh[:16]}"
    )


if __name__ == "__main__":
    main()
