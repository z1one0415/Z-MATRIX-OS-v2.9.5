"""Hermes Memory Kernel Preview — read-only / preview-only coordinator

Kernel is NOT a writer.
Kernel is NOT an auto-evolution agent.
Kernel is NOT a prompt injector.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

HERMES_MEMORY_KERNEL_PREVIEW_VERSION = "HERMES_MEMORY_KERNEL_PREVIEW_V10"


def build_hermes_memory_kernel_preview(
    *,
    task_context: dict,
    event_store_events: list[dict] | None = None,
    core_memory: dict | None = None,
    working_context: dict | None = None,
    learned_heuristics: list[dict] | None = None,
) -> dict:
    """Build Hermes Memory Kernel Preview — unified read-only coordinator.

    1. Read core_memory
    2. Read working_context
    3. Filter learned_heuristics
    4. Generate prompt_patch_preview
    5. Output kernel preview
    6. Does NOT write long-term memory
    7. Does NOT append EventStore
    8. Does NOT auto-inject prompts
    """
    from zmatrix.hermes_kernel.retrieval import retrieve_relevant_heuristics
    from zmatrix.hermes_kernel.prompt_patch_preview import build_prompt_patch_preview

    seed = f"{task_context.get('task_type','')}|{task_context.get('ticker','')}"
    kernel_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    heuristics = learned_heuristics or []
    retrieval = retrieve_relevant_heuristics(
        task=task_context,
        heuristics=heuristics,
    )
    matched = retrieval.get("matched_heuristics", [])

    patch_preview = build_prompt_patch_preview(
        task_context=task_context,
        heuristics=matched,
    )

    return {
        "kernel_id": kernel_id,
        "kernel_version": HERMES_MEMORY_KERNEL_PREVIEW_VERSION,
        "mode": "READ_ONLY_PREVIEW",
        "created_at": created_at,
        "task_context": dict(task_context),
        "core_memory_preview": dict(core_memory) if core_memory else {},
        "working_context_preview": dict(working_context) if working_context else {},
        "relevant_heuristics": matched,
        "prompt_patch_preview": patch_preview,
        "memory_candidate_preview_allowed": True,
        "calibration_event_preview_allowed": True,
        "write_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
        "real_trade_allowed": False,
    }
