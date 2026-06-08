# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — MODULE_PRIORITY_PLAN

> Status: _MODULE_PRIORITY_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Modules: 19 ranked
Hardened: 2026-06-08

## 2. Scope

Priority ranking for implementation (FUTURE ONLY, not authorized now):

Wave A (P1-P7): 1. CAP-REG-001 (T0, FIRST), 2. CAP-MEM-001 (T1), 3. CAP-GAT-001 (T1), 4. CAP-RPT-001 (T1), 5. CAP-EVT-001 (T2), 6. CAP-RPT-002 (T2), 7. CAP-DOC-001 (T2).

Wave B (P8-P15): 8. CAP-CHN-001 (T3), 9. CAP-BMX-001 (T3), 10. CAP-DMX-001 (T3), 11. CAP-RMX-001 (T3), 12. CAP-SCR-001 (T3), 13. CAP-SIM-001 (T3), 14. CAP-EXE-001 (T4), 15. CAP-FLO-001 (T4).

Wave C (P16-P19, FUTURE ONLY): 16. CAP-PRT-001, 17. CAP-BRK-001, 18. CAP-TRD-001, 19. CAP-DEP-001.

Dependency ordering rules: Rule 1: No adapter before dependencies. Rule 2: CAP-REG-001 MUST be priority 1. Rule 3: Wave B cannot start until Wave A 1-5 complete. Rule 4: Wave C NEVER from this package. Rule 5: Same-tier independent adapters by lower risk first.

Critical path: CAP-REG-001 → CAP-MEM-001 → CAP-CHN-001 → CAP-BMX-001 → CAP-SCR-001 → CAP-EXE-001 → CAP-FLO-001 (7 nodes). Parallel: CAP-RPT-001, CAP-GAT-001 parallel to CAP-MEM-001. Matrix scans (BMX, DMX, RMX) in parallel.

## 3. Evidence / Dependency

Priority reassessment triggers: Upstream WAVE0 changes, Z-MATRIX v2.9.5 API changes, new capability registration requirements, cross-wave dependency discovery.

## 4. Boundary

Priority scope: Implementation order specification only. No execution planning, no schedule, no resource allocation. Out: Implementation start, sprint planning, developer assignment, timeline, infrastructure.

Wave C: FUTURE ONLY. Zero specification. No priority refinement. Level 5 BLOCKED.

## 5. Forbidden Actions

F-MP01 Out of priority order implementation (HIGH) | F-MP02 Skipping dependency (CRITICAL) | F-MP03 Wave C implementation from this plan (CRITICAL) | F-MP04 Changing priorities without re-evaluation (HIGH) | F-MP05 Parallel dependent modules (MEDIUM) | F-MP06 Priority reassign without contract review (MEDIUM) | F-MP07 Bypass CAP-REG-001 first (CRITICAL) | F-MP08 Wave B before Wave A (HIGH) | F-MP09 Ignoring dependency graph (CRITICAL) | F-MP10 Priority modified without version bump (MEDIUM) | F-MP11 Implied implementation start date (MEDIUM) | F-MP12 Resource allocation from this plan (MEDIUM) | F-MP13 Priority as execution authorization (CRITICAL) | F-MP14 T5-T7 claiming priority refinement (MEDIUM) | F-MP15 Adapter claiming ready with missing dependency (CRITICAL) | F-MP16 Same-wave parallel with dependency (MEDIUM) | F-MP17 Priority as readiness report (HIGH) | F-MP18 Priority claiming to authorize implementation (CRITICAL)

## 6. Proof / Requirements

R-MP01: 19 modules with priority | R-MP02: Wave A P1-P7 | R-MP03: Wave B P8-P15 | R-MP04: Wave C P16-P19 future | R-MP05: CAP-REG-001 priority 1 | R-MP06: Critical path 7 nodes | R-MP07: Parallel groups identified | R-MP08: 5 ordering rules | R-MP09: Forbidden >=18 | R-MP10: FUTURE_PLAN_ONLY stated

## 7. Next

FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-MODULE_PRIORITY_PLAN-v1.1
