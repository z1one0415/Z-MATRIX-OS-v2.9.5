#!/usr/bin/env python3
"""V5.1-C: CSI300 benchmark returns — same entry_date, date-aligned."""
import json, csv, io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
P = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"

ENTRY_DATE = "20240102"
HORIZONS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}

def load_benchmark():
    data = {}
    for row in csv.DictReader(io.StringIO((P / "benchmark_csi300_price.csv").read_text())):
        data[row["trade_date"]] = float(row["close"])
    return data

def forward_date(start, n, trade_dates):
    idx = trade_dates.index(start) if start in trade_dates else -1
    if idx < 0: return None
    target = idx + n
    return trade_dates[target] if target < len(trade_dates) else None

def normalize_date(d):
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(str(d)) == 8 else str(d)

def main():
    bench = load_benchmark()
    trade_dates = sorted(bench.keys())

    if ENTRY_DATE not in trade_dates:
        print(f"ERROR: ENTRY_DATE {ENTRY_DATE} not in benchmark dates")
        return

    entry_close = bench[ENTRY_DATE]
    returns = {}

    for hk, n in HORIZONS.items():
        fd = forward_date(ENTRY_DATE, n, trade_dates)
        exit_close = bench.get(fd) if fd else None

        if entry_close is None:
            truth, blocked, ret = "BLOCKED_MISSING_ENTRY_PRICE", "entry_close missing", None
        elif fd is None:
            truth, blocked, ret = "BLOCKED_INSUFFICIENT_FORWARD_DAYS", f"horizon {hk} exceeds calendar", None
        elif exit_close is None:
            truth, blocked, ret = "BLOCKED_MISSING_EXIT_PRICE", f"exit_close missing at {fd}", None
        else:
            truth, blocked, ret = "REAL_READ_ONLY", None, (exit_close / entry_close - 1)

        returns[hk] = {
            "entry_date": normalize_date(ENTRY_DATE),
            "exit_date": normalize_date(fd) if fd else None,
            "entry_close": entry_close,
            "exit_close": exit_close,
            "return": round(ret, 10) if ret is not None else None,
            "calculation_formula": "exit_close / entry_close - 1",
            "truth_status": truth,
            "blocked_reason": blocked,
        }

    out = {
        "benchmark_id": "CSI300",
        "entry_date": normalize_date(ENTRY_DATE),
        "entry_close": entry_close,
        "horizons": list(HORIZONS.keys()),
        "returns": returns,
    }
    (CASES / "csi300_benchmark_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    blocked = sum(1 for hk in HORIZONS if returns[hk]["truth_status"] != "REAL_READ_ONLY")
    print(f"Benchmark: CSI300, {len(HORIZONS)} horizons | entry={normalize_date(ENTRY_DATE)} | blocked={blocked}")

if __name__ == "__main__":
    main()
