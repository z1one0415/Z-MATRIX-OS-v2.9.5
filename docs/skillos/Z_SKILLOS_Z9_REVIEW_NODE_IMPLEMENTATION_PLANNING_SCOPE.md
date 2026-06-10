---
title: "Z9 Review Node Implementation Planning — Scope"
pipeline: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING
branch: plan/skillos-z9-review-node-implementation-planning
base_commit: 1d61244
SEAL: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_SEALED
CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_READY_FOR_REVIEW
REVIEW_DECISION_RECORD: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_REVIEW_DECISION_PENDING
MERGE_CLOSEOUT: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
---

# Z9 Review Node Implementation Planning — Scope

## Section 1: In-Scope Deliverables

### 1.1 Core Review Engine
The Z9 Review Node implementation shall deliver a complete explanation-only review engine capable of:
- Accepting Z2 `z9_review_snapshot_candidate` input (15 fields)
- Validating input contract compliance (source check, field presence, evidence chain integrity)
- Classifying input into exactly one of 6 review labels
- Producing structured explanation evidence for each classification
- Enforcing readonly/advisory mode with zero side effects
- Providing Z2 feedback through the approved advisory channel (10 allowed fields)

### 1.2 Contract Enforcement
- INPUT_CONTRACT: Strict validation of z9_review_snapshot_candidate shape
- OUTPUT_CONTRACT: 6-label review output with structured explanation
- EVIDENCE contract: 19-field pass-through with immutability guard
- ATTRIBUTION contract: 9 explanation-only types, profit attribution blocked
- DEGRADATION contract: 10-decision degradation with 2 hard blockers
- Z2_FEEDBACK contract: 10 allowed fields, 8 forbidden (no auto-patch/auto-update)

### 1.3 Safety Boundaries
- DISABLED_BY_DEFAULT: Node must NOOP when kill_switch is ON (default)
- DENY_Z9_TRADE_RESULT_FORBIDDEN: Hard block on any trade/computation
- DENY_Z9_MEMORY_MUTATION_FORBIDDEN: Hard block on any state mutation
- Readonly enforcement: No filesystem writes, no network calls, no DB mutations
- Input source validation: Reject non-Z2 sources with REJECTED_UNSAFE_SOURCE

### 1.4 Test Coverage
- Unit tests for all 12 planned code modules
- Contract validation tests for all 6 contracts
- Degradation path tests covering all 10 decisions
- Evidence immutability tests
- Attribution boundary tests
- Z2 feedback advisory enforcement tests
- DISABLED_DEFAULT_NOOP integration tests
- Forbidden imports static analysis

## Section 2: Explicitly Out-of-Scope

### 2.1 Trade/Execution Concerns
- NO trade signal generation
- NO broker integration
- NO profit/PNL computation
- NO position sizing
- NO order management
- NO execution routing
- NO portfolio optimization

### 2.2 State Mutation
- NO memory/knowledge-graph writes
- NO file writes outside audit trail
- NO database mutations
- NO configuration changes
- NO environment variable modifications
- NO side-effect of any form

### 2.3 Direct Integration Paths (BLOCKED)
- NO direct B1 Composition Graph input
- NO direct FactorInvocationResponse input
- NO direct research/factor_library input
- NO direct external API calls
- NO direct market data access

### 2.4 Feedback Actions
- NO auto-patching of Z2 output
- NO auto-updating of Z2 models
- NO feedback loop with execution engine
- NO automatic parameter tuning
- NO closed-loop optimization

## Section 3: Dependency Scope

### 3.1 Primary Dependencies (All MERGED_AND_SEALED)
The implementation depends on the following already-merged planning artifacts at postmerge HEAD 1d61244:
1. Z2_RESEARCH_REPORT_NODE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
2. Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED
3. Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED
4. Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_MERGED_AND_SEALED
5. B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
6. A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
7. FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED

### 3.2 Bridge Dependencies (FOR REFERENCE)
The following bridge dependencies provide context but are NOT directly called by Z9:
- A1 Factor Library Bridge (provides FactorInvocationResponse — NOT consumed by Z9)
- B1 Composition Graph Bridge (provides graph composition — NOT consumed by Z9)
- Factor Library Readonly Adapter (provides factor data — NOT consumed by Z9)

### 3.3 External Dependencies
- Python 3.11+
- Pydantic v2 (data validation)
- pytest (test framework)
- SkillOS capability registry (node registration)

## Section 4: Deliverable Boundaries

### 4.1 Planning Phase (This Branch)
All 26 documentation files under docs/skillos/ with prefix Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_PLANNING_. NO CODE FILES ARE CREATED IN THIS PHASE.

### 4.2 Implementation Phase (Future Branch)
- 12 Python modules under skillos/capability_invocation_os/review_node/
- 9 test modules under tests/skillos/capability_invocation_os/review_node/
- Integration and deployment configuration

### 4.3 Review Phase (Future Gate)
- Review gate approval
- Review checklist completion
- Risk register review
- Decision record finalization

### 4.4 Merge Phase (Future Gate)
- Merge readiness check
- Merge checklist completion
- Human decision finalization
- Post-merge seal

## Section 5: Quality Gates

### 5.1 Planning Gate (Current)
- All 26 docs created with ≥minimum line counts
- All 7-section structures complete
- All status markers in place
- All key content references included
- All dependency references correct

### 5.2 Review Gate
- Review Checklist ≥38 checks
- Review Risk Register ≥24 risks (each: severity/likelihood/mitigation/control/rollback trigger)
- Review Decision Record PENDING with 21+ pending fields

### 5.3 Merge Gate
- Merge Checklist ≥32 checks
- Merge Risk Register ≥20 risks
- Test & Proof Plan ≥48 proof categories

## Section 6: Risk Constraints

### 6.1 Architectural Risks
- Input source validation bypass could allow non-Z2 input to reach Z9
- Evidence immutability breach could corrupt review integrity
- Attribution model leakage could expose trade-sensitive computation
- Degradation misconfiguration could disable safety blocks

### 6.2 Implementation Risks
- DISABLED_DEFAULT bypass would expose review node prematurely
- Memory mutation could corrupt investment knowledge graph
- Trade result leakage could influence downstream execution

### 6.3 Integration Risks
- Z2 contract drift could invalidate input shape
- SkillOS registry misregistration could expose wrong capabilities
- Kill switch misconfiguration could leave node permanently disabled or enabled

## Section 7: Approval Requirements

### 7.1 Planning Approval
- All 26 docs verified for line count minimums
- All status markers verified
- All dependency references cross-checked against postmerge HEAD 1d61244
- Planning CLOSEOUT signed
- Planning SEAL affixed

### 7.2 Future Approvals
- Review gate approval (separate ceremony)
- Review decision record finalized (separate ceremony)
- Merge approval (human decision required)
- Post-merge seal (separate ceremony)
