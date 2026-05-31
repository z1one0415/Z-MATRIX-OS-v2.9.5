#!/usr/bin/env python3
"""V5-C: Calculate CSI300 benchmark returns."""
import json, csv, io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
P = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"
HORIZONS = [1, 5, 10, 20, 60]
HKEYS = ["T1", "T5", "T10", "T20", "T60"]

def main():
    bench_data = {}
    for row in csv.DictReader(io.StringIO((P / "benchmark_csi300_price.csv").read_text())):
        bench_data[row["trade_date"]] = float(row["close"])
    
    trade_dates = sorted(bench_data.keys())
    entry = trade_dates[0]
    ec = bench_data[entry]
    idx = 0
    returns = {}
    for n, hk in zip(HORIZONS, HKEYS):
        ti = idx + n
        if ti < len(trade_dates):
            fd = trade_dates[ti]
            ec2 = bench_data.get(fd)
            ret = (ec2 / ec - 1) if ec2 else None
            returns[hk] = {"exit_date": fd, "return": ret, "entry_close": ec, "exit_close": ec2, "truth_status": "REAL_READ_ONLY" if ret is not None else "BLOCKED"}
        else:
            returns[hk] = {"exit_date": None, "return": None, "truth_status": "BLOCKED_INSUFFICIENT_FORWARD_DAYS"}
    
    out = {"benchmark_id": "CSI300", "entry_date": entry, "entry_close": ec, "returns": returns}
    (CASES / "csi300_benchmark_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Benchmark: CSI300, {len(returns)} horizons")

if __name__ == "__main__":
    main()
