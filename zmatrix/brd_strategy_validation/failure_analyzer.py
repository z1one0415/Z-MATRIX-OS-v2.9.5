# allowlist: forbidden-token-definition
"""Failure Analyzer — count fallback/data_gap/no_action/insufficient"""
from __future__ import annotations

def analyze_validation_failures(*, replay_result):
    actions, outcomes, failures = [], [], []
    for daily in replay_result.get("daily_results",[]):
        actions.extend(daily.get("paper_actions",[]))
        outcomes.extend(daily.get("outcomes",[]))
        failures.extend(daily.get("failures",[]))
    fb = [a for a in actions if a.get("source_brd_result",{}).get("fallback") is True]
    dg = [a for a in actions if a.get("paper_action")=="DATA_GAP"]
    na = [a for a in actions if a.get("paper_action")=="NO_ACTION"]
    insuf = [o for o in outcomes if o.get("outcome_status") in ("INSUFFICIENT_DATA","INSUFFICIENT_FORWARD_DATA")]
    ready = [o for o in outcomes if o.get("outcome_status")=="READY"]
    return {"failure_analysis_version":"V35_FAILURE_ANALYSIS_V10","failure_count":len(failures),
            "paper_action_count":len(actions),"outcome_count":len(outcomes),
            "fallback_count":len(fb),"fallback_rate":len(fb)/len(actions) if actions else None,
            "data_gap_count":len(dg),"no_action_count":len(na),
            "insufficient_outcome_count":len(insuf),"ready_outcome_count":len(ready),
            "real_trade_allowed":False,"broker_order_allowed":False}
