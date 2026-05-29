#!/usr/bin/env python3
# allowlist: forbidden-token-definition
from __future__ import annotations
import json
from pathlib import Path
from zmatrix.strategy_repair.repair_dataset_loader import load_repair_dataset
from zmatrix.strategy_repair.repair_lab_report import build_strategy_repair_lab_report

def main():
    dataset = load_repair_dataset(replay_path="runtime_reports/v35_brd_strategy_replay_result.json")
    if dataset.get("dataset_status") != "READY":
        print(json.dumps(dataset, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    report = build_strategy_repair_lab_report(joined=dataset["joined"], horizon="t20")
    out = Path("runtime_reports/v352_strategy_repair_lab_report.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"report_version": report.get("report_version"), "policy_violations": report.get("policy_violations"), "recommended_next_step": report.get("recommended_next_step"), "ready_candidates": report.get("repair_verdict", {}).get("ready_candidates"), "pathology_tag_counts": report.get("pathology", {}).get("tag_counts"), "real_trade_allowed": report.get("real_trade_allowed"), "broker_order_allowed": report.get("broker_order_allowed")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report.get("policy_violations"): raise SystemExit(3)
    print("v3.5.2 strategy repair lab report generated")

if __name__ == "__main__":
    main()
