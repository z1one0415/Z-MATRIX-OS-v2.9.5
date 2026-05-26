"""Approval Queue Preview — local queue preview, no DB write, no auto process"""
from __future__ import annotations

_SEVERITY_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
_REQUEST_TYPE_RANK = {
    "CALIBRATION_EVENT_APPROVAL": 0,
    "PROMPT_PATCH_APPROVAL": 1,
    "MEMORY_CANDIDATE_APPROVAL": 2,
}


def build_approval_queue_preview(requests: list[dict]) -> dict:
    """Build a preview of the approval queue.

    Sorting:
    1. HIGH severity first
    2. CalibrationEvent > PromptPatch > MemoryCandidate
    3. REQUEST_MORE_EVIDENCE stays pending

    Preview only. No auto processing. No Hermes write. No Z9 write.
    """
    def _sort_key(r):
        preview = r.get("source_preview", {})
        severity = str(preview.get("severity", "LOW")).upper()
        sev_rank = _SEVERITY_RANK.get(severity, 99)
        req_rank = _REQUEST_TYPE_RANK.get(r.get("request_type", ""), 99)
        return (sev_rank, req_rank)

    sorted_requests = sorted(requests, key=_sort_key)
    pending = [r for r in sorted_requests if r.get("status") == "PENDING_REVIEW"]

    return {
        "queue_version": "APPROVAL_QUEUE_PREVIEW_V10",
        "pending_count": len(pending),
        "requests": pending,
        "auto_process_allowed": False,
        "requires_human_review": True,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "auto_calibration_allowed": False,
        "prompt_auto_injection_allowed": False,
        "real_trade_allowed": False,
    }
