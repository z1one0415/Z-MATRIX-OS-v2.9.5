#!/usr/bin/env python3
"""
v3.5 Parallel BRD Strategy Validation — 独立并行模块
Reuses _process_one_ticker + fork architecture from quick audit.
Produces: replay_result (raw) + validation_metrics + failure_analysis
"""
import json, sys, os, time, argparse, multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_DATA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reuse the same processing function from quick audit
from scripts.run_v35_brd_result_audit_quick import _process_one_ticker

from zmatrix.brd_strategy_validation.date_sampler import sample_replay_dates_from_index
from zmatrix.brd_strategy_validation.metrics_aggregator import aggregate_validation_metrics
from zmatrix.brd_strategy_validation.failure_analyzer import analyze_validation_failures
from zmatrix.historical_replay.replay_universe import build_replay_universe


def build_replay_result(dates, paper_actions, outcomes, failures):
    """Build the standard replay_result dict from collected data."""
    daily_results = []
    for d in dates:
        day_papers = [p for p in paper_actions if p and p.get("replay_date") == d]
        day_paper_ids = {p.get("paper_id") for p in day_papers}
        day_outcomes = [o for o in outcomes if o and o.get("paper_id") in day_paper_ids]
        day_failures = [f for f in failures if f and f.get("replay_date") == d]
        daily_results.append({
            "replay_date": d,
            "paper_actions": day_papers,
            "outcomes": day_outcomes,
            "failures": day_failures,
        })
    total_paper = sum(len(d.get("paper_actions", [])) for d in daily_results)
    return {
        "multi_day_replay_version": "BRD_STRATEGY_REPLAY_MULTI_DAY_V10",
        "mode": "HISTORICAL_STRATEGY_VALIDATION_ONLY",
        "date_count": len(dates),
        "success_day_count": len(daily_results),
        "failure_day_count": 0,
        "total_paper_actions": total_paper,
        "daily_results": daily_results,
        "failures": failures,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser(description="v3.5 Parallel BRD Strategy Validation")
    parser.add_argument("--max-dates", type=int, default=60)
    parser.add_argument("--max-tickers", type=int, default=5523)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--horizon", type=str, default="t20", choices=["t5", "t20", "t60"])
    parser.add_argument("--replay-output", type=str,
                        default="runtime_reports/v35_brd_strategy_replay_result.json")
    parser.add_argument("--validation-output", type=str,
                        default="runtime_reports/v35_brd_strategy_validation_report.json")
    args = parser.parse_args()

    t0 = time.time()

    # ── 1. Sample dates ──
    print("Sampling dates...", flush=True)
    sampled = sample_replay_dates_from_index(local_data_root=LOCAL_DATA_ROOT,
                                             index_code="000001",
                                             max_dates=args.max_dates + 20)
    print(f"  dates sampled in {time.time()-t0:.1f}s", flush=True)

    if sampled.get("sample_status") != "READY":
        print("BLOCKED: no dates"); sys.exit(2)

    all_dates = sampled["dates"]
    cut = args.max_dates + 20 - args.max_dates if args.max_dates + 20 > args.max_dates else max(1, len(all_dates) - args.max_dates)
    dates = all_dates[-args.max_dates:] if len(all_dates) > args.max_dates else all_dates[cut:]

    # ── 2. Build universe ──
    print("Building ticker universe...", flush=True)
    universe = build_replay_universe(replay_date=dates[0], local_data_root=LOCAL_DATA_ROOT,
                                     max_tickers=args.max_tickers)
    tickers = universe.get("tickers", [])
    if not tickers:
        print("BLOCKED: no tickers"); sys.exit(3)
    print(f"  Universe: {len(tickers)} tickers ({len(universe.get('excluded',[]))} excluded)", flush=True)

    # ── 3. Build tasks ──
    tasks = [(ticker, date, LOCAL_DATA_ROOT) for date in dates for ticker in tickers]
    print(f"\nDates: {len(dates)} | Tickers: {len(tickers)} | Workers: {args.workers}")
    print(f"Tasks: {len(tasks)}", flush=True)

    # ── 4. Parallel execution ──
    paper_actions, outcomes, failures = [], [], []
    ctx = mp.get_context('fork')
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as executor:
        results = executor.map(_process_one_ticker, tasks, chunksize=20)
        done = 0
        for paper, outcome, error in results:
            done += 1
            if error:
                failures.append(error)
            else:
                paper_actions.append(paper)
                outcomes.append(outcome)
            if done % 100 == 0:
                elapsed = time.time() - t0
                print(f"  [{done}/{len(tasks)}] {done/elapsed:.0f}/s", flush=True)

    elapsed = time.time() - t0
    throughput = len(tasks) / elapsed if elapsed > 0 else 0
    print(f"\n  Execution: {elapsed:.0f}s ({throughput:.0f} tasks/s)", flush=True)

    # ── 5. Build replay_result ──
    print("Building replay_result...", flush=True)
    t_build = time.time()
    replay_result = build_replay_result(dates, paper_actions, outcomes, failures)
    print(f"  replay_result built in {time.time()-t_build:.1f}s", flush=True)

    # ── 6. Save raw replay_result ──
    print("Saving replay_result...", flush=True)
    Path(args.replay_output).parent.mkdir(exist_ok=True)
    with open(args.replay_output, 'w') as f:
        json.dump(replay_result, f, ensure_ascii=False, default=str)
    replay_size = os.path.getsize(args.replay_output) / (1024 * 1024)
    print(f"  Saved: {args.replay_output} ({replay_size:.1f} MB)", flush=True)

    # ── 7. Compute validation metrics ──
    print(f"Computing validation metrics (horizon={args.horizon})...", flush=True)
    t_metrics = time.time()
    metrics = aggregate_validation_metrics(replay_result=replay_result, horizon=args.horizon)
    failures_analysis = analyze_validation_failures(replay_result=replay_result)
    print(f"  Metrics computed in {time.time()-t_metrics:.1f}s", flush=True)

    # ── 8. Build validation report ──
    all_actions = sum(len(d.get("paper_actions", [])) for d in replay_result.get("daily_results", []))
    all_outcomes = sum(len(d.get("outcomes", [])) for d in replay_result.get("daily_results", []))
    fb_count = sum(1 for d in replay_result.get("daily_results", [])
                   for a in d.get("paper_actions", [])
                   if a.get("source_brd_result", {}).get("fallback") is True)
    fb_rate = round(fb_count / all_actions, 4) if all_actions else None

    # Determine status
    if fb_rate is not None and fb_rate >= 0.05:
        status = "BLOCKED_FALLBACK_RATE_TOO_HIGH"
    elif metrics.get("valid_outcome_count", 0) == 0:
        status = "BLOCKED_NO_VALID_OUTCOMES"
    else:
        status = "STRATEGY_VALIDATION_READY"

    prim = metrics.get("primary", {})
    t5 = metrics.get("t5", {})
    t60 = metrics.get("t60", {})

    summary = {
        "validation_version": "V35_BRD_STRATEGY_VALIDATION_V10",
        "validation_status": status,
        "mode": "HISTORICAL_VALIDATION_ONLY",
        "elapsed_seconds": round(elapsed, 1),
        "throughput": round(throughput, 1),
        "dates_count": len(dates),
        "tickers_count": len(tickers),
        "total_processed": len(tasks),
        "horizon": args.horizon.upper(),
        "workers": args.workers,
        "total_paper_actions": all_actions,
        "total_outcomes": all_outcomes,
        "fallback_rate": fb_rate,
        "brd_connected": True,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        # Primary horizon metrics
        "primary_win_rate": prim.get("win_rate"),
        "primary_average_return": prim.get("average_return"),
        "primary_median_return": prim.get("median_return"),
        "primary_best_return": prim.get("best_return"),
        "primary_worst_return": prim.get("worst_return"),
        "primary_invalidated_rate": prim.get("invalidated_rate"),
        "primary_sample_count": prim.get("sample_count"),
        # T5 metrics
        "t5_win_rate": t5.get("win_rate"),
        "t5_average_return": t5.get("average_return"),
        # T60 metrics
        "t60_win_rate": t60.get("win_rate"),
        "t60_average_return": t60.get("average_return"),
        # Failure analysis
        "failure_analysis": failures_analysis,
    }

    # ── 9. Save validation report ──
    report = {
        "summary": summary,
        "metrics": metrics,
        "failure_analysis": failures_analysis,
        "safety": {
            "real_trade_allowed": False,
            "broker_order_allowed": False,
        },
    }

    Path(args.validation_output).parent.mkdir(exist_ok=True)
    with open(args.validation_output, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Validation report: {args.validation_output}", flush=True)

    # ── 10. Print summary ──
    print("\n" + "=" * 60)
    print(f"  v3.5 Strategy Validation — {status}")
    print("=" * 60)
    print(f"  Tasks:      {len(tasks):,}")
    print(f"  Paper:      {all_actions:,}")
    print(f"  Outcomes:   {all_outcomes:,}")
    print(f"  Fallback:   {fb_rate}")
    print(f"  Horizon:    {args.horizon.upper()}")
    print("-" * 60)
    if prim.get("win_rate") is not None:
        print(f"  Win Rate:   {prim['win_rate']*100:.1f}%")
        print(f"  Avg Return: {prim['average_return']*100:.2f}%")
        print(f"  Med Return: {prim['median_return']*100:.2f}%")
        print(f"  Best:       {prim['best_return']*100:.2f}%")
        print(f"  Worst:      {prim['worst_return']*100:.2f}%")
        print(f"  Invalidated:{prim.get('invalidated_rate',0)*100:.1f}%")
    else:
        print("  ⚠️  No valid returns computed")
    print("=" * 60)

    # Gate check
    if status != "STRATEGY_VALIDATION_READY":
        print(f"\n❌ BLOCKED: {status}")
        sys.exit(3)
    print(f"\n✅ Strategy Validation Complete ({elapsed:.0f}s)")


if __name__ == "__main__":
    main()
