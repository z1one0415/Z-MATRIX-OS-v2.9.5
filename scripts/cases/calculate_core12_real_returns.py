#!/usr/bin/env python3
"""V5.1-B: Core 12 real returns — fail-closed, date-aligned, formula-verified."""
import json, csv, io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
P = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"
REGISTRY = json.loads((W / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())

ENTRY_DATE = "20240102"
HORIZONS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}

def load_prices():
    data = {}
    for row in csv.DictReader(io.StringIO((P / "core12_daily_price_bar.csv").read_text())):
        data.setdefault(row["ticker"], {})[row["trade_date"]] = float(row["close"])
    return data

def load_trade_dates():
    """Use price data dates as trading calendar (cal is_open unreliable from tushare)."""
    dates = set()
    for row in csv.DictReader(io.StringIO((P / "core12_daily_price_bar.csv").read_text())):
        dates.add(row["trade_date"])
    return sorted(dates)

def forward_date(start, n, trade_dates):
    idx = trade_dates.index(start) if start in trade_dates else -1
    if idx < 0: return None
    target = idx + n
    return trade_dates[target] if target < len(trade_dates) else None

def normalize_date(d):
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(str(d)) == 8 else str(d)

def main():
    prices = load_prices()
    trade_dates = load_trade_dates()

    if ENTRY_DATE not in trade_dates:
        print(f"ERROR: ENTRY_DATE {ENTRY_DATE} not in trade dates")
        return

    results = []
    for c in REGISTRY:
        if c.get("case_layer") != "CORE": continue
        ticker = c["ticker"]
        ps = prices.get(ticker, {})
        returns = {}
        entry_close = ps.get(ENTRY_DATE)

        for hk, n in HORIZONS.items():
            fd = forward_date(ENTRY_DATE, n, trade_dates)
            exit_close = ps.get(fd) if fd else None

            # Fail-closed checks
            if entry_close is None:
                truth, blocked, ret = "BLOCKED_MISSING_ENTRY_PRICE", "entry_close missing", None
            elif entry_close <= 0:
                truth, blocked, ret = "BLOCKED_INVALID_ENTRY_PRICE", f"entry_close={entry_close}", None
            elif fd is None:
                truth, blocked, ret = "BLOCKED_INSUFFICIENT_FORWARD_DAYS", f"horizon {hk} exceeds calendar", None
            elif exit_close is None:
                truth, blocked, ret = "BLOCKED_MISSING_EXIT_PRICE", f"exit_close missing at {fd}", None
            elif exit_close <= 0:
                truth, blocked, ret = "BLOCKED_INVALID_EXIT_PRICE", f"exit_close={exit_close}", None
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

        results.append({
            "case_id": c["case_id"], "ticker": ticker, "name": c["name"],
            "entry_date": normalize_date(ENTRY_DATE),
            "entry_close": entry_close,
            "returns": returns,
            "ready_for_real_return": entry_close is not None and entry_close > 0,
            "ready_for_alpha_claim": False,
        })

    out = {
        "entry_date": normalize_date(ENTRY_DATE),
        "horizons": list(HORIZONS.keys()),
        "total_cases": len(results),
        "cases": results,
    }
    (CASES / "core_12_real_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    blocked = sum(1 for r in results for hk in HORIZONS if r["returns"][hk]["truth_status"] != "REAL_READ_ONLY")
    print(f"Real returns: {len(results)} cases x {len(HORIZONS)} horizons | entry={normalize_date(ENTRY_DATE)} | blocked_horizons={blocked}")

if __name__ == "__main__":
    main()
