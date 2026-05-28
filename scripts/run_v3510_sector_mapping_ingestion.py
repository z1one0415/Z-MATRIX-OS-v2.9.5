#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.sector_mapping_ingestion.ingestion_report_builder import build_sector_mapping_ingestion_report

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
    ap.add_argument("--replay-report", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--output", default="runtime_reports/v3510_sector_mapping_ingestion_report.json")
    args = ap.parse_args()
    rows = _load_rows(args.replay_report)
    report = build_sector_mapping_ingestion_report(data_root=args.data_root, replay_rows=rows, write_artifact=True)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"report_version":report["report_version"],"ingestion_status":report["ingestion_status"],"source_count":report["source_discovery"]["source_count"],"sector_mapping_status":report["mapping_validator"]["sector_mapping_status"],"ticker_count":report["mapping_validator"]["ticker_count"],"sector_ready_count":report["mapping_validator"]["sector_ready_count"],"sector_coverage":report["mapping_validator"]["sector_coverage"],"sector_count":report["mapping_validator"]["sector_count"],"replay_join_status":report["replay_sector_join_validator"]["join_status"],"replay_join_coverage":report["replay_sector_join_validator"]["join_coverage"],"artifact_path":report["mapping_artifact_writer"].get("output_path"),"artifact_size_bytes":report["mapping_artifact_writer"].get("size_bytes"),"artifact_git_track_allowed":report["mapping_artifact_writer"].get("git_track_allowed"),"policy_violations":report["policy_violations"],"recommended_next_step":report["recommended_next_step"],"real_trade_allowed":report["real_trade_allowed"]}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.10 sector mapping ingestion report generated")

if __name__ == "__main__": main()
