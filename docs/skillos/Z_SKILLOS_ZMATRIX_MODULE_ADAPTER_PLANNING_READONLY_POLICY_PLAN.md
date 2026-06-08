# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — READONLY_POLICY_PLAN

> Status: _READONLY_POLICY_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Policy: Waves A/B strictly read-only to Z-MATRIX state
Hardened: 2026-06-08

## 2. Scope

READ operations (allowed Waves A/B): Query memory (Z9), parse research output, query capability registry, validate TruthGate, chain research, scoring, execution plans, survival sandbox, B/D/R Matrix scans, Flow A RC pipeline.

WRITE operations — FILESYSTEM ONLY (allowed Waves A/B): Generate local report (memory palace path only), generate document (docs output path only), write to EventStore (local event log). Four conditions: (a) pre-approved memory palace path, (b) idempotent operation, (c) logged to EventStore, (d) no downstream state mutation.

WRITE operations — STATE MUTATION (Wave C ONLY, FORBIDDEN Waves A/B): Modify portfolio positions, execute broker orders, deploy to production, real trades, modify Z-MATRIX database/config, update capability registry at runtime, mutate in-memory module state, emit trade signals externally.

## 3. Evidence / Dependency

5 enforcement mechanisms: EM1 Contract Precondition (r/w classification declared) | EM2 Permission Gate (tier check before execution) | EM3 Side Effect Audit (post-execution undeclared write detection) | EM4 Filesystem Sandbox (Wave A/B restricted directories) | EM5 Event Log Audit (all writes logged with evidence).

5-stage detection: 1. Contract declares r/w → 2. Permission gate checks tier → 3. FS sandbox restricts paths → 4. Post-execution side effect audit → 5. Violation triggers EventStore alert + block.

## 4. Boundary

What IS write (forbidden Waves A/B): Modifying Z-MATRIX database/state, updating portfolio positions, broker orders, modifying config, registry mut at runtime, in-memory state mutation, trade signals externally, network connections to broker/trade APIs, non-approved fs paths, adapter contract modification at runtime.

What is NOT write (allowed Waves A/B): Report files to memory palace, EventStore logging, in-memory computation, reading any module, document output, returning results via AdapterResult.

## 5. Forbidden Actions

F-RO01 Wave A state mutation (CRITICAL) | F-RO02 Wave B state mutation (CRITICAL) | F-RO03 FS outside approved paths (HIGH) | F-RO04 Runtime config mod (HIGH) | F-RO05 Undeclared write (CRITICAL) | F-RO06 FS sandbox bypass (CRITICAL) | F-RO07 Trade signals Wave A/B (CRITICAL) | F-RO08 Registry mod non-T0 (CRITICAL) | F-RO09 Production DB writes (CRITICAL) | F-RO10 Side effect audit bypass (HIGH) | F-RO11 Broker API Wave A/B (CRITICAL) | F-RO12 Portfolio mutation Wave A/B (CRITICAL) | F-RO13 Network outside sandbox (CRITICAL) | F-RO14 Contract r/w mismatch (HIGH) | F-RO15 EventStore write missing evidence (MEDIUM) | F-RO16 FS write without EventStore log (HIGH) | F-RO17 Memory palace path violation (MEDIUM) | F-RO18 Production deploy Wave A/B (CRITICAL)

## 6. Proof / Requirements

R-RO01: 19 modules r/w classified | R-RO02: Wave A 0 state mutations | R-RO03: Wave B 0 state mutations | R-RO04: FS exception 4 conditions | R-RO05: 5 enforcement mechanisms | R-RO06: 5-stage detection | R-RO07: Write taxonomy 10 forbidden types | R-RO08: Forbidden >=18 | R-RO09: Read ops complete for A/B | R-RO10: Allowed write taxonomy 6 types

## 7. Next

INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md → TEST_AND_PROOF_PLAN.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-READONLY_POLICY_PLAN-v1.1
