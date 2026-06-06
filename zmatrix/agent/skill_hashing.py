"""Deterministic hashing for SkillOS v1.0-C.

Provides canonical JSON serialization and SHA-256 hashing
for input_payload and output_payload.

Pure functions: no I/O, no invoke_skill, no runtime_reports.
"""

import json
import hashlib


def canonical_json(obj: object) -> str:
    """Serialize obj to canonical JSON string.

    Stable across Python runs:
    - sort_keys=True
    - separators=(",", ":")
    - ensure_ascii=False
    - No dynamic timestamps in payload.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_sha256(text: str) -> str:
    """Compute SHA-256 hex digest of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_input_hash(payload: dict) -> str:
    """Compute deterministic input_hash from input payload."""
    return compute_sha256(canonical_json(payload))


def compute_output_hash(payload: dict) -> str:
    """Compute deterministic output_hash from output payload.

    Only deterministic fields are included in the hash.
    Narrative/LLM-rendered fields are excluded if present.
    """
    # Strip narrative field if present (LLM output, not deterministic)
    clean = {k: v for k, v in payload.items() if k != "narrative"}
    return compute_sha256(canonical_json(clean))


def build_hash_audit_record(skill_id: str, input_payload: dict, output_payload: dict) -> dict:
    """Build a complete hash audit record for one skill invocation.

    Never blocks. Never writes files. Never calls invoke_skill.
    """
    ihash = compute_input_hash(input_payload)
    ohash = compute_output_hash(output_payload)
    return {
        "skill_id": skill_id,
        "mode": "PURE_HASH_SCAFFOLD",
        "blocked": False,
        "enforcement": "DISABLED",
        "input_hash": ihash,
        "output_hash": ohash,
        "hash_algorithm": "SHA-256",
        "canonical_method": "json.dumps(sort_keys=True, separators=(',',':'))",
        "narrative_stripped": "narrative" in output_payload,
    }
