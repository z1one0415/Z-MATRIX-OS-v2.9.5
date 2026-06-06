"""Hash-aware shadow auditor for SkillOS v1.0-E.

Chains:
- v1.0-B schema validator (input/output schema compliance)
- v1.0-C skill_hashing (input_hash/output_hash)
- v1.0-D golden cases (expected hash comparison)

Audit-only: never blocks, never writes, never calls invoke_skill.
"""

import json
from pathlib import Path
from zmatrix.agent.skill_schema_validator import (
    validate_input_schema,
    validate_output_schema,
)
from zmatrix.agent.skill_hashing import compute_input_hash, compute_output_hash

_GOLDEN_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "golden" / "skillos_v1_0_d_golden_cases.json"
_cache: dict | None = None


def _load_golden() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(_GOLDEN_PATH.read_text())
    return _cache


def _get_golden_case(skill_id: str) -> dict | None:
    golden = _load_golden()
    for c in golden.get("cases", []):
        if c["skill_id"] == skill_id:
            return c
    return None


def audit_hash_aware_skill(skill_id: str, input_payload: dict, output_payload: dict) -> dict:
    """Full hash-aware shadow audit for one skill invocation.

    Returns audit result. Never blocks. Never writes files.
    """
    # Schema audit (v1.0-B) — validate complete output with hashes
    ihash = compute_input_hash(input_payload)
    ohash = compute_output_hash(output_payload)
    complete_out = dict(output_payload)
    complete_out["input_hash"] = ihash
    complete_out["output_hash"] = ohash
    schema_in = validate_input_schema(skill_id, input_payload)
    schema_out = validate_output_schema(skill_id, complete_out)

    # Golden comparison (v1.0-D)
    golden = _get_golden_case(skill_id)
    golden_in_match = None
    golden_out_match = None
    golden_found = golden is not None
    if golden:
        golden_in_match = ihash == golden.get("expected_input_hash", "")
        golden_out_match = ohash == golden.get("expected_output_hash", "")

    violations = schema_in.get("violations", []) + schema_out.get("violations", [])
    if not schema_in.get("valid"):
        violations.append(f"schema_input_invalid: {skill_id}")
    if not schema_out.get("valid"):
        violations.append(f"schema_output_invalid: {skill_id}")
    if golden_found and golden_in_match is False:
        violations.append(f"golden_input_hash_mismatch: {skill_id}")

    return {
        "skill_id": skill_id,
        "mode": "HASH_AWARE_SHADOW_AUDIT",
        "schema_input_valid": schema_in.get("valid", False),
        "schema_output_valid": schema_out.get("valid", False),
        "input_hash": ihash,
        "output_hash": ohash,
        "golden_case_found": golden_found,
        "golden_input_match": golden_in_match,
        "golden_output_match": golden_out_match,
        "violations": violations,
        "blocked": False,
        "enforcement": "DISABLED",
    }


def audit_hash_aware_batch(cases: list) -> dict:
    """Audit a batch of cases. Each case: {skill_id, input_payload, output_payload}."""
    results = []
    all_pass = True
    for c in cases:
        r = audit_hash_aware_skill(c["skill_id"], c.get("input_payload", {}), c.get("output_payload", {}))
        results.append(r)
        if not r["schema_input_valid"] or not r["schema_output_valid"]:
            all_pass = False
        if r["golden_input_match"] is False or r["golden_output_match"] is False:
            all_pass = False
    return {
        "case_count": len(cases),
        "blocked_count": 0,
        "enforcement": "DISABLED",
        "all_pass": all_pass,
        "results": results,
    }
