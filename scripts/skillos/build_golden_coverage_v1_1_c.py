#!/usr/bin/env python3
"""Build v1.1-C golden regression: 24 cases, >=16 domains.

Reads v1.0-F 12 cases, adds 12 new registry-exact skills.
Outputs: skillos_v1_1_c_golden_regression_cases_24.json
"""

import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
F12 = ROOT / "data/research_db/agent/golden/skillos_v1_0_f_golden_regression_cases.json"
OUT = ROOT / "data/research_db/agent/golden/skillos_v1_1_c_golden_regression_cases_24.json"

NEW_SKILL_IDS = [
    "SYSTEM.GET_SKILLOS_STATUS",
    "SYSTEM.GET_SKILL_REGISTRY_SUMMARY",
    "SYSTEM.GET_RESEARCH_SUMMARY",
    "WORKFLOW.GET_WORKFLOW_SCHEMA",
    "ZC35.GET_SCHEMA",
    "ZG16.GET_SOURCE_REGISTRY",
    "REPORT.RENDER_DRAFT",
    "COUNCIL.GET_EXPERT_ROLE_REGISTRY",
    "GOVERNANCE.GET_LEDGER_STATUS",
    "PORTFOLIO.GET_RISK_BUDGET_TEMPLATE",
    "FACTOR.GET_FACTOR_SCHEMA",
    "RESEARCHDB.GET_DATASET_REGISTRY",
]

MINIMAL_OUTPUT = {
    "skill_id": "PLACEHOLDER", "skill_version": "1.0.0",
    "status": "SUCCESS", "risk_level": "R0_READ",
}


def build():
    from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
    from zmatrix.agent.skill_contract_registry import get_skill_contract

    old = json.loads(F12.read_text())
    old_cases = list(old["cases"])
    existing_ids = {c["skill_id"] for c in old_cases}

    new_cases = []
    for sid in NEW_SKILL_IDS:
        if sid in existing_ids:
            continue
        c = get_skill_contract(sid)
        if c is None:
            print(f"SKIP: {sid} not in registry", file=sys.stderr)
            continue
        domain = c["domain"]  # contract-derived, not manual
        risk = c["risk_level"]
        out = dict(MINIMAL_OUTPUT)
        out["skill_id"] = sid
        out["risk_level"] = risk
        case = {
            "case_id": f"REGRESSION.{sid}.001",
            "skill_id": sid, "domain": domain, "risk_level": risk,
            "input_payload": {},
            "output_payload": out,
            "expected_input_hash": compute_input_hash({}),
            "expected_output_hash": compute_output_hash(out),
            "expected_hash_algorithm": "SHA-256",
            "excluded_output_fields": ["narrative", "input_hash", "output_hash"],
        }
        new_cases.append(case)

    all_cases = old_cases + new_cases
    domains = len({c["domain"] for c in all_cases})
    return {
        "regression_version": "1.1-C",
        "hash_algorithm": "SHA-256",
        "generation_policy": "REPRODUCIBLE_STATIC_BUILD",
        "source_registry": "skill_contract_registry.json",
        "v1_0_f_cases": len(old_cases),
        "v1_1_c_added": len(new_cases),
        "case_count": len(all_cases),
        "domains_covered": domains,
        "registry_exact": True,
        "cases": all_cases,
    }


if __name__ == "__main__":
    reg = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n")
    print(f"Built: {reg['case_count']} cases, {reg['domains_covered']} domains → {OUT}")
