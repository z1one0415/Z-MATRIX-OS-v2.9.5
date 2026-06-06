#!/usr/bin/env python3
"""Audit v1.0-E hash-aware shadow for 4 golden cases.

Reads v1.0-D golden cases, runs hash-aware shadow audit.
Outputs summary to stdout only. No runtime_reports.
"""

import json
import sys
from pathlib import Path
from zmatrix.agent.skill_hash_aware_auditor import audit_hash_aware_batch

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_d_golden_cases.json"


def main():
    if not GOLDEN_PATH.exists():
        print(f"FAIL: {GOLDEN_PATH} not found")
        sys.exit(1)

    golden = json.loads(GOLDEN_PATH.read_text())
    cases = golden["cases"]

    print(f"Golden cases: {len(cases)}")
    for c in cases:
        print(f"  {c['case_id']}: {c['skill_id']}")

    batch = audit_hash_aware_batch(cases)

    print("\n--- Hash-Aware Shadow Audit ---")
    for r in batch["results"]:
        sid = r["skill_id"]
        schema_ok = r["schema_input_valid"] and r["schema_output_valid"]
        golden_ok = r["golden_input_match"] and r["golden_output_match"]
        ok = schema_ok and (golden_ok or not r["golden_case_found"])
        print(f"  {sid}: schema={'PASS' if schema_ok else 'FAIL'} golden={'PASS' if golden_ok else 'MISMATCH' if r['golden_case_found'] else 'NF'} => {'PASS' if ok else 'FAIL'}")
        if r["violations"]:
            for v in r["violations"]:
                print(f"    violation: {v}")

    schema_pass = sum(1 for r in batch["results"] if r["schema_input_valid"] and r["schema_output_valid"])
    golden_match = sum(1 for r in batch["results"] if r["golden_input_match"] and r["golden_output_match"])

    print(f"\n--- Audit Summary ---")
    print(f"case_count: {len(cases)}")
    print(f"schema_input_pass: {schema_pass}/{len(cases)}")
    print(f"schema_output_pass: {schema_pass}/{len(cases)}")
    print(f"golden_input_match: {golden_match}/{len(cases)}")
    print(f"golden_output_match: {golden_match}/{len(cases)}")
    print(f"blocked_count: {batch['blocked_count']}")
    print(f"enforcement: {batch['enforcement']}")
    print(f"runtime_reports_written: 0")

    if batch["all_pass"]:
        print("Z_SKILLOS_V1_0_E_HASH_AWARE_SHADOW_AUDIT_PASS")
    else:
        print("Z_SKILLOS_V1_0_E_HASH_AWARE_SHADOW_AUDIT_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
