#!/usr/bin/env python3
"""Audit v1.1-C golden coverage: 24 cases, >=16 domains."""

import json, sys
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
from zmatrix.agent.skill_contract_registry import get_skill_contract

P = Path(__file__).resolve().parent.parent.parent / "data/research_db/agent/golden/skillos_v1_1_c_golden_regression_cases_24.json"


def main():
    if not P.exists():
        print(f"FAIL: {P} not found"); sys.exit(1)
    g = json.loads(P.read_text())
    cases = g["cases"]
    errors = []

    if len(cases) != 24:
        errors.append(f"case_count={len(cases)}, expected 24")
    ids = [c["skill_id"] for c in cases]
    if len(set(ids)) != len(ids):
        errors.append(f"duplicate skill_ids")
    domains = {c["domain"] for c in cases}
    if len(domains) < 16:
        errors.append(f"domains={len(domains)}, expected >=16")

    for c in cases:
        sid = c["skill_id"]
        if not get_skill_contract(sid):
            errors.append(f"{sid}: not in registry")
        ih = compute_input_hash(c["input_payload"])
        oh = compute_output_hash(c["output_payload"])
        if ih != c["expected_input_hash"]:
            errors.append(f"{sid}: input_hash mismatch")
        if oh != c["expected_output_hash"]:
            errors.append(f"{sid}: output_hash mismatch")

    plural = "s" if len(errors) != 1 else ""
    print(f"Cases: {len(cases)}, Domains: {len(domains)}")
    print(f"Errors: {len(errors)}" + (f": {errors[0]}" if len(errors) == 1 else ""))

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        print("Z_SKILLOS_V1_1_C_GOLDEN_COVERAGE_EXPANSION_FAIL_CI")
        sys.exit(1)
    else:
        print("Z_SKILLOS_V1_1_C_GOLDEN_COVERAGE_EXPANSION_PASS")


if __name__ == "__main__":
    main()
