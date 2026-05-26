# Approval Request Contract v1.0

## Fields

approval_request_id, request_version, request_type, source_preview_id, source_preview, requested_by, reason, status, requires_human_approval, created_at, safety

## Rules

- request_type must be in APPROVAL_REQUEST_TYPES
- status is always PENDING_REVIEW on creation
- Does NOT write Hermes memory
- Does NOT write Z9
- Does NOT auto calibrate
- Does NOT auto inject prompts
