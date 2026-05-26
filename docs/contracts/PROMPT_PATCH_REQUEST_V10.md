# Prompt Patch Request Contract v1.0

## Fields

prompt_patch_request_id, request_version, request_type, task_context, prompt_patch_preview_id, prompt_patch_preview, approval_decision_id, approval_status, status, created_at, safety

## Rules

- No approval_decision → PENDING_APPROVAL
- With approval_decision + APPROVED → APPROVED_PREVIEW
- APPROVED_PREVIEW does NOT enable runtime injection
- No system_prompt write
- No Hermes memory write
- No real trade
