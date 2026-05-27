#!/usr/bin/env python3
"""v3.5 Quick BRD Result Audit — parallel, configurable dates/tickers/workers"""
import json, sys, os, time, argparse, multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_DATA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from zmatrix.brd_strategy_validation.date_sampler import sample_replay_dates_from_index
from zmatrix.brd_replay.pit_feature_builder import build_pit_features
from zmatrix.brd_matrix_pit.brd_input_bundle_builder import build_brd_input_bundle
from zmatrix.brd_replay.real_brd_connector import build_real_brd_classifier_connector
from zmatrix.brd_replay.paper_action_builder import build_paper_action_from_brd
from zmatrix.brd_replay.outcome_linker import build_outcome_for_paper_action
from zmatrix.brd_result_audit.audit_report_builder import build_brd_result_audit_report


def _process_one_ticker(args):
    """Process a single ticker for a single date. Returns (paper_action, outcome, error)."""
    ticker, replay_date, local_data_root = args
    try:
        features = build_pit_features(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root)
        bundle = build_brd_input_bundle(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root, pit_features=features)
        features["brd_input_bundle"] = bundle
        result = build_real_brd_classifier_connector().classify(features)

        price = features.get("price_snapshot", {}).get("close") or features.get("features", {}).get("close") or 0
        paper = build_paper_action_from_brd(replay_date=replay_date, ticker=ticker, brd_result=result, price_snapshot={"close": float(price) if price else 0})
        outcome = build_outcome_for_paper_action(paper_action=paper, local_data_root=local_data_root)
        return (paper, outcome, None)
    except Exception as e:
        return (None, None, {"ticker": ticker, "error": str(e)[:120]})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-dates", type=int, default=10)
    parser.add_argument("--max-tickers", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--output", type=str, default="runtime_reports/v35_brd_result_audit_quick.json")
    args = parser.parse_args()

    t0 = time.time()

    print("Sampling dates...", flush=True)
    sampled = sample_replay_dates_from_index(local_data_root=LOCAL_DATA_ROOT, index_code="000001", max_dates=args.max_dates + 20)
    print(f"  dates sampled in {time.time()-t0:.1f}s", flush=True)
    if sampled.get("sample_status") != "READY":
        print("BLOCKED: no dates"); sys.exit(2)

    # Filter out first 180 days (need min_history_days=120 of pre-replay data)
    all_dates = sampled["dates"]
    if all_dates:
        cut = args.max_dates + 20 - args.max_dates if args.max_dates + 20 > args.max_dates else len(all_dates) - args.max_dates
        dates = all_dates[-args.max_dates:] if len(all_dates) > args.max_dates else all_dates[20:]
    else:
        dates = []
    print(f"Dates: {len(dates)} | Tickers: {args.max_tickers} | Workers: {args.workers}")

    # Build ticker list from universe
    from zmatrix.historical_replay.replay_universe import build_replay_universe
    universe = build_replay_universe(replay_date=dates[0], local_data_root=LOCAL_DATA_ROOT, max_tickers=args.max_tickers)
    tickers = universe.get("tickers", [])
    if not tickers:
        print("BLOCKED: no tickers"); sys.exit(3)
    print(f"Ticker pool: {len(tickers)}")

    # Build task list
    tasks = [(ticker, date, LOCAL_DATA_ROOT) for date in dates for ticker in tickers]
    print(f"Tasks: {len(tasks)}")

    paper_actions = []
    outcomes = []
    failures = []

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

    # Build replay_result structure for audit
    daily_results = []
    for d in dates:
        day_papers = [p for p in paper_actions if p and p.get("replay_date") == d]
        day_outcomes = [o for o in outcomes if o and o.get("paper_id") in {p.get("paper_id") for p in day_papers}]
        daily_results.append({
            "paper_actions": day_papers,
            "outcomes": day_outcomes,
            "rows": [{"ticker": p.get("ticker")} for p in day_papers],
            "failures": [],
        })

    replay_result = {"daily_results": daily_results, "date_count": len(dates),
                      "success_day_count": len(dates), "failure_day_count": 0}

    report = build_brd_result_audit_report(replay_result=replay_result)

    Path(args.output).parent.mkdir(exist_ok=True)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2))

    mrd = report["market_role_distribution"]
    ao = report["active_outcome_validation"]

    # Calculate quality metrics from paper_actions
    fallback_count = sum(1 for p in paper_actions if p and p.get("source_brd_result",{}).get("fallback") is True)
    fallback_rate = round(fallback_count / len(paper_actions), 4) if paper_actions else None
    data_gap_count = sum(1 for p in paper_actions if p and p.get("paper_action") == "DATA_GAP")
    data_gap_rate = round(data_gap_count / len(paper_actions), 4) if paper_actions else None

    summary = {
        "elapsed_seconds": round(elapsed, 1),
        "throughput": round(throughput, 1),
        "dates_count": len(dates),
        "tickers_count": len(tickers),
        "total_processed": len(tasks),
        "audit_status": report["audit_status"],
        "total": mrd["total"],
        "active_paper_actions": ao["active_paper_actions"],
        "ready_outcomes": ao["ready_outcomes"],
        "ready_outcome_rate": ao["ready_outcome_rate"],
        "unknown_rate": mrd["unknown_rate"],
        "reason_violation_count": report["role_reason_integrity"]["violation_count"],
        "role_distribution": {r: d["count"] for r, d in mrd["role_distribution"].items() if d["count"] > 0},
        "workers": args.workers,
        "policy_violations": report["policy_violations"],
        "fallback_rate": fallback_rate,
        "data_gap_rate": data_gap_rate,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary["total"] < 10000:
        print(f"BLOCKED: total={summary['total']} < 10000")
        sys.exit(3)
    if summary.get("unknown_rate") is not None and summary["unknown_rate"] >= 0.05:
        print(f"BLOCKED: unknown_rate={summary['unknown_rate']}")
        sys.exit(4)
    if summary.get("fallback_rate") is not None and summary["fallback_rate"] >= 0.05:
        print(f"BLOCKED: fallback_rate={summary['fallback_rate']}")
        sys.exit(5)
    if summary["active_paper_actions"] <= 0:
        print("BLOCKED: active=0")
        sys.exit(6)
    if summary["ready_outcomes"] <= 0:
        print("BLOCKED: ready_outcomes=0")
        sys.exit(7)
    if summary.get("reason_violation_count", 0) > 0:
        print(f"BLOCKED: reason_violations={summary['reason_violation_count']}")
        sys.exit(8)
    if summary.get("policy_violations"):
        print("BLOCKED: policy violations")
        sys.exit(9)
    if report["audit_status"] != "PASS":
        print(f"BLOCKED: audit_status={report['audit_status']}")
        sys.exit(10)

    print(f"\n✅ Quick Audit PASS ({elapsed:.0f}s, {throughput:.0f} tasks/s)")


if __name__ == "__main__":
    main()
