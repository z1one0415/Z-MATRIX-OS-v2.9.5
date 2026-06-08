# Z-SkillOS Skill Composition Graph P0 Implementation Planning — OVERVIEW

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft
> Generated: 2026-06-08

---

## 1. Purpose

This document is the executive overview for the SkillOS Skill Composition Graph P0 Implementation
Planning package. This package translates the P0 Planning designs (from the companion planning branch)
into concrete implementation specifications: file-level structure, node/edge models with full schema,
DAG validator with cycle detection, permission and evidence propagation contracts, degradation
strategies, loop prevention enforcement, output boundary controls, and comprehensive test/proof plans.

## 2. Relationship to P0 Planning Package

| Dimension | P0 Planning Package | P0 Implementation Planning Package |
|-----------|--------------------|------------------------------------|
| Branch | plan/skillos-skill-composition-graph-p0-planning | plan/skillos-skill-composition-graph-p0-implementation-planning |
| Purpose | Conceptual design, contracts, policies | Concrete implementation specs, file layout, schema |
| Level | Architecture + Policy | Implementation-ready specification |
| Deliverables | 30 docs (planning, review, merge) | 26 docs (planning, review, merge) |
| Evidence | Policy-level hash models | Implementation-level hash functions + test vectors |

## 3. P0 Implementation Scope Boundary

| Dimension | P0 Implementation Scope | Out of Scope |
|-----------|------------------------|--------------|
| Graph topology | Single-node dry plan, two-node sequential plan | >2 nodes, branching, fan-out, merge |
| Execution | Dry plan generation only (no-op output) | Real capability execution |
| Node types | Read-only analysis nodes (Tier 0-1) | Write, production, broker, real_trade |
| Depth | Max depth = 2 | Depth > 2, recursive composition |
| Cycles | Strictly forbidden; Kahn's algorithm at build time | Dynamic cycles, feedback loops |
| Persistence | None (ephemeral in-memory) | Database, file, stateful storage |
| Evidence | Ephemeral hash chain (SHA-256) | Audit log, persistent evidence store |
| Runtime | Plan validation only | Execution engine, scheduler, dispatcher |
| Permissions | Monotonic non-increasing; escalation forbidden | Auto-escalation, dynamic tier adjustment |
| Degradation | Noop or plan-only; no fail-closed | Dynamic recovery, retry logic, circuit breaker |

## 4. Implementation Principles

1. **Contract-First Implementation**: Every data structure is defined by a contract before any code.
2. **Compile-Time Safety**: All validation (DAG, permissions, evidence, loops) runs at graph build time.
3. **Immutable Data Structures**: Node results, edge outputs, and graph decisions are immutable post-build.
4. **No Hidden Tooling**: No node can invoke hidden tools, dynamic agent loops, or unregistered capability paths.
5. **Fail-By-Degradation**: Failure degrades to noop or plan-only; never blocks the pipeline.
6. **Deterministic Hashing**: All evidence hashes use fixed input ordering and canonical JSON serialization.
7. **Z-MATRIX Non-Integration**: This package does not integrate with Z-MATRIX; it is standalone SkillOS infrastructure.

## 5. Document Package Structure

### Planning Layer (14 docs)
| # | Document | Purpose | Min Lines |
|---|----------|---------|-----------|
| 1 | OVERVIEW | Executive summary (this document) | 30 |
| 2 | SCOPE | Precise P0 scope boundary with in/out tables | 30 |
| 3 | FILE_LEVEL_PLAN | File tree, module structure, import hierarchy | 30 |
| 4 | NODE_MODEL_PLAN | Node data model, contract schema, validation rules | 30 |
| 5 | EDGE_MODEL_PLAN | Edge data model, contract schema, field governance | 30 |
| 6 | DAG_VALIDATOR_PLAN | Static DAG validation, cycle detection, topology | 30 |
| 7 | PERMISSION_PROPAGATION_PLAN | Permission tier model, propagation enforcement | 30 |
| 8 | EVIDENCE_PROPAGATION_PLAN | Hash chain design, deterministic evidence | 30 |
| 9 | DEGRADATION_PLAN | Failure modes, degradation states, markers | 30 |
| 10 | LOOP_PREVENTION_PLAN | Cycle detection, depth limits, recursion guards | 30 |
| 11 | OUTPUT_BOUNDARY_PLAN | Output schema enforcement, forbidden field blocking | 30 |
| 12 | TEST_AND_PROOF_PLAN | ≥18 proof categories with strategies | 30 |
| 13 | PLANNING_CLOSEOUT | Planning completeness checklist | 30 |
| 14 | PLANNING_SEAL | Immutable seal of planning phase | 30 |

### Review Layer (7 docs)
| # | Document | Purpose | Min Lines |
|---|----------|---------|-----------|
| 15 | REVIEW_GATE | Review entry conditions and gate criteria | 35 |
| 16 | REVIEW_CHECKLIST | ≥18 line-item review checklist | 35 |
| 17 | REVIEW_RISK_REGISTER | ≥12 risks with severity, likelihood, mitigations | 35 |
| 18 | REVIEW_DECISION_BRIEF | Summary brief for reviewer decision | 35 |
| 19 | REVIEW_DECISION_RECORD | Record of all review decisions (≥10 PENDING) | 35 |
| 20 | REVIEW_MERGE_READINESS | Assessment of merge readiness | 35 |
| 21 | REVIEW_CLOSEOUT | Review phase closure documentation | 35 |

### Merge Layer (5 docs)
| # | Document | Purpose | Min Lines |
|---|----------|---------|-----------|
| 22 | MERGE_REVIEW | Pre-merge review of all artifacts | 30 |
| 23 | MERGE_CHECKLIST | ≥15 line-item merge checklist | 30 |
| 24 | MERGE_RISK_REGISTER | ≥10 merge-specific risks | 30 |
| 25 | MERGE_DECISION_BRIEF | Summary brief for merge decision | 30 |
| 26 | MERGE_CLOSEOUT | Merge phase closure documentation | 30 |

## 6. Future Implementation Path

All code files will reside at:
```
skillos/capability_invocation_os/composition/
├── __init__.py
├── models/
│   ├── node.py            # CompositionNode model
│   ├── edge.py            # CompositionEdge model
│   └── graph.py           # CompositionGraph model
├── validators/
│   ├── dag_validator.py   # DAG structure + cycle detection
│   ├── permission_validator.py
│   └── evidence_validator.py
├── policies/
│   ├── permission_propagation.py
│   ├── evidence_propagation.py
│   ├── loop_prevention.py
│   └── output_boundary.py
├── degradation/
│   └── degradation_controller.py
└── tests/
    └── test_composition_graph.py
```

No code is written in P0. These paths serve as implementation targets for P1+.

## 7. Governance

- **Level 5 BLOCKED**: No implementation, no execution, no Z-MATRIX integration.
- **FUTURE_PLAN_ONLY**: All documents are forward-looking specifications.
- **Immutable After Seal**: The PLANNING_SEAL document finalizes this package as a sealed artifact.
- **Review Required**: All 7 review documents must be completed before merge consideration.
- **Merge Gate**: All 5 merge documents must pass before branch approval.
