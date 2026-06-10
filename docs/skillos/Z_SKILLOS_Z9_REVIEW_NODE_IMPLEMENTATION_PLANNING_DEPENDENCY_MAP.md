---
title: "Z9 Review Node Implementation Planning — Dependency Map"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Dependency Map

## Section 1: Dependency Graph Overview

The Z9 Review Node sits downstream of the Z2 Research Report Node in the SkillOS capability invocation pipeline. It does NOT receive input from the Factor Library, B1 Composition Graph, A1 Bridge, or any other upstream node. Its sole input source is Z2's `z9_review_snapshot_candidate` contract.

```
A1_FACTOR_LIBRARY_BRIDGE ─┐
B1_COMPOSITION_GRAPH ─────┤
FACTOR_LIBRARY_ADAPTER ──┤   (NOT consumed by Z9)
                           │
Z2_RESEARCH_REPORT_NODE ───┼──→ z9_review_snapshot_candidate ──→ Z9_REVIEW_NODE
                           │         (15 input fields)              │
                           │                                        ↓
                           │                            explanation-only review
                           │                            (6 review labels)
                           │                                        │
                           │                                        ↓
                           │                              Z2_FEEDBACK (advisory)
                           │                              (10 allowed fields)
```

## Section 2: Primary Dependencies (ALL MERGED_AND_SEALED)

### 2.1 Tier 1 — Critical Path Dependencies

| # | Artifact | Role | Merge Status |
|---|---------|------|:---:|
| D1 | Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | Defines DISABLED_DEFAULT contract for Z2 node; Z9 inherits same disabled-default pattern | MERGED |
| D2 | Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED | Defines Z2 planning contracts including z9_review_snapshot_candidate shape | MERGED |
| D3 | Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED | Defines Z9 planning foundation: 6 review labels, degradation decisions, evidence model | MERGED |
| D4 | Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_MERGED_AND_SEALED | Defines Z2 implementation contracts that Z9 input validation references | MERGED |

### 2.2 Tier 2 — Bridge Dependencies (Context Only)

| # | Artifact | Role | Z9 Consumption | Merge Status |
|---|---------|------|:---:|:---:|
| D5 | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | Graph composition bridge | NOT CONSUMED | MERGED |
| D6 | A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | Factor library bridge | NOT CONSUMED | MERGED |
| D7 | FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | Factor library adapter | NOT CONSUMED | MERGED |

## Section 3: Dependency Contract Inheritance

### 3.1 From Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED (D2)
Z9 inherits the following contracts:
- z9_review_snapshot_candidate: 15-field input contract definition
- Evidence chain structure: 19-field evidence pass-through specification
- Z2 feedback channel: advisory/readonly channel definition with 10 allowed fields
- Report schema reference: Z2 output schema that Z9 reviews

### 3.2 From Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED (D3)
Z9 inherits the following contracts:
- 6 review label definitions (EXPLANATION_ACCEPTED_STRUCTURE_ONLY through REJECTED_UNSAFE_SOURCE)
- 10 degradation decision definitions (ALLOW through MEMORY_MUTATION_FORBIDDEN)
- 9 attribution type definitions
- Evidence immutability requirements
- DISABLED_DEFAULT_NOOP specification

### 3.3 From Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN (D1)
Z9 inherits:
- DISABLED_BY_DEFAULT pattern
- Kill switch architecture
- NOOP pass-through model
- Input source validation framework

## Section 4: Dependency Verification Matrix

| Check ID | Dependency | Verification Method | Pass/Fail |
|----------|-----------|-------------------|:---:|
| V-D1 | D1: Z2 disabled-default contract exists | File presence at docs/skillos/ | PASS |
| V-D2 | D2: z9_review_snapshot_candidate defined | Contract field audit | PASS |
| V-D3 | D3: 6 review labels defined | Label enumeration check | PASS |
| V-D4 | D4: Z2 implementation contracts exist | File presence audit | PASS |
| V-D5 | D5: B1 bridge merged | Branch merge status check | PASS |
| V-D6 | D6: A1 bridge merged | Branch merge status check | PASS |
| V-D7 | D7: Factor adapter merged | Branch merge status check | PASS |
| V-BASE | Base commit matches 1d61244 | git rev-parse HEAD | PASS |

## Section 5: Forbidden Dependency Paths

Z9 MUST NOT depend on any of the following paths. These are actively blocked:

| # | Forbidden Path | Block Reason | Enforcement |
|---|---------------|-------------|-------------|
| F1 | B1 Composition Graph → Z9 direct | Z9 only accepts Z2 input | Input source validation |
| F2 | A1 Factor Library Bridge → Z9 direct | Factor data not review-relevant | Input contract rejection |
| F3 | FactorInvocationResponse → Z9 | Wrong data shape/concept | Type validation failure |
| F4 | research/factor_library → Z9 | No direct research data access | Path isolation |
| F5 | trade/broker → Z9 | DENY_Z9_TRADE_RESULT_FORBIDDEN | Hard block |
| F6 | memory/knowledge_graph → Z9 (write) | DENY_Z9_MEMORY_MUTATION_FORBIDDEN | Hard block |
| F7 | market_data → Z9 direct | No market data access needed | Architecture isolation |
| F8 | profit/PNL → Z9 | Profit attribution blocked | Attribution model block |

## Section 6: Dependency Impact Analysis

### 6.1 If D2 Changes (z9_review_snapshot_candidate shape)
- Z9 INPUT_CONTRACT must be updated
- All contract validation tests must be re-run
- Evidence pass-through mapping must be re-verified

### 6.2 If D3 Changes (review labels or degradation model)
- REVIEW_CONTRACT must be updated
- Attribution mapping must be re-verified
- Degradation decision tree must be re-computed

### 6.3 If D1/D4 Changes (disabled-default or Z2 implementation)
- Kill switch configuration may need update
- DISABLED_DEFAULT_NOOP behavior must be re-verified
- Integration test suite must be re-run

## Section 7: Dependency Lifecycle

### 7.1 Current State (2026-06-10)
All 7 dependencies are MERGED_AND_SEALED on postmerge HEAD 1d61244. No pending dependency changes. No dependency drift detected. All verification checks pass (PASS).

### 7.2 Monitoring Requirements
- Track Z2_RESEARCH_REPORT_NODE for contract changes
- Track Z9_REVIEW_NODE_PLANNING for spec updates
- Monitor all bridge dependencies for breaking changes
- Verify input contract compatibility on each Z2 release

### 7.3 Dependency Update Protocol
1. Detect dependency change (commit monitor or manual notification)
2. Run dependency verification matrix (V-D1 through V-D7)
3. Update affected contracts if shape changes
4. Re-run full test suite
5. Update this dependency map
6. Re-seal with updated version

---

**Cross-Reference**: See OVERVIEW for architectural context, INPUT_CONTRACT for Z9 input specification, OUTPUT_CONTRACT for Z9 output specification.
