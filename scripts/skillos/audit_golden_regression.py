#!/usr/bin/env python3
"""Audit v1.0-F golden regression cases.

Verifies 12 registry-exact regression cases.
Outputs to stdout only. No runtime_reports.
"""

import json
import sys
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
from zmatrix.agent.skill_contract_registry import get_skill_contract

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_f_golden_regression_cases.json"


def main():
    if not GOLDEN_PATH.exists():
        print(f"FAIL: {GOLDEN_PATH} not found")
        sys.exit(1)

    golden = json.loads(GOLDEN_PATH.read_text())
    cases = golden.get("cases", [])

    print(f"Regression cases: {len(cases)}")
    domains = {c["domain"] for c in cases}
    print(f"Domains covered: {len(domains)}")

    all_pass = True
    match_count = 0

    print("\n--- Regression Audit ---")
    for c in cases:
        sid = c["skill_id"]
        # Verify skill exists in registry
        contract = get_skill_contract(sid)
        registry_ok = contract is not None

        ih = compute_input_hash(c["input_payload"])
        oh = compute_output_hash(c["output_payload"])
        ih_ok = ih == c["expected_input_hash"]
        oh_ok = oh == c["expected_output_hash"]
        ok = ih_ok and oh_ok and registry_ok

        if ok:
            match_count += 1
        else:
            all_pass = False
            issues = []
            if not registry_ok:
                issues.append("not in contract registry")
            if not ih_ok:
                issues.append("input_hash mismatch")
            if not oh_ok:
                issues.append("output_hash mismatch")

        print(f"  {sid}: registry={'OK' if registry_ok else 'MISSING'} hash={'MATCH' if ok else 'FAIL'}")
        if not ok:
            for i in issues:
                print(f"    issue: {i}")

    print(f"\n--- Summary ---")
    print(f"case_count: {len(cases)}")
    print(f"domains_covered: {len(domains)}")
    print(f"hash_match: {match_count}/{len(cases)}")
    print(f"runtime_reports_written: 0")

    if all_pass:
        print("Z_SKILLOS_V1_0_F_GOLDEN_REGRESSION_PASS")
    else:
        print("Z_SKILLOS_V1_0_F_GOLDEN_REGRESSION_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
