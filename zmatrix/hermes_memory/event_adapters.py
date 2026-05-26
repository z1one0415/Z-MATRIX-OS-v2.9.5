"""EventStore adapters for Hermes preview output — build EventStore events (no auto-append)"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event
from zmatrix.event_store.schemas import DEFAULT_EVENT_SAFETY


def build_memory_candidate_event(memory_candidate_preview: dict) -> dict:
    """Build a MemoryCandidateEvent from a memory candidate preview.

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    """
    payload = {
        "memory_candidate_id": memory_candidate_preview.get("memory_candidate_id", ""),
        "candidate_version": memory_candidate_preview.get("candidate_version", ""),
        "source_event_id": memory_candidate_preview.get("source_event_id", ""),
        "mistake_type": memory_candidate_preview.get("mistake_type", ""),
        "severity": memory_candidate_preview.get("severity", ""),
        "confidence": memory_candidate_preview.get("confidence", ""),
        "proposed_lesson": memory_candidate_preview.get("proposed_lesson", ""),
        "status": memory_candidate_preview.get("status", "DRAFT"),
    }
    return build_event(
        event_type="MemoryCandidateEvent",
        producer_module="zmatrix.hermes_memory.event_adapters.build_memory_candidate_event",
        payload=payload,
    )


def build_calibration_event(calibration_event_preview: dict) -> dict:
    """Build a CalibrationEvent from a calibration event preview.

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    """
    payload = {
        "calibration_event_id": calibration_event_preview.get("calibration_event_id", ""),
        "calibration_version": calibration_event_preview.get("calibration_version", ""),
        "memory_candidate_id": calibration_event_preview.get("memory_candidate_id", ""),
        "target_domain": calibration_event_preview.get("target_domain", ""),
        "proposed_change": calibration_event_preview.get("proposed_change", {}),
        "status": calibration_event_preview.get("status", "PENDING_HUMAN_APPROVAL"),
    }
    return build_event(
        event_type="CalibrationEvent",
        producer_module="zmatrix.hermes_memory.event_adapters.build_calibration_event",
        payload=payload,
    )


def build_prompt_patch_event(prompt_patch_preview: dict) -> dict:
    """Build a PromptPatchEvent from a prompt patch preview.

    Does NOT append. Does NOT auto-inject. Does NOT write Hermes memory.
    """
    payload = {
        "patch_id": prompt_patch_preview.get("patch_id", ""),
        "patch_version": prompt_patch_preview.get("patch_version", ""),
        "task_context": prompt_patch_preview.get("task_context", {}),
        "heuristic_count": prompt_patch_preview.get("heuristic_count", 0),
        "requires_human_approval": prompt_patch_preview.get("requires_human_approval", True),
    }
    return build_event(
        event_type="PromptPatchEvent",
        producer_module="zmatrix.hermes_memory.event_adapters.build_prompt_patch_event",
        payload=payload,
    )
