#!/usr/bin/env python3
"""V5-B: Calculate Core 12 real historical returns T1/T5/T10/T20/T60."""
import json, csv, io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
P = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"
REGISTRY = json.loads((W / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
HORIZONS = [1, 5, 10, 20, 60]
HKEYS = ["T1", "T5", "T10", "T20", "T60"]

def load_prices():
    data = {}
    for row in csv.DictReader(io.StringIO((P / "core12_daily_price_bar.csv").read_text())):
        data.setdefault(row["ticker"], {})[row["trade_date"]] = float(row["close"])
    return data

def load_calendar_dates():
    dates = set()
    cf = P / "trading_calendar.csv"
    for row in csv.DictReader(io.StringIO(cf.read_text())):
        if row.get("is_open", "false").lower() == "true": dates.add(row["trade_date"])
    return sorted(dates)

def main():
    prices = load_prices()
    trade_dates = load_calendar_dates()
    entry = trade_dates[0]  # First trading day
    
    results = []
    for c in REGISTRY:
        if c.get("case_layer") != "CORE": continue
        ticker = c["ticker"]
        ps = prices.get(ticker, {})
        ec = ps.get(entry)
        returns = {}
        idx = trade_dates.index(entry) if entry in trade_dates else 0
        for n, hk in zip(HORIZONS, HKEYS):
            ti = idx + n
            if ti < len(trade_dates):
                fd = trade_dates[ti]
                ec2 = ps.get(fd)
                ret = (ec2 / ec - 1) if ec and ec2 else None
                returns[hk] = {"exit_date": fd, "exit_close": ec2,
                    "return": ret if ret is not None else None,
                    "truth_status": "REAL_READ_ONLY" if ret is not None else "BLOCKED_MISSING_EXIT_PRICE"}
            else:
                returns[hk] = {"exit_date": None, "exit_close": None, "return": None, "truth_status": "BLOCKED_INSUFFICIENT_FORWARD_DAYS"}
        
        results.append({"case_id": c["case_id"], "ticker": ticker, "name": c["name"],
            "entry_date": entry, "entry_close": ec, "returns": returns,
            "ready_for_real_return": ec is not None, "ready_for_alpha_claim": False})
    
    out = {"cases": results, "horizons": HKEYS, "entry_date": entry, "total_cases": len(results)}
    (CASES / "core_12_real_returns.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Real returns: {len(results)} cases x {len(HKEYS)} horizons")

if __name__ == "__main__":
    main()
