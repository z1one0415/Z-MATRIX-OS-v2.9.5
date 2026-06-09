"""
Static Input Snapshot — In-memory placeholder only.

No file reads. No external data. No factor recalculation.
Produces only an in-memory placeholder structure.
"""

from __future__ import annotations


def build_static_input_snapshot(
    factor_ids: tuple[str, ...],
) -> dict:
    """
    Build a static input snapshot from factor IDs.

    This is a placeholder skeleton. It does NOT read any artifact
    files from disk, does NOT fetch external data, does NOT write
    any files, and does NOT trigger factor recalculation.

    Args:
        factor_ids: Tuple of factor identifiers (e.g., ('F21', 'F22')).

    Returns:
        A dict with placeholder fields only.
    """
    return {
        "snapshot_mode": "IN_MEMORY_PLACEHOLDER_ONLY",
        "runtime_data_required": False,
        "external_data_required": False,
        "factor_recalculation_required": False,
        "factor_result_update_required": False,
        "factor_ids": list(factor_ids),
        "artifacts_loaded": 0,
        "source": "placeholder",
    }
