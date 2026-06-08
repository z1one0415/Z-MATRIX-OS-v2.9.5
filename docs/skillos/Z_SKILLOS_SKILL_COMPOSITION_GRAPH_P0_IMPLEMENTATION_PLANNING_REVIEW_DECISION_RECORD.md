# Z-SkillOS Skill Composition Graph P0 Implementation Planning — REVIEW DECISION RECORD

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft
> Minimum: ≥10 PENDING decisions

---

## 1. Purpose

This document records all review decisions made during the review of the Skill Composition Graph P0
Implementation Planning package. Each decision is tracked with its status, rationale, and resolution.
Minimum: 10 decisions with at least one in PENDING state.

## 2. Decision Record (≥10 Decisions)

### Decision RD-01: P0 Max Depth
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-01 |
| Topic | Maximum graph depth in P0 |
| Proposed | Max depth = 2 |
| Rationale | Two-node sequential chain is the absolute minimum to prove edge model and composition |
| Alternatives | Depth = 1 (too small, can't prove edges); Depth = 3 (too large for P0 safety) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | DAG-03 enforcement; all depth > 2 graphs rejected |

### Decision RD-02: Evidence Hash Algorithm
| Attribute | Value |
|-------|-------|
| Decision ID | RD-02 |
| Topic | Cryptographic hash for evidence chain |
| Proposed | SHA-256 |
| Rationale | Standard algorithm, collision-resistant, deterministic, widely available |
| Alternatives | SHA-512 (overkill for P0); MD5 (deprecated); BLAKE2 (less standard) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | All evidence hashes use SHA-256; test vectors in TEST_AND_PROOF_PLAN |

### Decision RD-03: DAG Validation Algorithm
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-03 |
| Topic | Algorithm for DAG cycle detection |
| Proposed | Kahn's algorithm (topological sort) |
| Rationale | Simple, proven, O(V+E), detects all cycle types, produces valid ordering |
| Alternatives | DFS-based (equivalent complexity); Tarjan's (overkill for P0) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | DAG_VALIDATOR_PLAN specifies Kahn's with pseudocode |

### Decision RD-04: Permission Propagation Model
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-04 |
| Topic | Permission propagation rule |
| Proposed | Monotonic non-increasing (downstream ≤ upstream) |
| Rationale | Prevents privilege escalation; standard security principle |
| Alternatives | Bidirectional (unsafe); per-field permissions (too complex for P0) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | PP-01 through PP-06 enforcement; escalation → FORBIDDEN |

### Decision RD-05: Degradation on Failure
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-05 |
| Topic | Behavior when node/edge validation fails |
| Proposed | Degrade to PLAN_ONLY or NOOP; never fail-closed |
| Rationale | Safety property: system must always produce a result, even if degraded |
| Alternatives | Fail-closed (blocks pipeline — rejected); retry (adds complexity — P1+) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | Degradation state machine in DEGRADATION_PLAN |

### Decision RD-06: Output Serialization Format
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-06 |
| Topic | Format for deterministic evidence hashing |
| Proposed | Canonical JSON with sorted keys, compact separators |
| Rationale | Ensures same logical data always produces same hash |
| Alternatives | Pickle (non-deterministic); msgpack (less standard); plain dict repr (ambiguous) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | EVIDENCE_PROPAGATION_PLAN §3 canonical JSON specification |

### Decision RD-07: Result Envelope Immutability
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-07 |
| Topic | Mutability of node outputs after completion |
| Proposed | Immutable after node completion |
| Rationale | Prevents evidence tampering; enables hash chain integrity |
| Alternatives | Mutable with audit log (more complex — P1+) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | OUTPUT_BOUNDARY_PLAN §5 immutability contract |

### Decision RD-08: P0 Tier Limitation
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-08 |
| Topic | Which permission tiers are allowed in P0 |
| Proposed | Tier 0 (readonly) and Tier 1 (planning) only |
| Rationale | P0 is plan-only; write/execute tiers add unacceptable risk |
| Alternatives | Include Tier 2 (research) — adds complexity without benefit for P0 scope |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | NC-04 enforcement; Tier 2-5 rejected |

### Decision RD-09: File Organization Structure
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-09 |
| Topic | Directory structure for composition module |
| Proposed | models/, validators/, policies/, degradation/, tests/ subpackages |
| Rationale | Clear separation of concerns; follows SkillOS conventions |
| Alternatives | Flat structure (too messy); nested by domain (over-engineered for P0) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | FILE_LEVEL_PLAN §2 directory structure |

### Decision RD-10: Persistence Strategy
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-10 |
| Topic | Storage of composition graphs and evidence |
| Proposed | No persistence in P0; ephemeral in-memory only |
| Rationale | P0 is plan-only; persistence adds infrastructure complexity |
| Alternatives | File-based (P1+); database (P2+); cloud storage (P3+) |
| Decision | APPROVED |
| Decided By | Planning phase design |
| Date | 2026-06-08 |
| Impact | All data is ephemeral; no storage layer in P0 |

### Decision RD-11: PENDING — Max Node Count for P0
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-11 |
| Topic | Whether max node count = 2 is sufficient to prove composition |
| Status | PENDING |
| Concern | Two-node chain proves edge model, but does it prove the graph model? |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-12: PENDING — Evidence Chain Coverage
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-12 |
| Topic | Whether SHA-256 hash chain covers all tampering vectors |
| Status | PENDING |
| Concern | Timestamp spoofing could produce identical hashes for different times |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-13: PENDING — Degradation Propagation Depth
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-13 |
| Topic | Whether degradation propagation algorithm handles multi-level degradation |
| Status | PENDING |
| Concern | With only 2 nodes, can't test cascading degradation; P1+ risk |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-14: PENDING — Field Governance Wildcards
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-14 |
| Topic | Whether allow-list wildcards (e.g., "*") should be supported in P0 |
| Status | PENDING |
| Concern | "*" wildcard bypasses field governance; security risk |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-15: PENDING — Rollback Marker Scope
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-15 |
| Topic | Whether rollback marker should include full affected-node list or just flag |
| Status | PENDING |
| Concern | Flag-only may lose information about which nodes were affected |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-16: PENDING — Output Truncation Size
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-16 |
| Topic | Whether 1MB evidence truncation limit is appropriate for P0 |
| Status | PENDING |
| Concern | 1MB is arbitrary; should be configurable or removed for P0 (no real execution) |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-17: PENDING — Test Vector Completeness
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-17 |
| Topic | Whether test vectors in TEST_AND_PROOF_PLAN cover all critical paths |
| Status | PENDING |
| Concern | Some proof categories lack explicit test vectors (Cat 9, 10, 11) |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-18: PENDING — Immutability Enforcement Mechanism
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-18 |
| Topic | Whether frozen flag is sufficient for immutability enforcement |
| Status | PENDING |
| Concern | Python doesn't natively support object freezing; relies on convention |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-19: PENDING — Error Taxonomy Completeness
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-19 |
| Topic | Whether error taxonomy in DAG_VALIDATOR_PLAN covers all failure modes |
| Status | PENDING |
| Concern | Some DAG invariants (DAG-01, DAG-04, DAG-08) lack explicit error classes |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

### Decision RD-20: PENDING — Cross-Branch Consistency
| Attribute | Value |
|-----------|-------|
| Decision ID | RD-20 |
| Topic | Whether this branch is consistent with parent P0 Planning branch |
| Status | PENDING |
| Concern | Need to verify no contradictions between planning and implementation planning docs |
| Reviewer | PENDING ASSIGNMENT |
| Date | 2026-06-08 |
| Expected Resolution | During review execution |

## 3. Decision Summary

| Status | Count | Decision IDs |
|--------|:---:|------|
| APPROVED | 10 | RD-01 through RD-10 |
| PENDING | 10 | RD-11 through RD-20 |
| REJECTED | 0 | — |
| DEFERRED | 0 | — |
| **Total** | **20 decisions** | ✅ ≥ 10 PENDING |

## 4. Decision Impact Matrix

| Decision | Affects | Critical Path |
|----------|---------|:---:|
| RD-01 | DAG_VALIDATOR_PLAN, LOOP_PREVENTION_PLAN | ✅ |
| RD-02 | EVIDENCE_PROPAGATION_PLAN | ✅ |
| RD-03 | DAG_VALIDATOR_PLAN | ✅ |
| RD-04 | PERMISSION_PROPAGATION_PLAN | ✅ |
| RD-05 | DEGRADATION_PLAN | ✅ |
| RD-06 | EVIDENCE_PROPAGATION_PLAN | ✅ |
| RD-07 | OUTPUT_BOUNDARY_PLAN, NODE_MODEL_PLAN | ✅ |
| RD-08 | NODE_MODEL_PLAN, PERMISSION_PROPAGATION_PLAN | ✅ |
| RD-09 | FILE_LEVEL_PLAN | ✅ |
| RD-10 | All (persistence design) | — |
| RD-11 | OVERVIEW, SCOPE, DAG_VALIDATOR_PLAN | — |
| RD-12 | EVIDENCE_PROPAGATION_PLAN | — |
| RD-13 | DEGRADATION_PLAN | — |
| RD-14 | EDGE_MODEL_PLAN, OUTPUT_BOUNDARY_PLAN | — |
| RD-15 | DEGRADATION_PLAN, EVIDENCE_PROPAGATION_PLAN | — |
| RD-16 | OUTPUT_BOUNDARY_PLAN | — |
| RD-17 | TEST_AND_PROOF_PLAN | — |
| RD-18 | NODE_MODEL_PLAN, OUTPUT_BOUNDARY_PLAN | — |
| RD-19 | DAG_VALIDATOR_PLAN | — |
| RD-20 | All | ✅ |

## 5. PENDING Resolution Plan

All 10 PENDING decisions require reviewer input. Resolution is expected during review
execution. Any PENDING decision unresolved at REVIEW_CLOSEOUT will be escalated to
MERGE_DECISION_BRIEF for final determination.

## 6. Decision Governance

- All decisions are recorded in this document
- APPROVED decisions are binding for P0 scope
- PENDING decisions must be resolved before MERGE_CLOSEOUT
- REJECTED decisions must include rationale and alternative
- Decision changes after REVIEW_CLOSEOUT require MERGE_DECISION_BRIEF amendment

## 7. Review Decision Record Seal

This record is maintained throughout the review phase. At REVIEW_CLOSEOUT:
- All PENDING decisions are resolved (APPROVED, REJECTED, or DEFERRED)
- Final decision count is tallied
- Residual decisions are escalated to merge phase
