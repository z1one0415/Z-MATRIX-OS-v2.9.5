---
title: "Z9 Review Node Implementation Planning — Overview"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
created: 2026-06-10
status: PLANNING_ACTIVE
version: v1.0.0
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Overview

## Section 1: Executive Summary

This document provides the top-level architectural overview for implementing the Z9 Review Node within the SkillOS capability invocation system. The Z9 Review Node is designed as a pure explanation-only review service that operates strictly in advisory/readonly mode, accepting input exclusively from Z2's `z9_review_snapshot_candidate` contract and producing 6 review labels with corresponding explanation evidence.

The primary dependency chain is: Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED → Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED → Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED → Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_MERGED_AND_SEALED. All bridge dependencies (B1, A1, Factor Library) are also merged and sealed on postmerge HEAD 1d61244.

## Section 2: Core Mission Statement

The Z9 Review Node exists to provide **explanation-only review** of Z2 research report node output. It does NOT generate trade signals, does NOT connect to any broker or execution pipeline, does NOT produce profit/PNL computations, and does NOT modify any system state. Its sole function is to classify a Z2 research snapshot into one of 6 review labels and produce structured explanation evidence.

## Section 3: Architectural Boundaries

### 3.1 Input Boundary
Z9 accepts input EXCLUSIVELY through `z9_review_snapshot_candidate` from Z2. The input contract specifies 15 required fields. Z9 does NOT accept input from B1 Composition Graph directly. Z9 does NOT accept FactorInvocationResponse. Z9 does NOT accept from research/factor_library paths. Any input arriving from non-Z2 sources MUST be rejected with REJECTED_UNSAFE_SOURCE.

### 3.2 Output Boundary
Z9 produces explanation review only. Six review labels are defined:
- EXPLANATION_ACCEPTED_STRUCTURE_ONLY
- EXPLANATION_ACCEPTED_WITH_MINOR_ISSUES
- EXPLANATION_ACCEPTED_SIGNIFICANT_ISSUES
- EXPLANATION_REJECTED_INSUFFICIENT_EVIDENCE
- EXPLANATION_REJECTED_CONTRADICTORY
- REJECTED_UNSAFE_SOURCE

No trade, broker, profit, or PNL outputs are permitted. The DENY_Z9_TRADE_RESULT_FORBIDDEN guard prohibits any trade-influencing computation.

### 3.3 State Mutation Boundary
Z9 is strictly readonly. DENY_Z9_MEMORY_MUTATION_FORBIDDEN prohibits any memory/knowledge graph mutations. DENY_Z9_TRADE_RESULT_FORBIDDEN prohibits any trade side-effect. All Z9 feedback to Z2 is advisory/readonly.

## Section 4: Dependency Landscape

### Primary Dependencies (all MERGED_AND_SEALED on postmerge HEAD 1d61244):
| # | Dependency | Status |
|---|-----------|--------|
| 1 | Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | PRIMARY |
| 2 | Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED | REQUIRED |
| 3 | Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED | INHERITED |
| 4 | Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_MERGED_AND_SEALED | REQUIRED |
| 5 | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | BRIDGE |
| 6 | A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | BRIDGE |
| 7 | FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | BRIDGE |

## Section 5: Evidence and Attribution Model

### 5.1 Evidence Chain
Z9 inherits 19 evidence fields from the Z2 snapshot. Z9 does NOT re-generate evidence. All evidence is passed through from the Z2 input contract. Evidence immutability is enforced — Z9 must not alter, reinterpret, or supplement any evidence field.

### 5.2 Attribution Model
Z9 supports 9 explanation-only attribution types. Profit attribution is explicitly blocked. Attribution is computed from evidence fields without market data access. Each review label maps to a structured attribution payload that explains WHY the label was assigned.

## Section 6: Degradation and Kill Switch

### 6.1 Degradation Decisions (10 total)
| # | Decision | Description |
|---|---------|-------------|
| 1 | ALLOW | Normal review operation |
| 2 | ALLOW_DEGRADED | Review with reduced evidence |
| 3 | ALLOW_CACHED | Return cached review |
| 4 | DEGRADE_TO_EXPLANATION_ONLY | Strip all non-core fields |
| 5 | DEGRADE_TO_LABEL_ONLY | Return label without explanation |
| 6 | DEGRADE_TO_UNSAFE_DEFAULT | Mark all as unsafe source |
| 7 | BLOCK_Z2_INPUT_MISMATCH | Reject mismatched input |
| 8 | BLOCK_EVIDENCE_TAMPERED | Reject when evidence chain broken |
| 9 | TRADE_RESULT_FORBIDDEN | Hard block on trade output |
| 10 | MEMORY_MUTATION_FORBIDDEN | Hard block on state mutation |

Decisions 9 and 10 are **blockers** that halt all processing.

### 6.2 Kill Switch Configuration
The Z9 review node is DISABLED_BY_DEFAULT. It MUST NOT activate without explicit kill_switch OFF and config enablement. Default state is NOOP — the node returns a DISABLED_DEFAULT_NOOP pass-through.

## Section 7: Future File Map (Reference Only — Do NOT Create)

The following files are anticipated for future implementation but are NOT created as part of this planning phase:

**Code files (skillos/capability_invocation_os/review_node/):**
- `__init__.py` — Package init with disabled-default guard
- `constants.py` — Review labels, degradation decisions, forbidden actions
- `config.py` — Kill switch configuration and runtime toggles
- `kill_switch.py` — DISABLED_DEFAULT_NOOP enforcement
- `models.py` — Pydantic models for review labels, evidence, attribution
- `contracts.py` — Input/output contract validation
- `evidence.py` — Evidence pass-through and immutability guard
- `attribution.py` — 9-type attribution computation
- `degradation.py` — 10-decision degradation framework
- `review_builder.py` — Review label assignment and explanation construction
- `z2_feedback.py` — Advisory/readonly Z2 feedback channel
- `registry.py` — SkillOS capability registration

**Test files (tests/skillos/capability_invocation_os/review_node/):**
- `test_disabled_default.py` — Verify DISABLED_DEFAULT_NOOP passthrough
- `test_models.py` — Model validation and serialization
- `test_contracts.py` — Contract validation boundary tests
- `test_evidence.py` — Evidence pass-through and immutability
- `test_attribution.py` — Attribution type coverage
- `test_degradation.py` — All 10 degradation paths
- `test_review_builder.py` — Review label classification
- `test_z2_feedback.py` — Feedback advisory/readonly enforcement
- `test_no_forbidden_imports.py` — Static import safety check

---

**Document Trail**: OVERVIEW → SCOPE → DEPENDENCY_MAP → FILE_LEVEL_PLAN → MODEL_CONTRACT → INPUT_CONTRACT → OUTPUT_CONTRACT → EVIDENCE_PLAN → ATTRIBUTION_PLAN → DEGRADATION_PLAN → Z2_FEEDBACK_PLAN → TEST_AND_PROOF_PLAN → CLOSEOUT → SEAL

**Review Trail**: REVIEW_GATE → REVIEW_CHECKLIST → REVIEW_RISK_REGISTER → REVIEW_DECISION_BRIEF → REVIEW_DECISION_RECORD → REVIEW_MERGE_READINESS → REVIEW_CLOSEOUT

**Merge Trail**: MERGE_REVIEW → MERGE_CHECKLIST → MERGE_RISK_REGISTER → MERGE_DECISION_BRIEF → MERGE_CLOSEOUT
