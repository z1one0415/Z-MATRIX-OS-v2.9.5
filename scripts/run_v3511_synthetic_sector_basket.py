#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.synthetic_sector_index.sector_basket_report_builder import build_synthetic_sector_basket_report

def _load_rows(path):
    p = Path(path)
    if not p.exists(): return []
    report = json.loads(p.read_text(encoding="utf-8"))
    rows = []
    for daily in report.get("daily_results", []):
        for a in daily.get("paper_actions", []):
            if a.get("role") == "B_MID_ROTATION" and a.get("paper_action") not in ("NO_ACTION", "DATA_GAP", None):
                rows.append(a)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=".")
    ap.add_argument("--mapping-path", default="data/metadata/sector_mapping_v3510.csv")
    ap.add_argument("--replay-report", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--output", default="runtime_reports/v3511_synthetic_sector_basket_report.json")
    args = ap.parse_args()
    rows = _load_rows(args.replay_report)
    report = build_synthetic_sector_basket_report(data_root=args.data_root, replay_rows=rows, mapping_path=args.mapping_path, write_artifacts=True)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    s = {"report_version":report["report_version"],"basket_status":report["basket_status"],"sector_count":report["sector_mapping_loader"]["sector_count"],"sector_index_count":report["synthetic_sector_index_builder"]["sector_index_count"],"benchmark_status":report["market_benchmark_loader"]["benchmark_status"],"benchmark_code":report["market_benchmark_loader"]["benchmark_code"],"replay_join_status":report["replay_sector_feature_joiner"]["join_status"],"replay_join_coverage":report["replay_sector_feature_joiner"]["join_coverage"],"missing_price_file_count":report["sector_daily_return_builder"]["missing_price_file_count"],"policy_violations":report["policy_violations"],"recommended_next_step":report["recommended_next_step"],"real_trade_allowed":report["real_trade_allowed"]}
    print(json.dumps(s, ensure_ascii=False, indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.11 synthetic sector basket report generated")

if __name__ == "__main__": main()
