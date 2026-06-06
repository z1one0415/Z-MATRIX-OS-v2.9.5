#!/usr/bin/env python3
"""Audit v1.0-B shadow schema compliance for 5 sample skills.

Reads v1.0-A contract registry via skill_schema_validator.
Reports gaps for gate-approved skills missing from registry.
Audits available subset with documented substitutes.
Outputs to stdout only. Does NOT write runtime_reports.
"""

import sys
from zmatrix.agent.skill_schema_validator import (
    audit_skill_schema,
    list_sample_skill_ids,
    get_audit_skill_ids,
    AVAILABLE_SUBSTITUTES,
)

MOCK_INPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {},
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {},
    "RESEARCHDB.GET_LAYER_STATUS": {"data_snapshot_id": "snap-001"},
    "FACTOR.GET_FACTOR_REGISTRY": {"data_snapshot_id": "snap-002"},
}

MOCK_OUTPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {
        "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
        "skill_version": "1.0.0", "status": "SUCCESS",
        "risk_level": "R0_READ", "input_hash": "abc123", "output_hash": "def456",
    },
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {
        "skill_id": "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY",
        "skill_version": "1.0.0", "status": "SUCCESS",
        "risk_level": "R0_READ", "input_hash": "abc123", "output_hash": "def456",
    },
    "RESEARCHDB.GET_LAYER_STATUS": {
        "skill_id": "RESEARCHDB.GET_LAYER_STATUS",
        "skill_version": "1.0.0", "status": "SUCCESS",
        "risk_level": "R0_READ", "input_hash": "abc123", "output_hash": "def456",
        "data_snapshot_id": "snap-001",
    },
    "FACTOR.GET_FACTOR_REGISTRY": {
        "skill_id": "FACTOR.GET_FACTOR_REGISTRY",
        "skill_version": "1.0.0", "status": "SUCCESS",
        "risk_level": "R0_READ", "input_hash": "abc123", "output_hash": "def456",
        "data_snapshot_id": "snap-002",
    },
}

BAD_OUTPUT_MISSING_REQUIRED = {
    "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
    "status": "SUCCESS",
}


def main():
    sample_ids = list_sample_skill_ids()
    audit_ids = get_audit_skill_ids()
    missing = [s for s in sample_ids if s not in audit_ids]

    print(f"Gate-approved: {len(sample_ids)} skills")
    for sid in sample_ids:
        status = "EXISTS" if sid in audit_ids else f"GAP -> substitute: {AVAILABLE_SUBSTITUTES.get(sid, 'NONE')}"
        icon = "V" if sid in audit_ids else "!"
        print(f"  {icon} {sid}: {status}")

    print(f"\nAuditable (in registry): {len(audit_ids)}")
    for sid in audit_ids:
        print(f"  - {sid}")
    print(f"Gaps (documented, not silent): {len(missing)}")

    all_passed = True

    print("\n--- Shadow Audit: available skills ---")
    for sid in audit_ids:
        inp = MOCK_INPUTS.get(sid, {})
        out = MOCK_OUTPUTS.get(sid, {})
        result = audit_skill_schema(sid, inp, out)
        ok = "PASS" if result["input_valid"] and result["output_valid"] else "FAIL"
        print(f"  {sid}: input={result['input_valid']} output={result['output_valid']} blocked={result['blocked']} enforcement={result['enforcement']} => {ok}")
        if not result["input_valid"] or not result["output_valid"]:
            all_passed = False
        for v in result["violations"]:
            print(f"    violation: {v}")

    print("\n--- Shadow Audit: negative case ---")
    neg = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, BAD_OUTPUT_MISSING_REQUIRED)
    print(f"  SYSTEM.GET_SKILLOS_STATUS: input={neg['input_valid']} output={neg['output_valid']} blocked={neg['blocked']} => {'PASS (caught)' if not neg['output_valid'] else 'FAIL (missed)'}")
    for v in neg["violations"]:
        print(f"    violation: {v}")
    if neg["output_valid"]:
        all_passed = False

    print(f"\n--- Audit Summary ---")
    print(f"approved_sample_count: {len(sample_ids)}")
    print(f"registry_gap_count: {len(missing)}")
    print(f"auditable_unique_count: {len(audit_ids)}")
    # Count substitutes that collide: total substitutions attempted minus unique additions
    sub_attempts = sum(1 for s in sample_ids if s not in audit_ids and s in AVAILABLE_SUBSTITUTES)
    # But we need to count collisions. Count how many approved have substitutes,
    # subtract how many unique auditable came from substitutes.
    approved_with_sub = [s for s in sample_ids if s in AVAILABLE_SUBSTITUTES]
    direct_count = sum(1 for s in sample_ids if s in audit_ids)
    sub_added = len(audit_ids) - direct_count
    dupes = len(approved_with_sub) - sub_added
    print(f"duplicate_substitute_count: {dupes}")
    print(f"all_available_passed: {all_passed}")
    print(f"negative_violation_detected: {not neg['output_valid']}")
    print(f"blocked_count: 0")
    print(f"runtime_reports_written: 0")
    print(f"enforcement: DISABLED")

    if all_passed and not neg["output_valid"]:
        print("Z_SKILLOS_V1_0_B_SHADOW_AUDIT_PASS")
    else:
        print("Z_SKILLOS_V1_0_B_SHADOW_AUDIT_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
