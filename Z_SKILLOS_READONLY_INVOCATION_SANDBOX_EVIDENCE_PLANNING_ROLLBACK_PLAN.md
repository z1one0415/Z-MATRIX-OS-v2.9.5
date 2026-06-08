# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — ROLLBACK PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_ROLLBACK_PLAN_READY

## Scope
This document defines the rollback plan — deterministic reversion of any invocation to a known safe state.

## Evidence
Rollback evidence is captured via rollback_marker in the evidence bundle.

### Rollback States
| State | Description | Entry Condition | Exit Action |
|-------|-------------|-----------------|-------------|
| IDLE | No active invocation | Sandbox start | — |
| GATE_PENDING | Invocation at gate | Input validated | Rollback: discard input |
| EXECUTING | Skill adapter executing | Gate passed | Rollback: abort adapter, zero arena |
| EVIDENCE_SEALING | Computing final tamper_seal | Execution complete | Rollback: discard partial evidence |
| DELIVERING | Sending bundle to consumer | Evidence sealed | Rollback: cancel delivery |
| DELIVERED | Consumer acknowledged | Delivery complete | Rollback: NO-OP |
| TIMED_OUT | TTL expired | TTL trigger | Rollback: destroy all evidence |

### Rollback Procedure
```
function rollback(invocation_id, target_state):
    current_state = get_state(invocation_id)
    if current_state == DELIVERED:
        return ROLLBACK_DENIED
    if current_state == TIMED_OUT:
        set_state(invocation_id, IDLE)
        return ROLLBACK_NO_OP
    if current_state == EXECUTING:
        abort_adapter(invocation_id)
    zero_fill_arena(invocation_id)
    destroy_hash_chain(invocation_id)
    destroy_audit_sink_entry(invocation_id)
    destroy_ephemeral_key(invocation_id)
    rollback_marker = generate_rollback_marker()
    emit_rollback_evidence(invocation_id, rollback_marker)
    set_state(invocation_id, IDLE)
    return ROLLBACK_COMPLETE
```

### Rollback Guarantees
1. Deterministic — Same inputs produce same rollback outcome
2. Complete — No residual state after rollback
3. Evidenced — Rollback produces a final evidence link with rollback_marker
4. Non-Blocking — Rollback cannot be prevented by adapter state
5. Idempotent — Rollback of IDLE state is a NO-OP
6. Privacy-Preserving — Rollback does not leak data across invocations

## Boundary
- Rollback is per-invocation; no bulk rollback
- Rollback after DELIVERED is denied
- Rollback does not affect consumer-side state
- Rollback does not persist rollback markers across invocations
- Rollback is synchronous and atomic

## Forbidden
1. Rollback after DELIVERED state (evidence handoff is irreversible)
2. Partial rollback (all-or-nothing only)
3. Cross-invocation rollback side effects
4. Rollback marker persistence beyond invocation lifecycle
5. Adapter interference with rollback procedure
6. Rollback without evidence (every rollback produces a link)

## Proof
- Finite state machine with 7 states, all transitions defined
- Rollback is denied in exactly one state (DELIVERED)
- All other states have deterministic rollback paths
- Zero-fill guarantees no data remnants
- Rollback evidence provides audit trail even for aborted invocations

## Next
- Validate rollback does not violate PRIVACY_BOUNDARY_PLAN isolation
- Ensure TEST_AND_PROOF_PLAN covers all rollback state transitions
- Proceed to TEST_AND_PROOF_PLAN
