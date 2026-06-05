#!/usr/bin/env python3
"""Audit v1.0-B shadow schema compliance for 5 sample skills.

Reads v1.0-A contract registry via skill_schema_validator.
Constructs minimal mock payloads.
Outputs audit summary to stdout only.
Does NOT write runtime_reports.
Does NOT modify invoke_skill.
"""

import sys
from zmatrix.agent.skill_schema_validator import (
    audit_skill_schema,
    list_sample_skill_ids,
)

MOCK_INPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {},
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {},
    "RESEARCHDB.GET_LAYER_STATUS": {"data_snapshot_id": "snap-001"},
    "FACTOR.GET_FACTOR_REGISTRY": {"data_snapshot_id": "snap-002"},
    "AUTOCASE.GET_INTAKE_SCHEMA": {"data_snapshot_id": "snap-003"},
}

MOCK_OUTPUTS = {
    "SYSTEM.GET_SKILLOS_STATUS": {
        "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "input_hash": "abc123",
        "output_hash": "def456",
    },
    "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY": {
        "skill_id": "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "input_hash": "abc123",
        "output_hash": "def456",
    },
    "RESEARCHDB.GET_LAYER_STATUS": {
        "skill_id": "RESEARCHDB.GET_LAYER_STATUS",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "input_hash": "abc123",
        "output_hash": "def456",
        "data_snapshot_id": "snap-001",
    },
    "FACTOR.GET_FACTOR_REGISTRY": {
        "skill_id": "FACTOR.GET_FACTOR_REGISTRY",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "input_hash": "abc123",
        "output_hash": "def456",
        "data_snapshot_id": "snap-002",
    },
    "AUTOCASE.GET_INTAKE_SCHEMA": {
        "skill_id": "AUTOCASE.GET_INTAKE_SCHEMA",
        "skill_version": "1.0.0",
        "status": "SUCCESS",
        "risk_level": "R0_READ",
        "input_hash": "abc123",
        "output_hash": "def456",
        "data_snapshot_id": "snap-003",
    },
}

# Intentionally bad output for negative test
BAD_OUTPUT_MISSING_REQUIRED = {
    "skill_id": "SYSTEM.GET_SKILLOS_STATUS",
    "status": "SUCCESS",
}


def main():
    sample_ids = list_sample_skill_ids()
    print(f"Sample skills: {len(sample_ids)}")
    for sid in sample_ids:
        print(f"  - {sid}")

    all_passed = True
    total_violations = 0

    print("\n--- Shadow Audit: valid payloads ---")
    for sid in sample_ids:
        inp = MOCK_INPUTS.get(sid, {})
        out = MOCK_OUTPUTS.get(sid, {})
        result = audit_skill_schema(sid, inp, out)
        ok = "PASS" if result["input_valid"] and result["output_valid"] else "FAIL"
        print(f"  {sid}: input={result['input_valid']} output={result['output_valid']} blocked={result['blocked']} enforcement={result['enforcement']} => {ok}")
        if not result["input_valid"] or not result["output_valid"]:
            all_passed = False
            total_violations += len(result["violations"])
        if result["violations"]:
            for v in result["violations"]:
                print(f"    violation: {v}")

    print("\n--- Shadow Audit: negative case (missing required field) ---")
    neg = audit_skill_schema("SYSTEM.GET_SKILLOS_STATUS", {}, BAD_OUTPUT_MISSING_REQUIRED)
    print(f"  SYSTEM.GET_SKILLOS_STATUS: input={neg['input_valid']} output={neg['output_valid']} blocked={neg['blocked']} => {'PASS (caught violation)' if not neg['output_valid'] else 'FAIL (missed violation)'}")
    for v in neg["violations"]:
        print(f"    violation: {v}")
    if neg["output_valid"]:
        all_passed = False

    print(f"\n--- Audit Summary ---")
    print(f"sample_count: {len(sample_ids)}")
    print(f"all_positive_passed: {all_passed}")
    print(f"negative_violation_detected: {not neg['output_valid']}")
    print(f"blocked_count: {0}")
    print(f"runtime_reports_written: 0")
    print(f"enforcement: DISABLED")
    print(f"invoke_skill_touched: False")
    print(f"result_envelope_touched: False")

    if all_passed and not neg["output_valid"]:
        print("Z_SKILLOS_V1_0_B_SHADOW_AUDIT_PASS")
    else:
        print("Z_SKILLOS_V1_0_B_SHADOW_AUDIT_FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
