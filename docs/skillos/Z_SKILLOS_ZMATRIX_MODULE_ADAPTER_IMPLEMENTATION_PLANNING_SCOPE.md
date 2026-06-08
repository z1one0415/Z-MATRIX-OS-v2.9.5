# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — SCOPE

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Scope Statement

This document defines the precise boundaries of the Z-MATRIX Module Adapter
implementation planning effort. It establishes what is IN scope, what is OUT
of scope, and what is explicitly FORBIDDEN for the first batch of five adapters.

---

## §2 — In-Scope Adapters (Batch 1)

| # | Adapter Name | Function | Risk Tier |
|---|-------------|----------|-----------|
| 1 | `capability_registry_readonly` | Read-only inspection of capability registry entries | Tier 0 |
| 2 | `z9_memory_review_readonly` | Read-only recall from Z9 memory review store | Tier 0 |
| 3 | `z2_research_output_readonly` | Read-only access to Z2 research output reports | Tier 0 |
| 4 | `local_report_reading` | Read-only file inspection of local reports | Tier 0 |
| 5 | `document_generation_in_memory` | In-memory document generation (no disk write) | Tier 1 |

All five adapters are read-only or in-memory-only. No adapter in Batch 1
performs any write, execution, or side-effect operation.

---

## §3 — Out of Scope (Explicit)

| # | Item | Reason |
|---|------|--------|
| 1 | Z8 execution bridge | Requires trade routing — FORBIDDEN |
| 2 | V3 trade/survival engine | Production trading system |
| 3 | Broker connectivity | External API calls |
| 4 | Real trade operations | Monetary risk |
| 5 | Production deployment | Live environment |
| 6 | Portfolio management | Position modification |
| 7 | External publish | Outbound communication |
| 8 | Market data streaming | Real-time data feed |
| 9 | OMS integration | Order management |
| 10 | Risk engine calls | Risk computation |

---

## §4 — Future Files (Post-Planning)

All adapter implementations will reside at:
```
skillos/capability_invocation_os/zmatrix_adapters/
├── capability_registry_readonly.py
├── z9_memory_review_readonly.py
├── z2_research_output_readonly.py
├── local_report_reading.py
└── document_generation_in_memory.py
```

These are NOT part of the current planning package.

---

## §5 — Deliverable Boundaries

| Deliverable | Type | Count |
|------------|------|-------|
| Planning docs | Markdown | 14 |
| Review docs | Markdown | 7 |
| Merge docs | Markdown | 5 |
| Code files | Python | 0 (FUTURE) |
| Config files | YAML/JSON | 0 (FUTURE) |
| Test files | Python | 0 (FUTURE) |

---

## §6 — Constraint Matrix

| Constraint | Value |
|-----------|-------|
| Minimum planning doc length | ≥30 lines |
| Minimum review doc length | ≥35 lines |
| Minimum merge doc length | ≥30 lines |
| Review checklist items | ≥18 |
| Review risk register items | ≥12 |
| Merge checklist items | ≥15 |
| Merge risk register items | ≥10 |
| Test proofs | ≥18 |
| Forbidden items enumerated | ≥18 |
| Sections per document | 7 |
| All adapters default state | DISABLED |

---

## §7 — Governance

This scope is FROZEN for the current planning iteration. Any scope change requires
a formal scope amendment document and re-approval through the planning gate.
No implementation may begin until all planning gates are satisfied.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Scope
