#!/usr/bin/env python3
"""Run Golden Path for a specific case from registry."""
import sys, json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))

def load_case(case_id: str) -> dict:
    registry = json.loads((WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
    for c in registry:
        if c.get("case_id") == case_id:
            return c
    raise ValueError(f"Case not found: {case_id}")

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

    status = "COMPLETED" if result.get("_audit_hash") else "PIPELINE_ERROR"
    print(f"Case: {args.case_id} | Ticker: {result['idea']['ticker']} | Status: {status} | Hash: {result.get('_audit_hash','N/A')}")

if __name__ == "__main__":
    main()
