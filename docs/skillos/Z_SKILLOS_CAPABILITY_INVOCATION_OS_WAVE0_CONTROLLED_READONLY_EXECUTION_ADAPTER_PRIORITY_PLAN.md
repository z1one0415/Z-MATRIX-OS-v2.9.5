# Wave0 Controlled Read-Only Execution Adapter Priority Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_ADAPTER_PRIORITY_PLAN_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Priority Order
FUTURE_PLAN_ONLY. Recommended enablement order for controlled read-only execution adapters:

| Priority | Adapter | Input Source | Gate Required | Rationale |
|:--:|:--|:--|:--|:--|
| A | **Report Reading** | Provided-input only | All 6 gates | Safest: reads local files only, no network |
| B | **Document Generation** | In-memory only | All 6 gates + output kill off | No file writes, in-memory generation |
| C | **Local Docs Inspection** | Controlled sandbox | All 6 gates + sandbox gate | Reads docs/ directory only |
| D | **GitHub Readonly** | Metadata-only, later | All 6 gates + separate GitHub gate | Highest risk: network call |

## Priority Rules
- DO NOT start with GitHub real call (highest risk)
- Each adapter requires its own explicit gate evaluation
- Adapter priority can be reordered by human decision
- Later adapters inherit gate trust from earlier successes
- Failure in earlier adapter blocks later adapters
- No adapter execution in this planning phase

## Evidence
- Report Reading: 0 network risk, tests local file parsing
- Document Generation: 0 file write risk if in-memory only
- Local Docs Inspection: 0 external risk if sandboxed
- GitHub Readonly: network call risk, requires separate security review

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4).

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. No GitHub call in this phase. Level 5 remains BLOCKED.

## Next
Adapter priority → canary plan → rollback plan

> Cap OS Wave0 | Controlled Exec Planning | Adapter Priority | FUTURE_PLAN_ONLY | Level 5 BLOCKED