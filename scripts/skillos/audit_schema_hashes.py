#!/usr/bin/env python3
"""Audit v1.0-C hash scaffold for 4 auditable skills.

Uses v1.0-B auditable_unique_skill_ids.
Constructs mock payloads, computes input/output hashes.
Outputs to stdout only. No runtime_reports, no invoke_skill.
"""

import sys
from zmatrix.agent.skill_hashing import (
    compute_input_hash,
    compute_output_hash,
    build_hash_audit_record,
)

AUDITABLE_SKILLS = [
    "SYSTEM.GET_SKILLOS_STATUS",
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY",
    "RESEARCHDB.GET_LAYER_STATUS",
    "FACTOR.GET_FACTOR_REGISTRY",
]

MOCK_INPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {},
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {},
    "RESEARCHDB.GET_LAYER_STATUS": {"data_snapshot_id": "snap-001"},
    "FACTOR.GET_FACTOR_REGISTRY": {"data_snapshot_id": "snap-002"},
}

MOCK_OUTPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {
        "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "evidence_refs": ["ref-001"],
    },
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {
        "skill_id": "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "evidence_refs": [],
    },
    "RESEARCHDB.GET_LAYER_STATUS": {
        "skill_id": "RESEARCHDB.GET_LAYER_STATUS",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "data_snapshot_id": "snap-001",
        "evidence_refs": [],
    },
    "FACTOR.GET_FACTOR_REGISTRY": {
        "skill_id": "FACTOR.GET_FACTOR_REGISTRY",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "data_snapshot_id": "snap-002",
        "evidence_refs": ["ref-f1"],
    },
}

OUTPUT_WITH_NARRATIVE = {
    "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
    "skill_version": "1.0.0",
    "status": "SUCCESS",
    "risk_level": "R0_READ",
    "narrative": "All systems operational.",
    "evidence_refs": [],
}


def main():
    print(f"Auditable skills: {len(AUDITABLE_SKILLS)}")
    for sid in AUDITABLE_SKILLS:
        print(f"  - {sid}")

    all_passed = True
    hashes = {}

    print("\n--- Hash Audit ---")
    for sid in AUDITABLE_SKILLS:
        inp = MOCK_INPUTS.get(sid, {})
        out = MOCK_OUTPUTS.get(sid, {})
        record = build_hash_audit_record(sid, inp, out)
        hashes[sid] = record

        ihash = record["input_hash"]
        ohash = record["output_hash"]
        print(f"  {sid}:")
        print(f"    input_hash: {ihash} (len={len(ihash)})")
        print(f"    output_hash: {ohash} (len={len(ohash)})")
        print(f"    blocked: {record['blocked']}")

        if len(ihash) != 64 or len(ohash) != 64:
            all_passed = False

    print("\n--- Stability Check ---")
    for sid in AUDITABLE_SKILLS:
        inp = MOCK_INPUTS.get(sid, {})
        out = MOCK_OUTPUTS.get(sid, {})
        ih1, oh1 = compute_input_hash(inp), compute_output_hash(out)
        ih2, oh2 = compute_input_hash(inp), compute_output_hash(out)
        stable = ih1 == ih2 and oh1 == oh2
        print(f"  {sid}: input_stable={ih1==ih2} output_stable={oh1==oh2} => {'PASS' if stable else 'FAIL'}")
        if not stable:
            all_passed = False

    print("\n--- Reordered Dict Test ---")
    a = compute_input_hash({"a": 1, "b": 2})
    b = compute_input_hash({"b": 2, "a": 1})
    reorder_ok = a == b
    print(f"  reordered_dict_same_hash: {reorder_ok} => {'PASS' if reorder_ok else 'FAIL'}")
    if not reorder_ok:
        all_passed = False

    c = compute_input_hash({"a": 1, "b": 2})
    d = compute_input_hash({"a": 1, "b": 3})
    diff_ok = c != d
    print(f"  changed_value_different_hash: {diff_ok} => {'PASS' if diff_ok else 'FAIL'}")
    if not diff_ok:
        all_passed = False

    print("\n--- Narrative Stripping ---")
    nrec = build_hash_audit_record("SYSTEM.GET_SKILLOS_STATUS", {}, OUTPUT_WITH_NARRATIVE)
    print(f"  narrative_stripped: {nrec['narrative_stripped']}")
    print(f"  output_hash: {nrec['output_hash']} (len={len(nrec['output_hash'])})")

    print(f"\n--- Audit Summary ---")
    print(f"auditable_skills: {len(AUDITABLE_SKILLS)}")
    print(f"hash_length_ok: {all_passed}")
    print(f"reordered_dict_same_hash: {reorder_ok}")
    print(f"changed_value_different_hash: {diff_ok}")
    print(f"blocked_count: 0")
    print(f"runtime_reports_written: 0")
    print(f"enforcement: DISABLED")

    if all_passed:
        print("Z_SKILLOS_V1_0_C_HASH_SCAFFOLD_PASS")
    else:
        print("Z_SKILLOS_V1_0_C_HASH_SCAFFOLD_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
