#!/usr/bin/env python3
"""v3.5 Full-Market BRD Result Audit — 60 dates, all tickers"""
import json, sys
from pathlib import Path
from zmatrix.brd_strategy_validation.date_sampler import sample_replay_dates_from_index
from zmatrix.brd_replay.multi_day_runner import run_multi_day_brd_strategy_replay
from zmatrix.brd_result_audit.audit_report_builder import build_brd_result_audit_report

def main():
    sampled = sample_replay_dates_from_index(local_data_root=".", index_code="000001", max_dates=60)
    if sampled.get("sample_status") != "READY":
        print("BLOCKED: no dates"); sys.exit(2)
    dates = sampled["dates"]
    print(f"Replay dates: {len(dates)}")
    print(f"Mode: FULL-MARKET (all tickers)")
    
    replay = run_multi_day_brd_strategy_replay(replay_dates=dates, local_data_root=".", max_tickers=None)
    report = build_brd_result_audit_report(replay_result=replay)
    
    out = Path("runtime_reports"); out.mkdir(exist_ok=True)
    (out/"v35_full_market_audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    
    mrd = report["market_role_distribution"]
    ao = report["active_outcome_validation"]
    rri = report["role_reason_integrity"]
    
    summary = {
        "audit_status": report["audit_status"],
        "total": mrd["total"],
        "active_paper_actions": ao["active_paper_actions"],
        "ready_outcomes": ao["ready_outcomes"],
        "ready_outcome_rate": ao["ready_outcome_rate"],
        "unknown_rate": mrd["unknown_rate"],
        "reason_violation_count": rri["violation_count"],
        "role_distribution": {r: d["count"] for r, d in mrd["role_distribution"].items() if d["count"] > 0},
        "policy_violations": report["policy_violations"],
        "date_count": len(dates),
    }
    
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # Validation gates
    if report["audit_status"] != "PASS":
        print(f"BLOCKED: audit_status={report['audit_status']}")
        sys.exit(3)
    
    # Extra checks for full-market
    if mrd["total"] < 1000:
        print(f"BLOCKED: total={mrd['total']} < 1000")
        sys.exit(4)
    if ao["active_paper_actions"] == 0:
        print("BLOCKED: active_paper_actions=0")
        sys.exit(5)
    
    print("\n✅ BRD Result Audit Full-Market PASS")

if __name__ == "__main__":
    main()
