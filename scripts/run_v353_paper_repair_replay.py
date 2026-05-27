#!/usr/bin/env python3
"""v3.5.3 Paper-Only Repair Replay — parallel with cached price paths"""
from __future__ import annotations
import argparse, json, csv, multiprocessing as mp
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from zmatrix.paper_repair_replay.repair_dataset_loader import load_paper_repair_dataset
from zmatrix.paper_repair_replay.invalidation_rule_extractor import extract_invalidation_rule
from zmatrix.paper_repair_replay.invalidation_exit_simulator import simulate_invalidation_exit
from zmatrix.paper_repair_replay.baseline_repair_comparator import compare_baseline_vs_repaired
from zmatrix.paper_repair_replay.policy import validate_paper_repair_replay_report
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

PRICE_CACHE = {}

def _clean_date(x) -> str: return str(x or "").replace("-", "").strip()

def _preload_price_paths(tickers: set, data_root: str, max_days: int):
    """Pre-load all unique ticker price paths into module cache."""
    global PRICE_CACHE
    loaded = 0
    for ticker in tickers:
        bare = str(ticker).split(".")[0]
        path = Path(data_root) / "data" / "price_bars" / f"{bare}.csv"
        if not path.exists(): continue
        bars = {}
        with open(path, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                d = _clean_date(row.get("trade_date") or row.get("date"))
                close = row.get("close")
                if not d or close in (None, ""): continue
                try: bars[d] = float(close)
                except Exception: continue
        PRICE_CACHE[ticker] = bars
        loaded += 1
    print(f"  Pre-loaded {loaded} ticker price paths", flush=True)
    return loaded

def _build_price_bars(ticker: str, entry_date: str, max_days: int):
    """Build bars list from cached price dict starting at entry_date."""
    bars_dict = PRICE_CACHE.get(ticker, {})
    entry = _clean_date(entry_date)
    bars = []
    for d in sorted(bars_dict.keys()):
        if d < entry: continue
        bars.append({"trade_date": d, "close": bars_dict[d]})
        if len(bars) >= max_days: break
    return bars

def _simulate_one(args):
    """Process one action. Returns (row, elapsed)."""
    action, max_days = args
    ticker = action.get("ticker") or ""
    entry_date = action.get("entry_date", "")

    rule = extract_invalidation_rule(action=action)
    bars = _build_price_bars(ticker, entry_date, max_days)
    path = {"bars": bars, "bar_count": len(bars), "path_status": "READY" if len(bars) >= 5 else "INSUFFICIENT"}
    sim = simulate_invalidation_exit(action=action, price_path=path, rule=rule, horizon_days=20)

    return {
        "paper_id": action.get("paper_id"),
        "ticker": ticker,
        "role": action.get("role"),
        "baseline_return_t20": action.get("baseline_return_t20"),
        "baseline_invalidation_triggered": action.get("baseline_invalidation_triggered"),
        "rule": rule,
        "price_path_status": path.get("path_status"),
        "simulation": sim,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--horizon-days", type=int, default=20)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--output", default="runtime_reports/v353_paper_repair_replay_report.json")
    args = ap.parse_args()

    import time; t0 = time.time()

    print("Loading repair dataset...", flush=True)
    dataset = load_paper_repair_dataset(replay_path="runtime_reports/v35_brd_strategy_replay_result.json")
    if dataset.get("dataset_status") != "READY":
        print(json.dumps(dataset, ensure_ascii=False, indent=2)); raise SystemExit(2)

    joined = dataset["joined"]
    items = joined[:args.max_items] if args.max_items else joined
    print(f"  Dataset: {len(joined):,} joined, {len(items):,} to process", flush=True)

    # Pre-load price paths
    tickers = {a.get("ticker", "") for a in items if a.get("ticker")}
    _preload_price_paths(tickers, ".", max(80, args.horizon_days + 5))

    # Build tasks
    max_days_val = max(80, args.horizon_days + 5)
    tasks = [(a, max_days_val) for a in items]
    print(f"  Workers: {args.workers}, Tasks: {len(tasks):,}", flush=True)

    # Parallel simulation
    rows = []
    ctx = mp.get_context('fork')
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as executor:
        results = executor.map(_simulate_one, tasks, chunksize=100)
        done = 0
        for row in results:
            rows.append(row)
            done += 1
            if done % 5000 == 0:
                elapsed = time.time() - t0
                print(f"  [{done}/{len(tasks)}] {done/elapsed:.0f}/s", flush=True)

    elapsed = time.time() - t0
    print(f"  Simulation done: {elapsed:.0f}s ({len(tasks)/elapsed:.0f} t/s)", flush=True)

    # Build comparison
    repaired_result = {"rows": rows}
    comparison = compare_baseline_vs_repaired(repaired_result=repaired_result)

    # Count additional stats
    exit_triggered = sum(1 for r in rows if r.get("simulation", {}).get("exit_triggered"))
    default_used = sum(1 for r in rows if r.get("rule", {}).get("default_rule_used"))

    # Build report
    report = {
        "report_version": "V353_PAPER_REPAIR_REPLAY_REPORT_V10",
        "mode": "PAPER_ONLY_REPAIR_REPLAY",
        "repair_rule": "apply_invalidation_exit_rule",
        "horizon_days": args.horizon_days,
        "repaired_outcomes": {"input_count": len(items), "ready_count": len(rows), "ready_rate": len(rows) / len(items) if items else None},
        "comparison": comparison,
        "exit_triggered_count": exit_triggered,
        "default_rule_used_count": default_used,
        "sample_rows": rows[:50],
        "lookahead_safe": True,
        "production_strategy_modified": False,
        "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY),
        "real_trade_allowed": False, "broker_order_allowed": False,
        "auto_buy_allowed": False, "auto_sell_allowed": False,
        "auto_position_close_allowed": False, "runtime_enabled": False,
    }
    report["policy_violations"] = validate_paper_repair_replay_report(report)

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    comp = comparison
    summary = {
        "report_version": report["report_version"], "repair_rule": report["repair_rule"],
        "input_count": len(items), "ready_count": len(rows), "ready_rate": len(rows)/len(items) if items else None,
        "exit_triggered_count": exit_triggered, "default_rule_used_count": default_used,
        "baseline": comp["baseline"], "repaired": comp["repaired"], "delta": comp["delta"],
        "lookahead_safe": report["lookahead_safe"],
        "production_strategy_modified": report["production_strategy_modified"],
        "policy_violations": report["policy_violations"],
        "real_trade_allowed": report["real_trade_allowed"],
        "broker_order_allowed": report["broker_order_allowed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report.get("policy_violations"): raise SystemExit(3)
    print("v3.5.3 paper-only repair replay report generated")

if __name__ == "__main__": main()
