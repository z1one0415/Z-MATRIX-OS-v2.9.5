# Prompt Middleware Contract v1.0

## Purpose

Prompt Middleware is the preview chain for prompt hot-patching.
It is NOT the real injection chain.

## Chain

Hermes PromptPatchPreview → ApprovalDecision → PromptPatchRequest → Middleware Render Preview → PromptPatchAudit → PromptPatchEvent → EventStore

## Safety

- APPROVED_PREVIEW does NOT equal injected
- PromptPatchEvent does NOT equal system_prompt modified
- No runtime injection
- No system_prompt write
- No prompt auto injection
- No Hermes memory write
- No real Z9 write
- No real trade
