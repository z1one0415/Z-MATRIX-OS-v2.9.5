# Wave0 Controlled Read-Only Execution P1 Canary Adapter Sequence Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P1_CANARY_ADAPTER_SEQUENCE_PLAN_READY
Branch: plan/...p1-canary-planning @ 2c0d7ae | Level 5: BLOCKED

## Priority Sequence
FUTURE_PLAN_ONLY. Recommended enablement order for P1 canary adapters.

### Sequence (A → D)
| Priority | Adapter | Input Source | Gate Required | Rationale |
|:--:|:--|:--|:--|:--|
| **A** | report_reading | Provided-input only | All 9 gates | Safest: reads local files, no network, provided by human |
| **B** | document_generation | In-memory only | All 9 gates + output kill off | No file writes, in-memory generation only |
| **C** | local_docs_inspection | Controlled sandbox | All 9 gates + sandbox gate | Reads docs/ directory, controlled path |
| **D** | github_metadata | Separate future gate | All 9 gates + explicit GitHub gate | Highest risk: potential network call |

### Sequence Rules
- DO NOT start with GitHub real call (requires separate security review)
- Each adapter requires its own explicit gate evaluation
- Adapter priority can be reordered by human decision
- Failure in earlier adapter blocks later adapters in sequence
- No adapter execution in this planning phase
- Z-MATRIX module adapter permanently forbidden

## Dependency
WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (b3ccd3f).

## Boundary
No runtime enablement. No adapter execution enablement. No GitHub call in P1. No Z-MATRIX adapter. Level 5 BLOCKED.

> Cap OS Wave0 | Controlled Exec P1 Canary | Adapter Sequence | A→D | FUTURE_PLAN_ONLY | Level 5 BLOCKED