"""Shadow/audit-only schema validator for SkillOS v1.0-B.

Reads v1.0-A contract registry.
Validates input/output schema compliance.
Audit-only mode: never blocks, never raises, never writes.
"""

import json
from pathlib import Path
from typing import Any, Optional

_CONTRACT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "research_db" / "agent" / "registry" / "skill_contract_registry.json"

SAMPLE_SKILL_IDS = [
    "SYSTEM.GET_SKILLOS_STATUS",
    "GOVERNANCE.GET_VERIFY_STATUS",
    "RESEARCHDB.GET_SCHEMA",
    "COCKPIT.GET_SKILLOS_STATUS",
    "FACTOR.LIST_REGISTERED_FACTORS",
]

# Best-available substitutes for gate-approved skills missing from contract registry.
AVAILABLE_SUBSTITUTES = {
    "GOVERNANCE.GET_VERIFY_STATUS": "GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY",
    "RESEARCHDB.GET_SCHEMA": "RESEARCHDB.GET_LAYER_STATUS",
    "COCKPIT.GET_SKILLOS_STATUS": "SYSTEM.GET_SKILLOS_STATUS",
    "FACTOR.LIST_REGISTERED_FACTORS": "FACTOR.GET_FACTOR_REGISTRY",
}

def get_audit_skill_ids() -> list:
    """Return skills available for audit: approved exist + substitutes."""
    from zmatrix.agent.skill_contract_registry import get_skill_contract
    result = []
    for sid in SAMPLE_SKILL_IDS:
        if get_skill_contract(sid):
            result.append(sid)
        elif sid in AVAILABLE_SUBSTITUTES:
            result.append(AVAILABLE_SUBSTITUTES[sid])
    return result

_cache: Optional[dict] = None


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(_CONTRACT_PATH.read_text())
    return _cache


def _get_contract(skill_id: str) -> Optional[dict]:
    reg = _load()
    for c in reg.get("contracts", []):
        if c.get("skill_id") == skill_id:
            return c
    return None


def _check_type(value: Any, expected: str) -> bool:
    """Check JSON Schema type compatibility."""
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float))
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "null":
        return value is None
    # union: ["string","null"]
    return True


def _validate_schema_fields(payload: dict, schema: dict) -> list:
    """Validate payload against a JSON schema (subset), return violations list."""
    violations = []
    stype = schema.get("type", "object")
    if stype == "object":
        if not isinstance(payload, dict):
            violations.append(f"expected object, got {type(payload).__name__}")
            return violations
        required = schema.get("required", [])
        for key in required:
            if key not in payload:
                violations.append(f"missing required field: {key}")
        props = schema.get("properties", {})
        for key, prop_schema in props.items():
            if key in payload:
                prop_type = prop_schema.get("type")
                if prop_type:
                    # handle union types
                    if isinstance(prop_type, list):
                        valid = False
                        for t in prop_type:
                            if _check_type(payload[key], t):
                                valid = True
                                break
                        if not valid:
                            violations.append(
                                f"field '{key}': expected {prop_type}, got {type(payload[key]).__name__}"
                            )
                    elif not _check_type(payload[key], prop_type):
                        violations.append(
                            f"field '{key}': expected {prop_type}, got {type(payload[key]).__name__}"
                        )
                p_enum = prop_schema.get("enum")
                if p_enum and payload[key] not in p_enum:
                    violations.append(
                        f"field '{key}': value '{payload[key]}' not in enum {p_enum}"
                    )
    return violations


def validate_input_schema(skill_id: str, payload: dict) -> dict:
    """Validate input payload against contract input_schema."""
    contract = _get_contract(skill_id)
    if contract is None:
        return {
            "skill_id": skill_id,
            "valid": False,
            "violations": [f"skill_id '{skill_id}' not found in contract registry"],
            "mode": "SHADOW_AUDIT_ONLY",
        }
    schema = contract.get("input_schema", {})
    violations = _validate_schema_fields(payload, schema)
    return {
        "skill_id": skill_id,
        "valid": len(violations) == 0,
        "violations": violations,
        "mode": "SHADOW_AUDIT_ONLY",
    }


def validate_output_schema(skill_id: str, payload: dict) -> dict:
    """Validate output payload against contract output_schema."""
    contract = _get_contract(skill_id)
    if contract is None:
        return {
            "skill_id": skill_id,
            "valid": False,
            "violations": [f"skill_id '{skill_id}' not found in contract registry"],
            "mode": "SHADOW_AUDIT_ONLY",
        }
    schema = contract.get("output_schema", {})
    violations = _validate_schema_fields(payload, schema)
    return {
        "skill_id": skill_id,
        "valid": len(violations) == 0,
        "violations": violations,
        "mode": "SHADOW_AUDIT_ONLY",
    }


def audit_skill_schema(skill_id: str, input_payload: dict, output_payload: dict) -> dict:
    """Full audit of both input and output schema compliance.

    Never blocks. Never raises exceptions. Never writes files.
    """
    input_result = validate_input_schema(skill_id, input_payload)
    output_result = validate_output_schema(skill_id, output_payload)
    return {
        "skill_id": skill_id,
        "mode": "SHADOW_AUDIT_ONLY",
        "input_valid": input_result["valid"],
        "output_valid": output_result["valid"],
        "violations": input_result["violations"] + output_result["violations"],
        "blocked": False,
        "enforcement": "DISABLED",
    }


def list_sample_skill_ids() -> list:
    """Return the fixed list of 5 sample skills for v1.0-B audit."""
    return list(SAMPLE_SKILL_IDS)
