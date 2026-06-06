#!/usr/bin/env python3
"""Standalone semantic drift auditor for SkillOS v1.1-B.

Compares current state against frozen baseline.
Outputs to stdout only. No file writes. No runtime blocking.
"""

import sys
from zmatrix.agent.skill_semantic_drift import audit_semantic_drift


def main():
    result = audit_semantic_drift()
    targets = result.get("targets", [])

    print(f"Drift detected: {result['drift_detected']}")
    print(f"Max severity: {result['max_severity']}")
    print(f"Runtime action: {result['runtime_action']}")
    print(f"Blocked: {result['blocked']}")
    print(f"Enforcement: {result['enforcement']}")
    print()

    for t in targets:
        name = t["target"]
        sev = t["severity"]
        icon = "✓" if sev == "INFO" else "⚠" if sev == "WARN" else "✗"
        print(f"  {icon} {name}: {sev}")

    print()

    if result["drift_detected"]:
        print("Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_AUDIT_FAIL_CI")
        sys.exit(1)
    else:
        print("Z_SKILLOS_V1_1_B_SEMANTIC_DRIFT_AUDIT_PASS")


if __name__ == "__main__":
    main()
