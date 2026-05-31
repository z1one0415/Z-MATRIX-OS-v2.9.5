#!/usr/bin/env python3
"""Run all 12 CORE cases in a single Python process — no shell loops, no pyc races."""
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

def main():
    registry = json.loads((WORKSPACE / "data/research_db/cases/case_registry_v1.json").read_text())
    from zmatrix.research_os.golden_path_runner import run_golden_path

    for c in registry:
        if c.get("case_layer") != "CORE":
            continue
        cid = c["case_id"]
        ticker = c["ticker"]

        result = run_golden_path(
            ticker=ticker, case_id=cid, name=c["name"],
            industry=c["industry"], sector=c["sector"], chain=c["chain"],
            style=c.get("style", ""), risk=c.get("risk", ""), dry_run=True,
        )

        case_meta = result.get("_case", {})
        status = "COMPLETED" if result.get("_audit_hash") else "PIPELINE_ERROR"

        # Write audit JSON with relative path
        report_rel = f"runtime_reports/cases/core_12/{cid}_{ticker}/{cid}_{ticker}_human_report.md"
        audit = {
            "case_id": cid, "ticker": ticker, "name": case_meta.get("name", ""),
            "status": status, "audit_hash": result.get("_audit_hash", "N/A"),
            "human_report": report_rel, "ticker_specific": True,
            "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
        }
        audit_file = WORKSPACE / "runtime_reports" / "cases" / "core_12" / f"{cid}_{ticker}" / f"{cid}_{ticker}_audit.json"
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        audit_file.write_text(json.dumps(audit, indent=2, ensure_ascii=False))

        print(f"Case: {cid} | Ticker: {ticker} | Status: {status} | Hash: {result.get('_audit_hash', 'N/A')}")

if __name__ == "__main__":
    main()
