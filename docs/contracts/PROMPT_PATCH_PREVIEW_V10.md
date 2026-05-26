# Prompt Patch Preview Contract v1.0 — Preview Only, No Auto Injection

## Fields

patch_id, source_heuristic_ids, task_type, ticker, role, patch_text, preview_only, prompt_auto_injection_allowed

## Safety

- Preview only
- Auto injection: DISABLED
- Human approval required: TRUE
- No Hermes memory write
- No real Z9 write
- No real trade

## Hard Rules

- injection_allowed MUST be False
- prompt_auto_injection_allowed MUST be False
- requires_human_approval MUST be True
- Forbidden tokens (BUY/SELL/REAL_TRADE) MUST be redacted in patch_text
