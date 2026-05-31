#!/usr/bin/env python3
"""Run Golden Path for a specific case from registry — writes audit JSON."""
import sys, json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))

def load_case(case_id: str) -> dict:
    registry = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
    for c in registry:
        if c.get("case_id") == case_id:
            return c
    return {}

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--case-id", default="CORE_001")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    case = load_case(args.case_id)
    from zmatrix.research_os.golden_path_runner import run_golden_path

    result = run_golden_path(
        ticker=case.get("ticker", "600519"),
        case_id=case.get("case_id", args.case_id),
        name=case.get("name", ""),
        category=case.get("category", ""),
        industry=case.get("industry", ""),
        sector=case.get("sector", ""),
        chain=case.get("chain", ""),
        style=case.get("style", ""),
        risk=case.get("risk", ""),
        dry_run=args.dry_run,
    )

    case_meta = result.get("_case", {})
    ticker = case_meta.get("ticker", "UNKNOWN")
    status = "COMPLETED" if result.get("_audit_hash") else "PIPELINE_ERROR"

    # Write audit JSON
    out_dir = WORKSPACE / "runtime_reports" / "cases" / "core_12" / f"{args.case_id}_{ticker}"
    out_dir.mkdir(parents=True, exist_ok=True)
    audit = {
        "case_id": args.case_id,
        "ticker": ticker,
        "name": case_meta.get("name", ""),
        "status": status,
        "audit_hash": result.get("_audit_hash", "N/A"),
        "human_report": str(out_dir / f"{args.case_id}_{ticker}_human_report.md"),
        "ticker_specific": True,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (out_dir / f"{args.case_id}_{ticker}_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False))

    print(f"Case: {args.case_id} | Ticker: {ticker} | Status: {status} | Hash: {result.get('_audit_hash', 'N/A')}")

if __name__ == "__main__":
    main()
