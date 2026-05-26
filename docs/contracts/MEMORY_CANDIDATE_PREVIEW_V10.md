# MemoryCandidate Preview Contract v1.0 — Draft Only, No Auto Approval

## Fields

memory_candidate_id, candidate_version, source_event_id, mistake_type, severity, confidence, proposed_lesson, evidence_event_ids, status, requires_human_approval, created_at

## Safety

- MemoryCandidate is a DRAFT only
- Must NOT be APPROVED in preview mode
- Does NOT write Hermes memory
- Does NOT write Z9
- Does NOT auto calibrate
- Does NOT auto-modify strategy

## Status Enum

DRAFT, PENDING_REVIEW, APPROVED, REJECTED, QUARANTINED, EXPIRED, SUPERSEDED

This version only produces DRAFT and PENDING_REVIEW.
