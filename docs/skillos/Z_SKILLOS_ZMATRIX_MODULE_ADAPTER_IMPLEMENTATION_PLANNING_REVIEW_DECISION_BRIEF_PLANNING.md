# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — REVIEW_DECISION_BRIEF

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED | REVIEW PHASE

---

## §1 — Decision Brief Purpose

This document captures the key decisions made during the review phase.
Each decision is recorded with context, options considered, chosen option,
rationale, and implications. Decisions are binding and feed into the
REVIEW_DECISION_RECORD.

---

## §2 — Decision Framework

| Element | Description |
|---------|-------------|
| Decision ID | D-REV-### |
| Context | What prompted this decision |
| Options | Alternatives considered |
| Chosen | Selected option |
| Rationale | Why this option was chosen |
| Impact | What this decision affects |
| Reversibility | Can this be changed later |

---

## §3 — Key Decision Areas

### DA1: Adapter Enablement Sequence
| Field | Value |
|-------|-------|
| Decision ID | D-REV-001 |
| Context | Order in which adapters are enabled after planning approval |
| Options | (A) All at once, (B) Wave-based sequential, (C) One at a time |
| Chosen | (B) Wave-based sequential |
| Rationale | Safety — each wave proves its safety before next wave enables. Matches PRIORITY_WAVE_PLAN. |
| Impact | Implementation timeline, testing strategy, review cadence |
| Reversibility | Yes — can accelerate/decelerate waves |
| Status | ⏳ PENDING REVIEW |

### DA2: Evidence Storage Backend
| Field | Value |
|-------|-------|
| Decision ID | D-REV-002 |
| Context | Where evidence records are stored persistently |
| Options | (A) SQLite, (B) JSON file, (C) In-memory only, (D) External DB |
| Chosen | (A) SQLite with JSON file backup |
| Rationale | Portable, no external dependency, supports hash-chain verification, append-only |
| Impact | Evidence infrastructure, storage sizing, backup strategy |
| Reversibility | Yes — can migrate to other backends |
| Status | ⏳ PENDING REVIEW |

### DA3: Permission Model Granularity
| Field | Value |
|-------|-------|
| Decision ID | D-REV-003 |
| Context | How fine-grained the permission tokens should be |
| Options | (A) Coarse (read/write/admin), (B) Medium (12 tokens as defined), (C) Fine (per-adapter tokens) |
| Chosen | (B) Medium — 12 tokens covering key capability domains |
| Rationale | Coarse is unsafe; Fine adds complexity without proportional safety gain. Medium balances both. |
| Impact | PERMISSION_PLAN, contract definitions, enforcement complexity |
| Reversibility | Yes — tokens can be added/split with contract version bump |
| Status | ⏳ PENDING REVIEW |

### DA4: Contract Versioning Strategy
| Field | Value |
|-------|-------|
| Decision ID | D-REV-004 |
| Context | How adapter contracts are versioned and evolved |
| Options | (A) Semver only, (B) Hash-based, (C) Semver + hash |
| Chosen | (C) Semver + hash — human-readable semver with SHA-256 content hash |
| Rationale | Semver for human understanding; hash for cryptographic integrity verification |
| Impact | CONTRACT_PLAN, registry design, verification tooling |
| Reversibility | Low — foundational architectural decision |
| Status | ⏳ PENDING REVIEW |

### DA5: Test Coverage Threshold
| Field | Value |
|-------|-------|
| Decision ID | D-REV-005 |
| Context | Minimum acceptable test coverage for merge approval |
| Options | (A) 70% line, (B) 85% line, (C) 90% line + 85% branch |
| Chosen | (C) 90% line + 85% branch |
| Rationale | Safety-critical system; high coverage is non-negotiable for Tier 0/1 adapters |
| Impact | TEST_AND_PROOF_PLAN, CI pipeline, development effort |
| Reversibility | Yes — can adjust thresholds per-wave with justification |
| Status | ⏳ PENDING REVIEW |

---

## §4 — Decision Dependencies

```
D-REV-001 (Sequence) ──► D-REV-005 (Coverage)
                              │
D-REV-003 (Permissions) ──► D-REV-004 (Versioning)
                              │
D-REV-002 (Storage) ─────────┘
```

---

## §5 — Outstanding Questions

| # | Question | Needed For |
|---|----------|-----------|
| Q1 | Who is the assigned reviewer? | Review execution |
| Q2 | What is the review deadline? | Timeline planning |
| Q3 | Are there additional forbidden actions? | Scope completeness |
| Q4 | Is Wave 0 implementation authorized after review? | Implementation gate |
| Q5 | What is the evidence retention policy? | Storage sizing |

---

## §6 — Decision Communication

All decisions in this brief must be:
1. Recorded in REVIEW_DECISION_RECORD with full detail.
2. Communicated to all stakeholders before review closeout.
3. Reflected in affected planning documents (amend if needed).
4. Verified at MERGE_REVIEW gate.

---

## §7 — Governance

This decision brief is FUTURE_PLAN_ONLY. All decisions are PENDING review.
No decision is binding until the review phase is complete and the
REVIEW_DECISION_RECORD is finalized. All adapters remain DISABLED.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Review Decision Brief
