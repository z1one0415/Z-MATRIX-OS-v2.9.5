#!/usr/bin/env python3
"""Audit v1.0-D golden hash lock for 4 golden cases.

Reads golden cases JSON, recomputes hashes via v1.0-C skill_hashing,
compares against expected values.
Outputs to stdout only. No runtime_reports.
"""

import json
import sys
from pathlib import Path
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash

GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_d_golden_cases.json"


def main():
    if not GOLDEN_PATH.exists():
        print(f"FAIL: golden cases not found at {GOLDEN_PATH}")
        sys.exit(1)

    golden = json.loads(GOLDEN_PATH.read_text())
    cases = golden.get("cases", [])

    print(f"Golden cases: {len(cases)}")
    for c in cases:
        print(f"  {c['case_id']}: {c['skill_id']}")

    all_passed = True

    print("\n--- Golden Hash Lock Audit ---")
    for c in cases:
        cid = c["case_id"]
        sid = c["skill_id"]
        inp = c["input_payload"]
        out = c["output_payload"]
        exp_ih = c["expected_input_hash"]
        exp_oh = c["expected_output_hash"]

        ih = compute_input_hash(inp)
        oh = compute_output_hash(out)

        ih_ok = ih == exp_ih
        oh_ok = oh == exp_oh
        ok = ih_ok and oh_ok

        print(f"  {cid}: input_hash={'MATCH' if ih_ok else 'MISMATCH'} output_hash={'MATCH' if oh_ok else 'MISMATCH'} => {'PASS' if ok else 'FAIL'}")
        if not ih_ok:
            print(f"    expected: {exp_ih}")
            print(f"    computed: {ih}")
        if not oh_ok:
            print(f"    expected: {exp_oh}")
            print(f"    computed: {oh}")
        if not ok:
            all_passed = False

    print("\n--- Narrative Exclusion Test ---")
    out_narr = dict(cases[0]["output_payload"])
    out_narr["narrative"] = "hello world"
    oh_narr = compute_output_hash(out_narr)
    oh_base = compute_output_hash(cases[0]["output_payload"])
    narr_ok = oh_narr == oh_base
    print(f"  narrative_change_same_hash: {narr_ok} => {'PASS' if narr_ok else 'FAIL'}")

    out_diff = dict(cases[0]["output_payload"])
    out_diff["status"] = "FAILED"
    oh_diff = compute_output_hash(out_diff)
    diff_ok = oh_diff != oh_base
    print(f"  non_narrative_change_diff_hash: {diff_ok} => {'PASS' if diff_ok else 'FAIL'}")

    print(f"\n--- Audit Summary ---")
    print(f"golden_case_count: {len(cases)}")
    print(f"input_hash_match: {all_passed}")
    print(f"output_hash_match: {all_passed}")
    print(f"narrative_exclusion_ok: {narr_ok}")
    print(f"hash_diff_ok: {diff_ok}")
    print(f"runtime_reports_written: 0")

    if all_passed and narr_ok and diff_ok:
        print("Z_SKILLOS_V1_0_D_GOLDEN_HASH_LOCK_PASS")
    else:
        print("Z_SKILLOS_V1_0_D_GOLDEN_HASH_LOCK_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
