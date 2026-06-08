# Wave0 Controlled Read-Only Execution Kill Switch Plan

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_KILL_SWITCH_PLAN_READY
FUTURE_PLAN_ONLY | docs-only | Level 5: BLOCKED

## Kill Switch Layers
- Master kill — overrides all requested true
- Runtime kill — blocks runtime gate
- Adapter framework kill — blocks framework gate
- Per-adapter kill — blocks individual adapter (github, docgen, docs, report)
- Evidence kill — blocks evidence sink
- Output kill — blocks output generation
- Emergency rollback — immediate all-disable

## Rules
- All kills default active (True = BLOCKED)
- Kill false must not enable anything
- Kill switch check runs before any planned adapter action
- Per-adapter kill overrides individual gate even if master is off

> Cap OS Wave0 | Controlled Exec Planning | Kill Switch | FUTURE_PLAN_ONLY