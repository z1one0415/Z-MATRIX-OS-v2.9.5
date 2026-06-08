# Z-SkillOS Skill Composition Graph P0 Planning — OVERVIEW

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning
> Pipeline: Lane B — Skill Composition Graph P0
> Version: v1.0.0-draft
> Generated: 2026-06-08

---

## 1. Purpose

This document is the executive overview for the SkillOS Skill Composition Graph P0 Planning package.
The Skill Composition Graph is the central orchestration model for SkillOS: a static, compile-time-validated
directed acyclic graph (DAG) of capability nodes connected by contract-governed edges. P0 establishes
the foundational design with the absolute minimum of capability: single-node dry plans and two-node
sequential plans only. No real execution. No cycles. No dynamic recursion.

## 2. Problem Statement

SkillOS requires a structured, auditable mechanism for composing individual skill capabilities into
multi-step plans. Without a composition graph, capability invocation is ad-hoc, unverifiable, and unsafe.
The composition graph provides:

- **Static DAG topology**: all nodes and edges known at plan-graph-build time
- **Contract enforcement**: every node has a capability id, module adapter id, permission tier, input/output schema
- **Edge governance**: data fields must be explicitly allowed; forbidden fields rejected
- **Permission propagation**: downstream nodes cannot exceed upstream tier; escalation forbidden
- **Evidence propagation**: cryptographic hashes for node outputs, edge handoffs, and graph decisions
- **Failure degradation**: degrade to noop or plan-only; no fail-closed; no blocking
- **Loop prevention**: no self-edges, no circular dependencies, max depth enforced

## 3. P0 Scope Boundary

| Dimension | P0 Scope | Out of Scope |
|-----------|----------|--------------|
| Graph topology | Single-node dry plan, two-node sequential plan | >2 nodes, branching, fan-out, merge |
| Execution | Dry plan generation only (no-op output) | Real capability execution |
| Node types | Read-only analysis nodes (Tier 0-1) | Write, production, broker, real_trade |
| Depth | Max depth = 2 | Depth > 2, recursive composition |
| Cycles | Strictly forbidden | Dynamic cycles, feedback loops |
| Persistence | None (ephemeral in-memory) | Database, file, stateful storage |
| Persistence of evidence | None (ephemeral hash chain) | Audit log, persistent evidence store |
| Runtime | Plan validation only | Execution engine, scheduler, dispatcher |

## 4. Architecture Principles

1. **Compile-Time Validation**: The entire graph must be validatable before any node processes data.
2. **Contract-First Design**: Nodes and edges are defined by contracts; no ad-hoc capability wiring.
3. **Failure-By-Degradation**: When a node fails, the graph degrades (to noop or plan-only), never fails-closed.
4. **No Hidden Execution**: All execution paths are explicit in the static DAG. No implicit tool calls, no hidden agent loops.
5. **Permission Monotonicity**: Permission tier can only decrease or stay equal downstream; never increase.
6. **Evidence Chain Integrity**: Every node and edge produces a hash; graph decisions are hash-linked; tampering is detectable.

## 5. Document Package Structure

### Planning Layer (14 docs)
| Document | Purpose |
|----------|---------|
| OVERVIEW.md | Executive summary (this document) |
| SCOPE.md | Detailed scope definition and boundary enumeration |
| NODE_CONTRACT_PLAN.md | Node capability id, adapter, permission tier, I/O schema, degradation |
| EDGE_CONTRACT_PLAN.md | Upstream/downstream ids, allowed/forbidden fields, evidence handoff |
| DAG_POLICY_PLAN.md | P0 topology rules: max 2 nodes, sequential only, no cycles |
| PERMISSION_PROPAGATION_PLAN.md | Downstream ≤ upstream rule; forbidden on boundary violation |
| EVIDENCE_PROPAGATION_PLAN.md | Node hash, edge hash, decision hash, rollback marker; no persistence |
| FAILURE_DEGRADATION_PLAN.md | Degrade to noop/plan-only, partial invalidation; no fail-closed |
| LOOP_PREVENTION_PLAN.md | Static DAG only, max depth, no self-edge, no circular, no tool recursion |
| OUTPUT_BOUNDARY_PLAN.md | No result_envelope mutation, internal proof only, no user-visible side effect |
| TEST_AND_PROOF_PLAN.md | ≥18 proof categories covering contracts, edges, permissions, degradation |
| FORBIDDEN_ACTIONS_MATRIX.md | ≥18 forbidden actions with category, severity, detection mechanism |
| PLANNING_CLOSEOUT.md | Planning readiness assessment; _PLANNING_READY_FOR_REVIEW seal |
| PLANNING_SEAL.md | Cryptographic planning seal; _PLANNING_SEALED signature |

### Review Layer (7 docs)
| Document | Purpose |
|----------|---------|
| REVIEW_GATE.md | Entry gate for review phase; prerequisites and blockers |
| REVIEW_CHECKLIST.md | ≥18 review checks covering all contracts and policies |
| REVIEW_RISK_REGISTER.md | ≥12 risks with severity/likelihood/mitigation/control/rollback |
| REVIEW_DECISION_BRIEF.md | Summary brief for review decision |
| REVIEW_DECISION_RECORD.md | 10 PENDING fields; status: _REVIEW_DECISION_PENDING |
| REVIEW_MERGE_READINESS.md | Assessment of whether planning is ready for merge |
| REVIEW_CLOSEOUT.md | Review phase closeout with sign-off |

### Merge Layer (5 docs)
| Document | Purpose |
|----------|---------|
| MERGE_REVIEW.md | Final merge review gate |
| MERGE_CHECKLIST.md | ≥15 merge checks |
| MERGE_RISK_REGISTER.md | ≥10 merge risks |
| MERGE_DECISION_BRIEF.md | Merge decision summary |
| MERGE_CLOSEOUT.md | _MERGE_REVIEW_READY_FOR_HUMAN_DECISION |

## 6. Key Invariants

1. **FUTURE_PLAN_ONLY**: No code ships. No implementation touches Z-MATRIX.
2. **Level 5 BLOCKED**: All execution paths gated behind Level 5 approval.
3. **No Real Execution**: P0 produces plan structures only; no capability is actually invoked.
4. **Static Topology**: DAG is a compile-time artifact; no runtime graph mutation.
5. **No Persistence**: All evidence hashes are in-memory; no file or database side effects.
6. **No User-Visible Side Effects**: Output boundary prevents mutation of result_envelope.

## 7. Dependencies

- **Upstream**: SkillOS Capability Invocation OS (Level 4 gates passed)
- **Downstream**: P1 Composition Graph (multi-node branching, fan-out)
- **Blocked By**: None at docs-only level
- **Blocks**: P1 implementation planning

## 8. Acceptance Criteria

- [ ] All 14 planning docs meet depth standards (≥30 lines each)
- [ ] All 7 review docs meet depth standards (≥35 lines each)
- [ ] All 5 merge docs meet depth standards (≥30 lines each)
- [ ] Review Risk Register: ≥12 risks with full mitigation detail
- [ ] Merge Risk Register: ≥10 risks with full mitigation detail
- [ ] Review Checklist: ≥18 checks
- [ ] Merge Checklist: ≥15 checks
- [ ] Test & Proof: ≥18 proof categories
- [ ] Forbidden Actions: ≥18 forbidden actions
- [ ] Planning Seal: _PLANNING_SEALED
- [ ] Planning Closeout: _PLANNING_READY_FOR_REVIEW
- [ ] Merge Closeout: _MERGE_REVIEW_READY_FOR_HUMAN_DECISION

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|OVERVIEW|v1.0.0-draft`
**Next**: SCOPE.md
