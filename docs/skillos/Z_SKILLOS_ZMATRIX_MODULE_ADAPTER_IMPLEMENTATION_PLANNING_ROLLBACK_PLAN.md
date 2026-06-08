# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — ROLLBACK_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Rollback Philosophy

Every adapter and every configuration change must be reversible. The rollback
plan defines degraded operation modes, kill-switch mechanisms, and evidence
preservation during rollback. Safety is non-negotiable — the system must fail
closed, not open.

---

## §2 — Rollback Triggers

| Trigger | Severity | Action |
|---------|----------|--------|
| Contract violation detected | CRITICAL | Immediate KILL + rollback |
| Permission bypass detected | CRITICAL | Immediate KILL + rollback |
| Forbidden action executed | CRITICAL | Immediate KILL + rollback |
| Evidence chain broken | CRITICAL | Immediate KILL + rollback |
| Output schema mismatch (≥3 consecutive) | HIGH | DEGRADE + investigate |
| Timeout rate > 10% in rolling window | HIGH | DEGRADE + investigate |
| Error rate > 5% in rolling window | MEDIUM | Alert + monitor |
| Memory usage > 80% threshold | MEDIUM | DEGRADE + alert |

---

## §3 — Degradation Modes

### Mode 1: FULL_OPERATION
- All adapters ENABLED
- Full evidence capture
- Full permission enforcement

### Mode 2: READONLY_ONLY
- Only Tier 0 adapters ENABLED (A1-A4)
- Tier 1 adapters (A5) DISABLED
- All write operations blocked

### Mode 3: OBSERVATION_ONLY
- All adapters DISABLED
- Registry and evidence still readable
- No adapter execution permitted

### Mode 4: FULL_KILL
- All adapters KILLED
- Registry locked
- Evidence store sealed
- Manual intervention required to restore

---

## §4 — Kill Switch Mechanism

```python
KILL_SWITCH_CONFIG = {
    "global_kill": False,          # Kills ALL adapters immediately
    "per_adapter_kill": {          # Per-adapter kill switches
        "capability_registry_readonly": False,
        "z9_memory_review_readonly": False,
        "z2_research_output_readonly": False,
        "local_report_reading": False,
        "document_generation_in_memory": False,
    },
    "kill_on_evidence_break": True,  # Auto-kill if evidence chain breaks
    "kill_on_contract_violation": True,  # Auto-kill if contract violated
}
```

---

## §5 — Rollback Procedure

1. **Detect**: Trigger condition activates (automatic or manual).
2. **Isolate**: Affected adapter(s) moved to DEGRADED or KILLED state.
3. **Evidence**: Rollback event logged with full evidence record.
4. **Notify**: Alert dispatched to audit channel.
5. **Investigate**: Root cause analysis performed.
6. **Remediate**: Fix implemented and tested.
7. **Re-enable**: Graduated re-enablement through wave gates.
8. **Close**: Rollback incident closed with post-mortem evidence.

---

## §6 — State Preservation During Rollback

| Artifact | Preserved? | How |
|----------|-----------|-----|
| Evidence chain | ✅ | Sealed, no truncation |
| Registry state | ✅ | Pre-rollback snapshot |
| Contract hashes | ✅ | Immutable records |
| Invocation logs | ✅ | Append-only audit |
| In-flight invocations | ⚠️ | Completed with KILLED status |
| Pending invocations | ❌ | Rejected with ROLLBACK status |

---

## §7 — Governance

This rollback plan is FUTURE_PLAN_ONLY. Kill switches, degradation modes,
and rollback procedures are defined but not implemented. No adapter shall
be ENABLED until rollback infrastructure is operational and verified.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Rollback Plan
