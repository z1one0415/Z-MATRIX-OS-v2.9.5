# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — OVERVIEW

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED
> **Author**: Z2 Analyst (subagent)

---

## §1 — Purpose and Intent

This document serves as the master overview for the Z-MATRIX Module Adapter implementation
planning package. It defines the strategic framework for adapting Z-MATRIX-OS v2.9.5
capabilities into the Z-SkillOS capability invocation OS, ensuring read-only safety,
evidence traceability, and deterministic contract enforcement.

The planning package covers **14 planning documents**, **7 review documents**, and **5 merge**
**documents** — 26 docs in total — all docs-only with zero code changes.

---

## §2 — Strategic Context

Z-MATRIX-OS v2.9.5 provides core research and analysis pipelines (B-Matrix, D-Matrix,
R-Matrix, Flow A RC). Z-SkillOS capability invocation OS needs adapters to safely invoke
these capabilities as managed skills. This implementation planning defines the contract,
registry, permission, schema, evidence, priority-wave, rollback, and test-proof layers
before a single line of adapter code is written.

---

## §3 — First Batch Adapters (Scope)

| # | Adapter | Module | Mode |
|---|---------|--------|------|
| 1 | `capability_registry_readonly` | Capability Registry | Read-only inspection |
| 2 | `z9_memory_review_readonly` | Z9 Memory Review | Read-only memory recall |
| 3 | `z2_research_output_readonly` | Z2 Research Output | Read-only report reading |
| 4 | `local_report_reading` | Local Report Reading | Read-only file inspection |
| 5 | `document_generation_in_memory` | Document Generation | In-memory write only |

---

## §4 — Future Files (NOT in this batch)

Future adapter implementations will reside at:
`skillos/capability_invocation_os/zmatrix_adapters/*.py`

These are **explicitly out of scope** for the current planning package.

---

## §5 — Explicit Forbidden Scope (≥18 items)

| # | Forbidden Action | Rationale |
|---|-----------------|-----------|
| 1 | Z8 execution | No trade execution path |
| 2 | V3 trade/survival | No production trading |
| 3 | Broker connectivity | No external broker calls |
| 4 | Real trade routing | No real-money operations |
| 5 | Production deployment | No live environment push |
| 6 | Portfolio modification | No position changes |
| 7 | External publish | No outbound publications |
| 8 | Z8 bridge activation | No Z8 pre-check execution |
| 9 | Live order submission | No order routing |
| 10 | Position sizing computation | No risk sizing |
| 11 | Account balance access | No balance queries |
| 12 | Market data streaming | No real-time feeds |
| 13 | OMS integration | No order management system |
| 14 | Risk engine invocation | No risk system calls |
| 15 | Compliance check execution | No compliance runs |
| 16 | Settlement reconciliation | No settlement ops |
| 17 | P&L calculation | No profit/loss computation |
| 18 | Alert/notification dispatch | No outbound alerts |
| 19 | Webhook/API callback | No external callbacks |
| 20 | Configuration mutation of live systems | No config changes |

---

## §6 — Document Inventory

### Planning (14 docs, ≥30 lines each)
| # | Document | Purpose |
|---|----------|---------|
| P01 | OVERVIEW | Master planning overview (this doc) |
| P02 | SCOPE | Scope boundary definition |
| P03 | FILE_LEVEL_PLAN | File-level implementation plan |
| P04 | CONTRACT_PLAN | Adapter contract standard |
| P05 | REGISTRY_PLAN | Capability registry design |
| P06 | PERMISSION_PLAN | Permission model |
| P07 | READONLY_POLICY_PLAN | Read-only enforcement policy |
| P08 | SCHEMA_PLAN | Input/output schema |
| P09 | EVIDENCE_PLAN | Evidence capture and traceability |
| P10 | PRIORITY_WAVE_PLAN | Priority wave sequencing |
| P11 | ROLLBACK_PLAN | Rollback and degrade strategy |
| P12 | TEST_AND_PROOF_PLAN | Test harness and proof plan (≥18 proofs) |
| P13 | PLANNING_CLOSEOUT | Planning phase closeout |
| P14 | PLANNING_SEAL | Planning seal and sign-off |

### Review (7 docs, ≥35 lines each)
| # | Document | Purpose |
|---|----------|---------|
| R01 | REVIEW_GATE | Review entry gate |
| R02 | REVIEW_CHECKLIST | Review checklist (≥18 checks) |
| R03 | REVIEW_RISK_REGISTER | Review risk register (≥12 risks) |
| R04 | REVIEW_DECISION_BRIEF | Review decision brief |
| R05 | REVIEW_DECISION_RECORD | Review decision record (10 PENDING) |
| R06 | REVIEW_MERGE_READINESS | Merge readiness assessment |
| R07 | REVIEW_CLOSEOUT | Review phase closeout |

### Merge (5 docs, ≥30 lines each)
| # | Document | Purpose |
|---|----------|---------|
| M01 | MERGE_REVIEW | Merge review gate |
| M02 | MERGE_CHECKLIST | Merge checklist (≥15 checks) |
| M03 | MERGE_RISK_REGISTER | Merge risk register (≥10 risks) |
| M04 | MERGE_DECISION_BRIEF | Merge decision brief |
| M05 | MERGE_CLOSEOUT | Merge phase closeout |

---

## §7 — Governance and Blocked State

**Level 5 BLOCKED**: All adapters are DISABLED by default. No adapter shall be enabled
without passing the full planning → review → merge gate pipeline. Every document in
this package must achieve `APPROVED` status before any code implementation begins.

**FUTURE_PLAN_ONLY**: This package contains only planning documents. No code,
configuration, or runtime changes are included. Implementation is deferred until
all planning gates are satisfied.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Z-MATRIX Module Adapter Implementation Planning
