# Wave0 Controlled Read-Only Execution Config Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_CONFIG_PLAN_READY
FUTURE_PLAN_ONLY | docs-only | Level 5: BLOCKED

## Requested vs Enabled Separation
- `wave0_controlled_execution_requested` — records intent only, never enables
- `is_wave0_controlled_execution_enabled(config)` — always returns False in planning phase
- Adapter-specific requested flags: github_readonly, document_generation, local_docs_inspection, report_reading

## Config Rules
- Strict bool True only accepted as requested
- Non-bool truthy = disabled (string "true", int 1, etc. rejected)
- Env cannot enable (no os.environ bypass)
- Config parse error = disabled
- Missing config = disabled
- No default true

> Cap OS Wave0 | Controlled Exec Planning | Config Plan | FUTURE_PLAN_ONLY