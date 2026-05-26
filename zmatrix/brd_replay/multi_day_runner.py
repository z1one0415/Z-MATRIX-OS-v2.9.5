"""Multi-Day BRD Strategy Replay Runner"""
from __future__ import annotations
from zmatrix.brd_replay.single_day_strategy_replay import run_single_day_brd_strategy_replay

def run_multi_day_brd_strategy_replay(*, replay_dates, local_data_root, max_tickers=None, benchmark_code=None):
    daily, failures = [], []
    for d in replay_dates or []:
        try: daily.append(run_single_day_brd_strategy_replay(replay_date=d,local_data_root=local_data_root,max_tickers=max_tickers,benchmark_code=benchmark_code))
        except Exception as e: failures.append({"replay_date":d,"error":str(e)[:160]})
    total_paper = sum(len(x.get("paper_actions",[])) for x in daily)
    return {"multi_day_replay_version":"BRD_STRATEGY_REPLAY_MULTI_DAY_V10","mode":"HISTORICAL_STRATEGY_VALIDATION_ONLY",
            "date_count":len(replay_dates or[]),"success_day_count":len(daily),"failure_day_count":len(failures),
            "total_paper_actions":total_paper,"daily_results":daily,"failures":failures,
            "real_trade_allowed":False,"broker_order_allowed":False}
