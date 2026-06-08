# Wave0 Controlled Read-Only Execution Scope

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_SCOPE_READY
Branch: plan/...controlled-readonly-execution-planning @ 86b5851 | Level 5: BLOCKED

## In Scope
FUTURE_PLAN_ONLY. Docs-only planning for controlled read-only execution.

### Input Sources (in gated order)
1. **Synthetic input**: mock/test data only, verified by canary gate
2. **Provided input**: human-supplied file paths, verified by permission gate
3. **Local controlled sandbox**: read docs/ directory, verified by adapter gate
4. **Future GitHub metadata-only**: requires separate explicit gate (NOT in this phase)

### Explicitly Out of Scope
- Real GitHub call (requires separate gate, not planned here)
- Z-MATRIX module call (permanently forbidden)
- File write / branch mutation / merge / publish
- Network call beyond GitHub read (future, gated)
- Production / broker / real_trade

## Deliverables
14 planning docs covering gate model, config, kill switch, permissions, evidence, adapter priority, canary deployment, rollback, test/proof matrix, forbidden actions.

## Dependency
WAVE0_EXECUTION_ENABLEMENT_P0_POST_MERGE_SEALED (b62d6e4). All enabled() functions in P0 return False.

## Boundary
No runtime enablement. No adapter execution enablement. No capability execution. No real adapter call. No network call. No file read/write. No Z-MATRIX module calling. No production/broker/real_trade. Level 5 remains BLOCKED.

## Next
Scope finalized → planning docs → review gate

> Cap OS Wave0 | Controlled Exec Planning | Scope | FUTURE_PLAN_ONLY | Level 5 BLOCKED