# Wave0 Controlled Read-Only Execution Adapter Priority Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_ADAPTER_PRIORITY_PLAN_READY
FUTURE_PLAN_ONLY | docs-only | Level 5: BLOCKED

## Future Enablement Order (recommended)
A. **report_reading** — provided-input only, read local reports first
B. **document_generation** — in-memory only, no file writes
C. **local_docs_inspection** — controlled sandbox only, read docs/ directory
D. **github_readonly** — metadata-only later, requires separate gate

## Rules
- DO NOT start with GitHub real call
- Each adapter requires its own explicit gate
- Adapter priority can be reordered by human decision
- No adapter execution in this planning phase

> Cap OS Wave0 | Controlled Exec Planning | Adapter Priority | FUTURE_PLAN_ONLY