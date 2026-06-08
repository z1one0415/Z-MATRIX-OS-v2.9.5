# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — PRIORITY_WAVE_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Priority Wave Philosophy

Adapter implementation follows a strict wave-based priority model. Each wave
must be fully implemented, tested, reviewed, and merged before the next wave
can begin. This prevents dependency inversion and ensures each wave's safety
guarantees are proven before more complex adapters are built.

---

## §2 — Wave Definitions

### Wave 0: Foundation (Risk Tier 0)
| Order | Adapter | Rationale |
|-------|---------|-----------|
| W0.1 | `capability_registry_readonly` | Registry must exist before other adapters can register |
| W0.2 | `z9_memory_review_readonly` | Memory recall is prerequisite for research context |

**Wave 0 Gate**: Both adapters pass all tests and review before Wave 1 starts.

### Wave 1: Research Access (Risk Tier 0)
| Order | Adapter | Rationale |
|-------|---------|-----------|
| W1.1 | `z2_research_output_readonly` | Research output reading depends on registry |
| W1.2 | `local_report_reading` | Local file reading depends on path validation from registry |

**Wave 1 Gate**: All four read-only adapters pass tests and review.

### Wave 2: Controlled Write (Risk Tier 1)
| Order | Adapter | Rationale |
|-------|---------|-----------|
| W2.1 | `document_generation_in_memory` | Only write-capable adapter; requires all read-only infrastructure proven |

**Wave 2 Gate**: Full system integration test with all five adapters.

---

## §3 — Wave Dependency Graph

```
Wave 0 ──────────────► Wave 1 ──────────────► Wave 2
│                      │                      │
├─ capability_registry ├─ z2_research_output  ├─ document_generation
└─ z9_memory_review    └─ local_report_reading
       │                      │
       └──────────────────────┘
              depends on
```

---

## §4 — Per-Wave Exit Criteria

| Criterion | Wave 0 | Wave 1 | Wave 2 |
|-----------|--------|--------|--------|
| Unit tests pass | ✅ | ✅ | ✅ |
| Integration tests pass | ✅ | ✅ | ✅ |
| Contract validation | ✅ | ✅ | ✅ |
| Evidence chain verification | ✅ | ✅ | ✅ |
| Permission enforcement | ✅ | ✅ | ✅ |
| Read-only policy check | ✅ | ✅ | N/A (A5 has write) |
| Review gate passed | ✅ | ✅ | ✅ |
| Merge gate passed | ✅ | ✅ | ✅ |
| Golden regression suite | ✅ | ✅ | ✅ |

---

## §5 — Wave Sequencing Timeline (Future)

| Wave | Estimated Effort | Dependencies |
|------|-----------------|--------------|
| Wave 0 | 3-5 days | None |
| Wave 1 | 3-5 days | Wave 0 complete |
| Wave 2 | 2-3 days | Wave 1 complete |

Note: Timeline is FUTURE_PLAN_ONLY. Actual implementation dates are TBD
after planning gates are satisfied.

---

## §6 — Wave Interruption Protocol

If a wave fails any exit criterion:
1. Implementation PAUSES immediately.
2. Root cause analysis is performed.
3. Fix is implemented and all tests re-run.
4. Wave restarts from the failing checkpoint.
5. No subsequent wave work begins until the current wave passes.

---

## §7 — Governance

This priority wave plan is FUTURE_PLAN_ONLY. No wave implementation may
begin until all planning-review-merge gates are satisfied. Wave order is
immutable — no parallel wave execution, no wave reordering without formal
amendment.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Priority Wave Plan
