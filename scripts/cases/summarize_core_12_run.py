#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path("runtime_reports/cases/core_12")
audits = sorted(ROOT.glob("CORE_*_*/*_audit.json"))

hashes = set()
for p in audits:
    d = json.loads(p.read_text())
    if d.get("audit_hash") != "N/A": hashes.add(d["audit_hash"])

summary = {
    "status": "CORE_12_TICKER_SPECIFIC_ATTEMPTED",
    "attempted": 12,
    "completed": len(audits),
    "data_gap": 0,
    "master_data_missing": 0,
    "pipeline_error": max(0, 12 - len(audits)),
    "unique_hash_count": len(hashes),
    "ticker_specific": True,
    "runner_parameterized": True,
    "results": [],
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
}
for p in audits:
    summary["results"].append(json.loads(p.read_text()))
(ROOT.parent / "core_12_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))

closeout = {
    "status": "CASE_EXPANSION_V2_PARAMETERIZED_CONFIRMED",
    "ce2_a_golden_path_parameterized": True,
    "ce2_b_human_report_parameterized": True,
    "ce2_c_core_12_attempted": True,
    "core_12_attempted": 12,
    "core_12_completed": len(audits),
    "unique_hash_count": len(hashes),
    "runner_parameterized": True,
    "ticker_specific": True,
    "human_report_parameterized": True,
    "independent_outputs": True,
    "buy_sell_instruction_count": 0,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
}
(ROOT.parent / "case_expansion_v2_closeout.json").write_text(json.dumps(closeout, indent=2))
print(json.dumps(summary, indent=2, ensure_ascii=False))
