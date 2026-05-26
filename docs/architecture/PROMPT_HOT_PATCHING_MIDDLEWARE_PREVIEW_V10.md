# Prompt Hot-Patching Middleware Preview Architecture v1.0

## Goal

Establish a preview-only, auditable pipeline for prompt hot-patching.

## Chain

```
Hermes PromptPatchPreview
→ ApprovalDecision
→ PromptPatchRequest
→ Middleware Render Preview
→ PromptPatchAudit
→ PromptPatchEvent → EventStore
```

## Not In Scope

- No real system_prompt write
- No OpenClaw runtime injection
- No prompt configuration file modification
- No auto activation
- No Hermes memory write
- No real Z9 write
- No real trade

## Architecture

v2.9.14 only proves the middleware preview chain is auditable.
Real runtime injection of prompt hot-patching must wait for a future version.
