# Wave0 Controlled Read-Only Execution Permission Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_PERMISSION_PLAN_READY
FUTURE_PLAN_ONLY | docs-only | Level 5: BLOCKED

## Allowed Permissions (future, gated)
- READ_ONLY — read existing resources
- GENERATION_ONLY — in-memory generation only

## Denied Permissions (always)
- WRITE — no file/branch mutation
- MERGE — no merge operations
- PUBLISH — no external publish
- PRODUCTION — no production access
- BROKER — no broker access
- REAL_TRADE — no real trade access
- NETWORK — no network calls (unless future explicit read gate)
- Z_MATRIX_MODULE — no Z-MATRIX module calls

## Rules
- Unknown permission = denied
- Missing permission = denied
- Generation-only is non-execution
- All denied unless future explicit gate

> Cap OS Wave0 | Controlled Exec Planning | Permission Plan | FUTURE_PLAN_ONLY