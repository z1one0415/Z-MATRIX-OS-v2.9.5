# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — REVIEW_CHECKLIST

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED | REVIEW PHASE

---

## §1 — Review Checklist Purpose

This checklist defines all review checks that must be performed against
the planning package. Each check must be explicitly marked as PASS or FAIL
with evidence. Minimum 18 checks required — this document defines 22.

---

## §2 — Document Completeness Checks (C01-C05)

| ID | Check | Criteria | Result |
|----|-------|----------|--------|
| C01 | All 14 planning docs present | File count = 14 | ⏳ PENDING |
| C02 | Minimum line counts met | All planning ≥30, review ≥35, merge ≥30 | ⏳ PENDING |
| C03 | 7-section structure enforced | Every doc has exactly §1-§7 | ⏳ PENDING |
| C04 | FUTURE_PLAN_ONLY consistency | All docs marked FUTURE_PLAN_ONLY | ⏳ PENDING |
| C05 | Level 5 BLOCKED consistency | All docs marked Level 5 BLOCKED | ⏳ PENDING |

---

## §3 — Content Quality Checks (C06-C11)

| ID | Check | Criteria | Result |
|----|-------|----------|--------|
| C06 | Adapter coverage | All 5 first-batch adapters referenced | ⏳ PENDING |
| C07 | Forbidden actions completeness | ≥18 forbidden items, no gaps | ⏳ PENDING |
| C08 | Proof coverage completeness | ≥18 proofs, all safety categories | ⏳ PENDING |
| C09 | Risk register completeness | Review ≥12 risks, Merge ≥10 risks | ⏳ PENDING |
| C10 | Checklist item counts | Review ≥18, Merge ≥15 | ⏳ PENDING |
| C11 | No implementation drift | Zero code/config references in planning | ⏳ PENDING |

---

## §4 — Cross-Reference Integrity Checks (C12-C15)

| ID | Check | Criteria | Result |
|----|-------|----------|--------|
| C12 | Adapter names consistent | Same names across all docs | ⏳ PENDING |
| C13 | Risk tiers consistent | Same tier assignments across docs | ⏳ PENDING |
| C14 | Permission tokens consistent | Same token names across docs | ⏳ PENDING |
| C15 | File paths consistent | Same future paths across docs | ⏳ PENDING |

---

## §5 — Safety and Compliance Checks (C16-C19)

| ID | Check | Criteria | Result |
|----|-------|----------|--------|
| C16 | No Z8 execution referenced | Zero mentions of Z8 trade execution | ⏳ PENDING |
| C17 | No V3 trade/survival referenced | Zero mentions of production trading | ⏳ PENDING |
| C18 | No broker/production referenced | Zero broker, real_trade, portfolio refs | ⏳ PENDING |
| C19 | No external publish referenced | Zero external publication paths | ⏳ PENDING |

---

## §6 — Governance Checks (C20-C22)

| ID | Check | Criteria | Result |
|----|-------|----------|--------|
| C20 | DISABLED default declared | All adapters start DISABLED | ⏳ PENDING |
| C21 | Review gate conditions clear | REVIEW_GATE has 12 entry conditions | ⏳ PENDING |
| C22 | Merge gate conditions clear | MERGE_REVIEW has clear entry criteria | ⏳ PENDING |

---

## §7 — Checklist Summary

| Metric | Value |
|--------|-------|
| Total checks defined | 22 |
| Minimum required | 18 |
| PASS (preliminary) | 0 |
| PENDING | 22 |
| FAIL | 0 |
| Blocking issues | 0 |

**Status**: All 22 checks are PENDING reviewer execution. This checklist
is FUTURE_PLAN_ONLY. No checks have been executed yet.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Review Checklist
