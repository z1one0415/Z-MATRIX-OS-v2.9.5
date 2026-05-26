#!/usr/bin/env python3
"""v3.5 BRD Result Audit — run on real replay data"""
import json, sys
from pathlib import Path
from zmatrix.brd_strategy_validation.date_sampler import sample_replay_dates_from_index
from zmatrix.brd_replay.multi_day_runner import run_multi_day_brd_strategy_replay
from zmatrix.brd_result_audit.audit_report_builder import build_brd_result_audit_report

def main():
    sampled = sample_replay_dates_from_index(local_data_root=".",index_code="000001",max_dates=3)
    if sampled.get("sample_status")!="READY": print("BLOCKED"); sys.exit(2)
    replay = run_multi_day_brd_strategy_replay(replay_dates=sampled["dates"],local_data_root=".",max_tickers=200)
    report = build_brd_result_audit_report(replay_result=replay)
    out = Path("runtime_reports"); out.mkdir(exist_ok=True)
    (out/"v35_brd_result_audit_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    summary = {"audit_status":report["audit_status"],"total":report["market_role_distribution"]["total"],
        "role_distribution":report["market_role_distribution"]["role_distribution"],
        "active_paper_actions":report["active_outcome_validation"]["active_paper_actions"],
        "ready_outcomes":report["active_outcome_validation"]["ready_outcomes"],
        "ready_outcome_rate":report["active_outcome_validation"]["ready_outcome_rate"],
        "reason_violation_count":report["role_reason_integrity"]["violation_count"],
        "policy_violations":report["policy_violations"]}
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    if report["audit_status"]!="PASS": print(f"BLOCKED: {report['audit_status']}"); sys.exit(3)
    if report["policy_violations"]: print("BLOCKED: policy"); sys.exit(4)
    print("v3.5 BRD Result Audit PASS")

if __name__=="__main__": main()
