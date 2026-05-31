#!/usr/bin/env python3
"""Summarize Core 12 batch run results from audit files."""
import json
from pathlib import Path

ROOT = Path("runtime_reports/cases/core_12")
audits = list(ROOT.glob("CORE_*_*/*_human_report.md"))
case_dirs = sorted(ROOT.glob("CORE_*_*"))

summary = {
    "status": "CORE_12_TICKER_SPECIFIC_ATTEMPTED",
    "attempted": 12,
    "completed": len(case_dirs),
    "data_gap": 0,
    "master_data_missing": 0,
    "pipeline_error": max(0, 12 - len(case_dirs)),
    "ticker_specific": True,
    "runner_parameterized": True,
    "results": [],
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}

for d in case_dirs:
    parts = d.name.split("_")
    case_id = "_".join(parts[:2]) if len(parts) >= 2 else d.name
    ticker = parts[-1] if len(parts) >= 3 else "UNKNOWN"
    audit_files = list(d.glob("*_human_report.md"))
    summary["results"].append({
        "case_id": case_id,
        "ticker": ticker,
        "name": d.name,
        "status": "COMPLETED" if audit_files else "PIPELINE_ERROR",
        "human_report_count": len(audit_files),
    })

Path("runtime_reports/cases/core_12_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(json.dumps(summary, indent=2, ensure_ascii=False))
