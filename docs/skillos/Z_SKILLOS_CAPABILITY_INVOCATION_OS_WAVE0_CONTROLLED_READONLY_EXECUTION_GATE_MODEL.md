# Wave0 Controlled Read-Only Execution Gate Model

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_GATE_MODEL_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## Architecture
FUTURE_PLAN_ONLY. Six-layer gate architecture for controlled read-only execution:

```
Request → [Runtime Gate] → [Adapter Framework Gate] → [Wave0 P0 Gate] → [Individual Adapter Gate] → [Permission Gate] → [Evidence Gate] → Controlled Action
```

## Gate Definitions

| Gate | Purpose | P0 State | Future State |
|:--|:--|:--|:--|
| Runtime Gate | Controls runtime execution ability | DISABLED | REQUESTED→ENABLED (human gate) |
| Adapter Framework Gate | Controls adapter framework loading | DISABLED | REQUESTED→ENABLED (human gate) |
| Wave0 P0 Gate | Controls Wave0 enablement module | DISABLED | REQUESTED→ENABLED (human gate) |
| Individual Adapter Gate | Controls specific adapter (github/docgen/docs/report) | DISABLED | REQUESTED→ENABLED (per-adapter gate) |
| Permission Gate | Controls what operations are allowed | ALL_DENIED | READ_ONLY/GENERATION_ONLY (gated) |
| Evidence Gate | Controls evidence collection | NOOP | IN_MEMORY_HASH_ONLY (explicit gate) |

## Gate Rules
- All gates strict bool True only: non-bool truthy = disabled
- Any gate false / missing / malformed = disabled / noop
- No direct env enablement (os.environ cannot bypass)
- All gates default disabled (no default true)
- Kill switch overrides all gates regardless of state
- ENABLED state reachable only via explicit human gate + all gates pass

## Gate Evaluation Sequence
1. Check kill switch (any active → immediate DENY)
2. Evaluate runtime gate (strict bool)
3. Evaluate adapter framework gate (strict bool)
4. Evaluate Wave0 P0 gate (strict bool)
5. Evaluate individual adapter gate (strict bool)
6. Evaluate permission gate (READ_ONLY/GENERATION_ONLY only)
7. Evaluate evidence gate (NOOP/IN_MEMORY only)
8. If all pass → PLAN_ONLY (P0) or CONTROLLED_ACTION (future)

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). P0 triple gate already implemented.

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. Level 5 remains BLOCKED.

## Next
Gate model defined → config planning → implementation gate

> Cap OS Wave0 | Controlled Exec Planning | Gate Model | FUTURE_PLAN_ONLY | Level 5 BLOCKED