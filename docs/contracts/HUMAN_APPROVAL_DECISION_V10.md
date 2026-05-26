# Human Approval Decision Contract v1.0

## Fields

approval_decision_id, decision_version, approval_request_id, source_preview_id, decision, result_status, human_operator, rationale, created_at, safety

## Decision Mapping

APPROVE → APPROVED
REJECT → REJECTED
QUARANTINE → QUARANTINED
REQUEST_MORE_EVIDENCE → PENDING_REVIEW

## Critical Boundaries

APPROVE does NOT imply:
- Hermes memory write
- Auto calibration
- Prompt auto injection
- Auto parameter change
