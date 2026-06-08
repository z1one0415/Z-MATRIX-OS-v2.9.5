# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — READONLY_POLICY_PLAN

> Status: _READONLY_POLICY_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

Read vs Write classification for all 19 modules:
Read operations (allowed Waves A/B): query memory (Z9), parse research output, query capability registry, validate TruthGate, execute chain research, scoring, execution plans, survival sandbox, B/D/R Matrix scans, Flow A RC pipeline.
Write operations — filesystem only (allowed Waves A/B): generate local report, generate document, write to EventStore.
Write operations — state mutation (Wave C only): modify portfolio state, execute broker order, deploy to production, execute real trade.

Filesystem writes exception rationale: local reports/documents write to local filesystem only (memory palace), do NOT modify Z-MATRIX system state, do NOT affect running modules, are idempotent (same input = same output).

## 3. Evidence / Dependency

5 enforcement mechanisms: (1) Contract Precondition — adapter declares read/write classification. (2) Permission Gate — tier check before execution. (3) Side Effect Audit — post-execution audit for undeclared writes. (4) Filesystem Sandbox — Wave A/B restricted directories. (5) Event Log Audit — all writes logged via EventStore.

Detection pipeline (5 stages): Contract declares r/w → Permission gate checks tier → Filesystem sandbox restricts paths → Post-execution side effect audit → Violation triggers EventStore alert + execution blocked.

## 4. Boundary

What constitutes Write (forbidden Waves A/B): modifying Z-MATRIX database/state, updating portfolio positions, sending broker orders, modifying config files, updating capability registry, mutating in-memory module state, emitting trade signals externally.
What does NOT constitute Write (allowed Waves A/B): writing report files to memory palace, logging locally, EventStore writes, computing in-memory results, reading from any module.

## 5. Forbidden Actions

F-RO01 Wave A state mutation (CRITICAL) | F-RO02 Wave B state mutation (CRITICAL) | F-RO03 Outside approved paths (HIGH) | F-RO04 Runtime config modification (HIGH) | F-RO05 Undeclared write (CRITICAL) | F-RO06 Sandbox bypass (CRITICAL) | F-RO07 Trade signals from A/B (CRITICAL) | F-RO08 Registry mod non-T0 (CRITICAL) | F-RO09 Production DB writes (CRITICAL) | F-RO10 Audit bypass (HIGH)

## 6. Proof / Requirements

R-RO01: 19 modules classified | R-RO02: Wave A 0 state mutations | R-RO03: Wave B 0 state mutations | R-RO04: FS exception 4 conditions | R-RO05: 5 enforcement mechanisms | R-RO06: 5-stage detection | R-RO07: Write definition explicit | R-RO08: Forbidden ≥10

## 7. Next

INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md → TEST_AND_PROOF_PLAN.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-READONLY_POLICY_PLAN-v1.0
