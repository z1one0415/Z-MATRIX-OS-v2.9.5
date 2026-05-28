#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.sector_clock_foundation.foundation_report_builder import build_sector_clock_foundation_report

def _load_rows(path):
    p = Path(path)
    if not p.exists(): return []
    report = json.loads(p.read_text(encoding="utf-8"))
    rows = []
    for payload in (report.get("policy_results") or report.get("candidate_results") or {}).values():
        rows.extend(payload.get("kept_rows") or payload.get("kept") or [])
        rows.extend(payload.get("downgraded_rows") or payload.get("downgraded") or [])
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay-report", default="runtime_reports/v357_regime_conditioned_replay_report.json")
    ap.add_argument("--data-root", default=".")
    ap.add_argument("--output", default="runtime_reports/v359_sector_clock_foundation_report.json")
    args = ap.parse_args()
    rows = _load_rows(args.replay_report)
    report = build_sector_clock_foundation_report(replay_rows=rows, data_root=args.data_root)
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    sm = report["sector_mapping_discovery"]; sj = report["stock_sector_join"]; ck = report["matrix_clock_metadata"]
    s = {"report_version":report["report_version"],"foundation_status":report["foundation_status"],"sector_mapping_status":sm["sector_mapping_status"],"ticker_count":sm["ticker_count"],"sector_index_status":report["sector_index_discovery"]["sector_index_status"],"sector_join_status":sj["sector_join_status"],"sector_join_coverage":sj["sector_join_coverage"],"matrix_clock_ready":{k:v.get("metadata_ready") for k,v in ck.items()},"data_decay":{"B":report["data_decay_penalty_preview"]["B"]["decay_status"],"R":report["data_decay_penalty_preview"]["R"]["decay_status"],"D":report["data_decay_penalty_preview"]["D"]["decay_status"]},"policy_violations":report["policy_violations"],"recommended_next_step":report["recommended_next_step"],"real_trade_allowed":report["real_trade_allowed"]}
    print(json.dumps(s, ensure_ascii=False, indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.9 sector clock foundation report generated")

if __name__ == "__main__": main()
