# allowlist: forbidden-token-definition
"""Single Day BRD Strategy Replay — universe→features→BRD→paper→outcome"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from zmatrix.historical_replay.replay_universe import build_replay_universe
from zmatrix.brd_replay.pit_feature_builder import build_pit_features
from zmatrix.brd_replay.brd_classifier_adapter import run_brd_classifier_adapter
from zmatrix.brd_replay.paper_action_builder import build_paper_action_from_brd
from zmatrix.brd_matrix_pit.brd_input_bundle_builder import build_brd_input_bundle
from zmatrix.brd_replay.outcome_linker import build_outcome_for_paper_action

def run_single_day_brd_strategy_replay(*, replay_date, local_data_root, max_tickers=None, benchmark_code=None, classifier=None):
    universe = build_replay_universe(replay_date=replay_date, local_data_root=local_data_root, max_tickers=max_tickers)
    rows, paper_actions, outcomes, failures = [], [], [], []
    for ticker in universe.get("tickers",[]):
        try:
            features = build_pit_features(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root)
            bundle = build_brd_input_bundle(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root, pit_features=features)
            features["brd_input_bundle"] = bundle
            brd = run_brd_classifier_adapter(ticker=ticker, replay_date=replay_date, pit_features=features, classifier=classifier)
            price = features.get("price_snapshot",{})
            paper = build_paper_action_from_brd(replay_date=replay_date, ticker=ticker, brd_result=brd, price_snapshot=price)
            outcome = build_outcome_for_paper_action(paper_action=paper, local_data_root=local_data_root, benchmark_code=benchmark_code)
            rows.append({"ticker":ticker,"features_status":features.get("feature_status"),"input_ready":bundle.get("input_ready"),
                         "b_status":bundle.get("b_matrix",{}).get("status"),"r_status":bundle.get("r_matrix",{}).get("status"),
                         "d_status":bundle.get("d_matrix",{}).get("status"),
                         "role":brd.get("role"),"brd_score":brd.get("brd_score"),
                         "paper_action":paper.get("paper_action"),"outcome_status":outcome.get("outcome_status")})
            paper_actions.append(paper); outcomes.append(outcome)
        except Exception as e: failures.append({"ticker":ticker,"error":str(e)[:120]})
    seed = f"{replay_date}|{len(rows)}|{len(failures)}"
    replay_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {"strategy_replay_version":"BRD_STRATEGY_REPLAY_DAILY_V10","mode":"HISTORICAL_STRATEGY_VALIDATION_ONLY",
            "replay_id":replay_id,"replay_date":replay_date,
            "created_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "universe_count":len(universe.get("tickers",[])),"processed_count":len(rows),
            "failure_count":len(failures),"rows":rows,"paper_actions":paper_actions,
            "outcomes":outcomes,"failures":failures,"universe":universe,
            "real_trade_allowed":False,"broker_order_allowed":False,
            "auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False}
