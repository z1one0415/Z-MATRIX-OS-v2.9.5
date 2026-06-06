#!/usr/bin/env python3
"""Build v1.0-F golden regression cases from real contract registry.

Reads: skill_contract_registry.json (READ-ONLY)
Selects: 12 real skill_ids across >= 8 domains
Outputs: skillos_v1_0_f_golden_regression_cases.json
Uses: v1.0-C skill_hashing for expected hashes
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONTRACT_PATH = ROOT / "data/research_db/agent/registry/skill_contract_registry.json"
GOLDEN_OUT = ROOT / "data/research_db/agent/golden/skillos_v1_0_f_golden_regression_cases.json"

# Priority selection: 1 per domain (R0_READ preferred), then fill to 12
SELECTION = [
    ("AUTOCASE", "AUTOCASE.GET_INTAKE_SCHEMA"),
    ("BMATRIX", "BMATRIX.GET_SCHEMA"),
    ("CASEFORGE", "CASEFORGE.GET_CASE_DRAFT_SCHEMA"),
    ("COCKPIT", "COCKPIT.BUILD_SKILLOS_OVERVIEW"),
    ("COUNCIL", "COUNCIL.GET_COUNCIL_SCHEMA"),
    ("DATAFORGE", "DATAFORGE.GET_SNAPSHOT_SCHEMA"),
    ("DMATRIX", "DMATRIX.GET_SCHEMA"),
    ("FACTOR", "FACTOR.GET_FACTOR_REGISTRY"),
    ("GOVERNANCE", "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY"),
    ("MEMORY", "MEMORY.GET_MEMORY_CANDIDATE_SCHEMA"),
    ("PORTFOLIO", "PORTFOLIO.GET_SCHEMA"),
    ("RESEARCHDB", "RESEARCHDB.GET_LAYER_STATUS"),
]

MINIMAL_OUTPUT = {
    "skill_id": "PLACEHOLDER",
    "skill_version": "1.0.0",
    "status": "SUCCESS",
    "risk_level": "R0_READ",
}


def build() -> dict:
    from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash
    from zmatrix.agent.skill_contract_registry import get_skill_contract

    contracts = json.loads(CONTRACT_PATH.read_text())
    valid_ids = {c["skill_id"] for c in contracts["contracts"]}

    cases = []
    for domain, sid in SELECTION:
        if sid not in valid_ids:
            print(f"SKIP: {sid} not in contract registry", file=sys.stderr)
            continue

        c = get_skill_contract(sid)
        risk = c["risk_level"] if c else "R0_READ"

        inp = {} if domain != "RESEARCHDB" else {"data_snapshot_id": "snap-reg-001"}
        out = dict(MINIMAL_OUTPUT)
        out["skill_id"] = sid
        out["risk_level"] = risk

        case = {
            "case_id": f"REGRESSION.{sid}.001",
            "skill_id": sid,
            "domain": domain,
            "risk_level": risk,
            "input_payload": inp,
            "output_payload": out,
            "expected_input_hash": compute_input_hash(inp),
            "expected_output_hash": compute_output_hash(out),
            "expected_hash_algorithm": "SHA-256",
            "excluded_output_fields": ["narrative", "input_hash", "output_hash"],
        }
        cases.append(case)

    domains_covered = len({c["domain"] for c in cases})
    return {
        "regression_version": "1.0.0",
        "hash_algorithm": "SHA-256",
        "generation_policy": "REPRODUCIBLE_STATIC_BUILD",
        "source_registry": "skill_contract_registry.json",
        "case_count": len(cases),
        "domains_covered": domains_covered,
        "cases": cases,
    }


if __name__ == "__main__":
    registry = build()
    GOLDEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    GOLDEN_OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
    print(f"Built regression cases: {registry['case_count']} skills, {registry['domains_covered']} domains -> {GOLDEN_OUT}")
