#!/usr/bin/env python3
# allowlist: forbidden-token-definition
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.entry_quality_repair.dataset_loader import load_entry_repair_dataset
from zmatrix.entry_quality_repair.repair_report_builder import build_entry_quality_repair_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--output", default="runtime_reports/v355_entry_quality_repair_report.json")
    args = ap.parse_args()
    dataset = load_entry_repair_dataset(replay_path="runtime_reports/v35_brd_strategy_replay_result.json", role_filter="B_MID_ROTATION")
    if dataset.get("dataset_status") != "READY":
        print(json.dumps(dataset, ensure_ascii=False, indent=2)); raise SystemExit(2)
    report = build_entry_quality_repair_report(joined=dataset["joined"], data_root=".", horizon="t20", max_items=args.max_items)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"report_version": report.get("report_version"), "input_count": report.get("input_count"), "feature_ready_count": report.get("feature_ready_count"), "feature_ready_rate": report.get("feature_ready_rate"), "archetype_counts": report.get("archetype_counts"), "entry_quality_bucket_counts": report.get("entry_quality_bucket_counts"), "baseline": report.get("entry_rule_replay", {}).get("baseline"), "ready_candidates": report.get("ready_candidates"), "candidate_verdict": report.get("candidate_verdict", {}).get("verdicts"), "policy_violations": report.get("policy_violations"), "production_strategy_modified": report.get("production_strategy_modified"), "real_trade_allowed": report.get("real_trade_allowed"), "broker_order_allowed": report.get("broker_order_allowed")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report.get("policy_violations"): raise SystemExit(3)
    print("v3.5.5 entry quality repair lab report generated")

if __name__ == "__main__": main()
