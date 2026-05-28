from __future__ import annotations
from zmatrix.regime_conditioned_replay.regime_feature_loader import load_regime_features
from zmatrix.regime_conditioned_replay.regime_policy_replay import run_regime_policy_replay
from zmatrix.regime_conditioned_replay.candidate_verdict import judge_all_replay_candidates
from zmatrix.regime_conditioned_replay.policy import validate_regime_replay_report
from zmatrix.regime_conditioned_replay.schema import DEFAULT_REGIME_REPLAY_SAFETY

def build_replay_report(*, joined: list[dict], data_root: str = ".", max_items: int | None = None) -> dict:
    features = load_regime_features(joined=joined, data_root=data_root, max_items=max_items)
    rows = features["rows"]
    replay = run_regime_policy_replay(rows=rows)
    verdict = judge_all_replay_candidates(replay=replay)
    ready = verdict.get("ready_policies",[])
    next_step = "v3.5.8 Regime Policy Observation Portfolio Simulation" if ready else "v3.5.8 B-Matrix / Role Definition Reconstruction"
    report = {"report_version":"V357_REGIME_CONDITIONED_REPLAY_REPORT_V10","mode":"PAPER_ONLY_REGIME_REPLAY","input_count":len(joined),"feature_ready_count":len(rows),"feature_ready_rate":len(rows)/len(joined) if joined else None,"baseline_raw":replay["baseline_raw"],"policy_results":replay["policy_results"],"candidate_verdict":verdict,"full_sample_pass_policies":ready,"ready_policies":[],"anti_overfit_validation_status":"PENDING","stability_validated_policies":[],"recommended_next_step":"v3.5.7 closeout: anti-overfit validation required" if ready else "v3.5.8 B-Matrix Reconstruction","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_REGIME_REPLAY_SAFETY)}
    report["policy_violations"] = validate_regime_replay_report(report)
    return report
