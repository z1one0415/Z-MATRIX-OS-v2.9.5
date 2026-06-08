# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — REVIEW_DECISION_RECORD

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED | REVIEW PHASE | 10 PENDING

---

## §1 — Decision Record Purpose

This document records all decisions made during the review phase in a
structured, auditable format. Each decision has a unique ID, status,
and traceable rationale. This document is the authoritative source for
review-phase decisions and must contain at minimum 10 PENDING decisions.

---

## §2 — Decision Record Format

```
D-REV-NNN | STATUS | DATE | DECISION | RATIONALE | IMPACT | REVERSIBLE
```

---

## §3 — Decision Records (10 PENDING)

### D-REV-001
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve Wave-based sequential adapter enablement |
| Rationale | Safety-first approach; each wave proves safety before next |
| Impact | Implementation timeline extends but safety guarantees increase |
| Reversible | Yes |

### D-REV-002
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve SQLite + JSON backup for evidence storage |
| Rationale | Portable, no external deps, supports hash-chain verification |
| Impact | Evidence infrastructure design, storage sizing |
| Reversible | Yes |

### D-REV-003
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve 12-token medium-granularity permission model |
| Rationale | Balances safety (not too coarse) and complexity (not too fine) |
| Impact | Permission engine implementation complexity |
| Reversible | Yes |

### D-REV-004
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve Semver + SHA-256 hash for contract versioning |
| Rationale | Human-readable + cryptographically verifiable |
| Impact | Contract and registry design; verification tooling |
| Reversible | Low |

### D-REV-005
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve 90% line + 85% branch coverage threshold |
| Rationale | Safety-critical system requires high coverage |
| Impact | Test effort, CI pipeline configuration |
| Reversible | Yes |

### D-REV-006
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve evidence capture as MANDATORY for all adapters |
| Rationale | Traceability is non-negotiable for audit and debugging |
| Impact | All adapters must implement evidence capture; no opt-out |
| Reversible | Low |

### D-REV-007
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve DISABLED default with explicit enable gate |
| Rationale | Fail-closed posture; no adapter runs without explicit approval |
| Impact | All adapters start DISABLED; enable requires full gate pass |
| Reversible | No (foundational safety) |

### D-REV-008
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve 5-layer read-only enforcement (contract → permission → runtime → evidence → policy) |
| Rationale | Defense in depth; no single layer failure compromises safety |
| Impact | Implementation complexity increases but safety guarantees multiply |
| Reversible | Low |

### D-REV-009
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve Z8/V3/broker/production as FORBIDDEN scope |
| Rationale | These systems involve real trade/money; out of scope for Batch 1 |
| Impact | Clear boundary; no accidental production access |
| Reversible | No (scope boundary) |

### D-REV-010
| Field | Value |
|-------|-------|
| Status | ⏳ PENDING |
| Date | TBD |
| Decision | Approve immutable evidence hash chain with genesis block |
| Rationale | Tamper-evident audit trail; mandatory for compliance |
| Impact | Evidence store design; chain verification tooling |
| Reversible | Low |

---

## §4 — Decision Summary

| Status | Count |
|--------|-------|
| PENDING | 10 |
| APPROVED | 0 |
| REJECTED | 0 |
| DEFERRED | 0 |
| **TOTAL** | **10** |

---

## §5 — Decision Lifecycle

```
PROPOSED → PENDING → UNDER_REVIEW → APPROVED/REJECTED/DEFERRED
                                              │
                                              └──► IMPLEMENTED → VERIFIED
```

All 10 decisions are in PENDING state, awaiting reviewer assignment and
review phase execution.

---

## §6 — Post-Review Actions

After all decisions are APPROVED:
1. Update affected planning documents with decision outcomes.
2. Feed decisions into MERGE_REVIEW gate.
3. Reflect decisions in implementation contracts.
4. Archive decision record in immutable evidence store.

---

## §7 — Governance

This decision record is FUTURE_PLAN_ONLY. All 10 decisions are PENDING.
No decision is binding until approved by the reviewer. The record is
appended to as the review phase progresses. All adapters remain DISABLED.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Review Decision Record
> **Decisions**: 10 PENDING
