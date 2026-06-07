# Z-SkillOS Capability Invocation OS Composition Engine Implementation Plan

## Status
Z_SKILLOS_COMPOSITION_ENGINE_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Safe skill composition plan. No engine code.

## Composition Types
- Sequential A→B→C: evidence handoff at each step
- Parallel A∥B: independent branches, merge with conflict detection
- Conditional if A.output then B else C: branching with evidence
- Forbidden combinations: any chain touching T5, any chain with conflicting permissions
- Evidence handoff: each step passes evidence to next
- Failure degrade: single failure degrades chain, never blocks

## Safety Rules
- Conflict detection: detect conflicting skill requirements
- Permission inheritance: chain inherits highest tier permission
- Tier ceiling: chain tier = max(all skill tiers)
- Human gate propagation: if any skill requires human, entire chain requires human
- Rollback scope: chain rollback = reverse order with evidence
- No blind execution: every step validated before next

## Forbidden
- Chain with T5 skill (immediate deny)
- Chain bypassing contract validation
- Chain with production/broker/real_trade component
- Chain without evidence capture
- Chain without rollback plan

## Future Tests
- test_composition_sequential: A→B evidence handoff
- test_composition_parallel: A∥B merge
- test_composition_forbidden_T5: T5 chain denied
- test_composition_failure_degrade: failure does not block
- test_composition_permission_inheritance: max tier propagation

## No engine code. Level 5 remains BLOCKED.
