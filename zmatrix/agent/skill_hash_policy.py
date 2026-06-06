"""Static hash policy manifest for SkillOS v1.0-D.

Declares canonical JSON policy, hash algorithm, and volatile field exclusions.
Does NOT modify hash computation logic (stays in skill_hashing.py).
Pure manifest: no I/O, no runtime calls, no enforcement.
"""

HASH_ALGORITHM = "SHA-256"

CANONICAL_JSON_POLICY = {
    "sort_keys": True,
    "separators": [",", ":"],
    "ensure_ascii": False,
}

OUTPUT_HASH_EXCLUDED_FIELDS = ["narrative"]


def get_hash_policy() -> dict:
    """Return the full hash policy manifest."""
    return {
        "hash_algorithm": HASH_ALGORITHM,
        "canonical_json_policy": CANONICAL_JSON_POLICY,
        "output_hash_excluded_fields": list(OUTPUT_HASH_EXCLUDED_FIELDS),
    }


def get_output_hash_excluded_fields() -> list:
    """Return the list of fields excluded from output hash computation."""
    return list(OUTPUT_HASH_EXCLUDED_FIELDS)


def is_output_hash_excluded_field(field: str) -> bool:
    """Check if a field is excluded from output hash."""
    return field in OUTPUT_HASH_EXCLUDED_FIELDS
