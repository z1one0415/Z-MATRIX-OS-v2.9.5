#!/usr/bin/env python3
"""v3.5.1 Return Integrity Report — robust performance attribution"""
from __future__ import annotations
import json
from pathlib import Path

from zmatrix.return_integrity.return_integrity_report import build_return_integrity_report

def main():
    replay_path = Path("runtime_reports/v35_brd_strategy_replay_result.json")
    audit_path = Path("runtime_reports/2026-05-27_v35_brd_full_market_audit_result.json")

    if not replay_path.exists():
        print("BLOCKED: replay result missing")
        raise SystemExit(2)

    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.exists() else {}

    paper_actions = []
    outcomes = []
    for daily in replay.get("daily_results", []):
        paper_actions.extend(daily.get("paper_actions", []))
        outcomes.extend(daily.get("outcomes", []))

    if not paper_actions or not outcomes:
        print("BLOCKED: paper_actions/outcomes missing")
        raise SystemExit(3)

    report = build_return_integrity_report(outcomes=outcomes, paper_actions=paper_actions, audit_report=audit, horizon="t20")

    out_path = Path("runtime_reports/v36_return_integrity_report.json")
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    rm = report["robust_metrics"]
    sv = report["strategy_verdict"]
    oa = report["outlier_attribution"]

    top_winner = oa["top_winners"][0] if oa.get("top_winners") else {}
    top_loser = oa["top_losers"][0] if oa.get("top_losers") else {}

    print(json.dumps({
        "performance_status": sv["performance_status"],
        "valid_return_count": rm["valid_return_count"],
        "win_rate": rm["win_rate"],
        "mean": rm["mean"],
        "median": rm["median"],
        "trimmed_mean_5pct": rm["trimmed_mean_5pct"],
        "winsorized_mean_5pct": rm["winsorized_mean_5pct"],
        "top_1pct_contribution": rm["top_1pct_contribution"],
        "top_winner_ticker": top_winner.get("ticker"),
        "top_winner_return": top_winner.get("return"),
        "top_loser_ticker": top_loser.get("ticker"),
        "top_loser_return": top_loser.get("return"),
        "policy_violations": report["policy_violations"],
        "real_trade_allowed": report["real_trade_allowed"],
        "broker_order_allowed": report["broker_order_allowed"],
    }, ensure_ascii=False, indent=2))

    if report["policy_violations"]:
        raise SystemExit(4)

    print("v3.5.1 return integrity report generated")

if __name__ == "__main__":
    main()
