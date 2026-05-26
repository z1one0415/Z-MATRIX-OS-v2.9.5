"""Hermes Memory Kernel validators — safety + schema validation

Hard rules:
- write_allowed must be False
- hermes_memory_write_allowed must be False
- real_z9_write_allowed must be False
- auto_calibration_allowed must be False
- prompt_auto_injection_allowed must be False
- real_trade_allowed must be False
- preview_only must be True
"""
from __future__ import annotations

from zmatrix.hermes_kernel.schemas import (
    APPROVAL_STATUS, MEMORY_STATUS,
)


def _check_safety_blockers(obj: dict, prefix: str = "") -> list[str]:
    violations = []
    if obj.get("write_allowed") is True:
        violations.append(f"{prefix}write_allowed must be False")
    if obj.get("hermes_memory_write_allowed") is True:
        violations.append(f"{prefix}hermes_memory_write_allowed must be False")
    if obj.get("real_z9_write_allowed") is True:
        violations.append(f"{prefix}real_z9_write_allowed must be False")
    if obj.get("auto_calibration_allowed") is True:
        violations.append(f"{prefix}auto_calibration_allowed must be False")
    if obj.get("prompt_auto_injection_allowed") is True:
        violations.append(f"{prefix}prompt_auto_injection_allowed must be False")
    if obj.get("real_trade_allowed") is True:
        violations.append(f"{prefix}real_trade_allowed must be False")
    if obj.get("preview_only") is False:
        violations.append(f"{prefix}preview_only must be True")
    return violations


def validate_hermes_safety(obj: dict) -> list[str]:
    return _check_safety_blockers(obj, "hermes_safety: ")


def validate_core_memory(memory: dict) -> list[str]:
    violations = []
    if not memory.get("memory_id"):
        violations.append("memory_id required")
    if not memory.get("title"):
        violations.append("title required")
    if memory.get("status") and memory["status"] not in MEMORY_STATUS:
        violations.append(f"invalid status: {memory['status']}")
    violations.extend(_check_safety_blockers(memory, "core_memory: "))
    return violations


def validate_learned_heuristic(heuristic: dict) -> list[str]:
    violations = []
    if not heuristic.get("heuristic_id"):
        violations.append("heuristic_id required")
    if not heuristic.get("title"):
        violations.append("title required")
    violations.extend(_check_safety_blockers(heuristic, "heuristic: "))
    return violations


def validate_memory_candidate(candidate: dict) -> list[str]:
    violations = []
    if not candidate.get("candidate_id"):
        violations.append("candidate_id required")
    if candidate.get("approval_status") and candidate["approval_status"] not in APPROVAL_STATUS:
        violations.append(f"invalid approval_status: {candidate['approval_status']}")
    if candidate.get("approval_status") == "APPROVED":
        violations.append("MemoryCandidate must not be APPROVED in preview mode")
    violations.extend(_check_safety_blockers(candidate, "memory_candidate: "))
    return violations


def validate_prompt_patch_preview(patch: dict) -> list[str]:
    violations = []
    if not patch.get("patch_id"):
        violations.append("patch_id required")
    if patch.get("prompt_auto_injection_allowed") is True:
        violations.append("prompt_auto_injection_allowed must be False")
    violations.extend(_check_safety_blockers(patch, "prompt_patch: "))
    return violations
