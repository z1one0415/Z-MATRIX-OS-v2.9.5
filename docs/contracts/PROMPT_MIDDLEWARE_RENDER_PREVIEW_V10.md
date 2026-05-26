# Prompt Middleware Render Preview Contract v1.0

## Fields

render_id, render_version, mode, prompt_patch_request_id, base_prompt_preview, rendered_prompt_preview, patch_text, render_status, created_at

## Safety

- PREVIEW_ONLY mode
- Does NOT write real system prompt
- Does NOT inject into runtime
- Does NOT modify prompt configuration files
- APPROVED_PREVIEW is NOT injection
