"""Validation Runner — multi-day B/R/D strategy validation"""
from __future__ import annotations
from datetime import datetime, timezone
from zmatrix.brd_replay.multi_day_runner import run_multi_day_brd_strategy_replay
from zmatrix.brd_strategy_validation.metrics_aggregator import aggregate_validation_metrics
from zmatrix.brd_strategy_validation.failure_analyzer import analyze_validation_failures
from zmatrix.brd_strategy_validation.schema import DEFAULT_VALIDATION_SAFETY

def run_brd_5y_strategy_validation(*, replay_dates, local_data_root=".", max_tickers=None, benchmark_code=None, horizon="t20"):
    started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    replay = run_multi_day_brd_strategy_replay(replay_dates=replay_dates, local_data_root=local_data_root, max_tickers=max_tickers, benchmark_code=benchmark_code)
    metrics = aggregate_validation_metrics(replay_result=replay, horizon=horizon)
    failures = analyze_validation_failures(replay_result=replay)

    # Calculate fallback rate
    all_actions = []
    for daily in replay.get("daily_results",[]):
        for a in daily.get("paper_actions",[]):
            fb = a.get("source_brd_result",{}).get("fallback") is True
            if fb: all_actions.append(a)
    fallback_rate = len(all_actions) / sum(len(d.get("paper_actions",[])) for d in replay.get("daily_results",[])) if any(d.get("paper_actions") for d in replay.get("daily_results",[])) else None

    brd_connected = any(
        a.get("source_brd_result",{}).get("brd_connected") is True
        for d in replay.get("daily_results",[]) for a in d.get("paper_actions",[]) if a.get("source_brd_result")
    )

    if not brd_connected: status = "BLOCKED_BRD_NOT_CONNECTED"
    elif fallback_rate is not None and fallback_rate >= 0.05: status = "BLOCKED_FALLBACK_RATE_TOO_HIGH"
    elif metrics.get("valid_outcome_count",0) == 0: status = "BLOCKED_NO_VALID_OUTCOMES"
    else: status = "STRATEGY_VALIDATION_REPORT_READY"

    return {"validation_version":"V35_BRD_5Y_STRATEGY_VALIDATION_V10","mode":"HISTORICAL_VALIDATION_ONLY",
            "started_at":started_at,"finished_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "date_count":len(replay_dates or[]),"max_tickers":max_tickers,"horizon":horizon.upper(),
            "validation_status":status,"brd_connected":brd_connected,"fallback_rate":fallback_rate,
            "metrics":metrics,"failure_analysis":failures,
            "source_replay_result":replay,
            "safety":dict(DEFAULT_VALIDATION_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False,
            "auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False}
