#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.invalidation_anatomy.invalidation_event_builder import load_replay_joined
from zmatrix.invalidation_anatomy.anatomy_report_builder import build_invalidation_anatomy_report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-items", type=int, default=None)
    ap.add_argument("--output", default="runtime_reports/v354_invalidation_anatomy_report.json")
    args = ap.parse_args()
    dataset = load_replay_joined(replay_path="runtime_reports/v35_brd_strategy_replay_result.json")
    if dataset.get("dataset_status") != "READY":
        print(json.dumps(dataset, ensure_ascii=False, indent=2)); raise SystemExit(2)
    report = build_invalidation_anatomy_report(joined=dataset["joined"], data_root=".", max_items=args.max_items)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"report_version": report.get("report_version"), "input_count": report.get("input_count"), "invalidation_event_count": report.get("invalidation_event_count"), "invalidation_event_rate": report.get("invalidation_event_rate"), "path_type_counts": report.get("path_type_counts"), "separability_status": report.get("separability", {}).get("separability_status"), "separability_score": report.get("separability", {}).get("separability_score"), "top_discriminating_features": [x.get("feature") for x in report.get("separability", {}).get("top_discriminating_features", [])[:5]], "candidate_count": report.get("conditional_invalidation_candidates", {}).get("candidate_count"), "candidates": [c.get("candidate_name") for c in report.get("conditional_invalidation_candidates", {}).get("candidates", [])], "policy_violations": report.get("policy_violations"), "production_strategy_modified": report.get("production_strategy_modified"), "real_trade_allowed": report.get("real_trade_allowed"), "broker_order_allowed": report.get("broker_order_allowed")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report.get("policy_violations"): raise SystemExit(3)
    print("v3.5.4 invalidation anatomy lab report generated")

if __name__ == "__main__": main()
