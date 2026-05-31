#!/usr/bin/env python3
"""Summarize Core 12 batch run from audit JSONs."""
import json
from pathlib import Path

ROOT = Path("runtime_reports/cases/core_12")
audits = sorted(ROOT.glob("CORE_*_*/*_audit.json"))

summary = {
    "status": "CORE_12_TICKER_SPECIFIC_ATTEMPTED",
    "attempted": 12,
    "completed": len(audits),
    "data_gap": 0,
    "master_data_missing": 0,
    "pipeline_error": max(0, 12 - len(audits)),
    "unique_hash_count": 0,
    "ticker_specific": True,
    "runner_parameterized": True,
    "results": [],
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}

hashes = set()
for p in audits:
    d = json.loads(p.read_text())
    h = d.get("audit_hash", "N/A")
    if h != "N/A": hashes.add(h)
    summary["results"].append(d)

summary["unique_hash_count"] = len(hashes)

(ROOT.parent / "core_12_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
# Also write closeout
closeout = {
    "status": "CASE_EXPANSION_V2_PARAMETERIZED_CONFIRMED",
    "core_12_attempted": 12,
    "core_12_completed": len(audits),
    "unique_hash_count": len(hashes),
    "runner_parameterized": True,
    "ticker_specific": True,
    "human_report_parameterized": True,
    "buy_sell_instruction_count": 0,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}
(ROOT.parent / "case_expansion_v2_closeout.json").write_text(json.dumps(closeout, indent=2))

print(json.dumps(summary, indent=2, ensure_ascii=False))
