#!/usr/bin/env python3
"""V8-G: V9 entry gate — reads ALL V8 audits including manifest."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

def load(name):
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    rd = load("v8_expanded_data_readiness.json")
    leak = load("v8_factor_leakage_audit.json")
    cov = load("v8_factor_coverage_audit.json")
    lcov = load("v8_label_coverage_audit.json")
    adeq = load("v8_sample_adequacy_audit.json")
    ma = load("v8_large_data_manifest_audit.json")
    co = load("case_expansion_v8_closeout.json")

    # Individual checks
    data_ok = rd.get("ready_for_factor_rebuild", False)
    leak_ok = leak.get("leakage_safe", False)
    cov_ok = cov.get("coverage", 0) >= 0.95
    c60 = lcov.get("coverage_by_horizon", {}).get("T60", {}).get("valid_dates", 0)
    t60_ok = c60 >= 400
    adeq_t60 = adeq.get("horizon_status", {}).get("T60", "")
    adeq_ok = adeq_t60 == "EXPLORATORY_USABLE"
    man_ok = ma.get("manifest_consistent", False)
    man_ready = ma.get("ready_for_v9_gate", False)
    man_committed = ma.get("large_files_committed_to_git", True)
    co_man_ok = co.get("manifest_consistent", False)
    co_audit_ok = co.get("large_data_manifest_audit_pass", False)
    alpha_blocked = (
        not rd.get("ready_for_alpha_claim", True)
        and not co.get("ready_for_alpha_claim", True)
    )
    safety_blocked = (
        co.get("production", "") == "BLOCKED"
        and co.get("broker_runtime", "") == "BLOCKED"
        and co.get("real_trade", "") == "BLOCKED"
    )

    # Build blocking reasons
    blocking = []
    if not data_ok:
        blocking.append("DATA_NOT_READY")
    if not leak_ok:
        blocking.append("LEAKAGE_AUDIT_NOT_PASS")
    if not cov_ok:
        blocking.append("FACTOR_COVERAGE_BELOW_THRESHOLD")
    if not t60_ok:
        blocking.append("T60_LABEL_INSUFFICIENT")
    if not adeq_ok:
        blocking.append("SAMPLE_ADEQUACY_NOT_PASS")
    if not man_ok:
        blocking.append("MANIFEST_NOT_CONSISTENT")
    if not man_ready:
        blocking.append("MANIFEST_AUDIT_NOT_PASS")
    if man_committed:
        blocking.append("LARGE_FILES_COMMITTED")
    if not co_man_ok:
        blocking.append("CLOSEOUT_MANIFEST_NOT_CONFIRMED")
    if not co_audit_ok:
        blocking.append("CLOSEOUT_MANIFEST_AUDIT_NOT_PASS")
    if not alpha_blocked:
        blocking.append("ALPHA_CLAIM_DETECTED")
    if not safety_blocked:
        blocking.append("SAFETY_NOT_BLOCKED")

    all_ok = len(blocking) == 0

    gate = {
        "status": (
            "V9_FORMAL_FACTOR_VALIDATION_ENTRY_ALLOWED"
            if all_ok
            else "V9_ENTRY_BLOCKED_V8_GATE_FAILURE"
        ),
        "ready_for_v9_formal_validation": all_ok,
        "manifest_consistent": man_ok,
        "ready_for_alpha_claim": False,
        "blocking_reasons": blocking,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (C / "v9_formal_factor_validation_entry_gate.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False)
    )
    print(
        f"V9 Gate: {'ALLOWED' if all_ok else 'BLOCKED'} | {len(blocking)} blocking | manifest_consistent={man_ok}"
    )


if __name__ == "__main__":
    main()
