# Z-SkillOS Skill Composition Graph P0 Planning — REVIEW CHECKLIST

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Review Checklist Definition

This checklist enumerates every verification item that must be checked during the Review phase.
Each item maps to specific planning documents and contracts. Minimum: 18 checks.

## 2. Review Checks

| # | Check | Category | Target Docs | Status |
|---|-------|----------|-------------|--------|
| RC-01 | Node contract defines capability_id with valid format | Node Contract | NODE_CONTRACT_PLAN.md §2.1 | ⬜ |
| RC-02 | Node contract defines module_adapter_id with valid path | Node Contract | NODE_CONTRACT_PLAN.md §2.2 | ⬜ |
| RC-03 | Node contract defines permission_tier in range 0-1 (P0) | Node Contract | NODE_CONTRACT_PLAN.md §2.3 | ⬜ |
| RC-04 | Node contract defines valid JSON Schema for input_schema | Node Contract | NODE_CONTRACT_PLAN.md §2.4 | ⬜ |
| RC-05 | Node contract defines valid JSON Schema for output_schema | Node Contract | NODE_CONTRACT_PLAN.md §2.5 | ⬜ |
| RC-06 | Node contract defines degradation_result per protocol | Node Contract | NODE_CONTRACT_PLAN.md §2.6 | ⬜ |
| RC-07 | Node contract defines boundary with max limits | Node Contract | NODE_CONTRACT_PLAN.md §2.7 | ⬜ |
| RC-08 | Edge contract defines upstream and downstream node ids | Edge Contract | EDGE_CONTRACT_PLAN.md §2.1-2.2 | ⬜ |
| RC-09 | Edge contract defines allowed_data_fields (non-empty) | Edge Contract | EDGE_CONTRACT_PLAN.md §2.3 | ⬜ |
| RC-10 | Edge contract defines forbidden_data_fields | Edge Contract | EDGE_CONTRACT_PLAN.md §2.4 | ⬜ |
| RC-11 | Edge contract defines evidence_handoff with hash structure | Edge Contract | EDGE_CONTRACT_PLAN.md §2.5 | ⬜ |
| RC-12 | Edge contract enforces downstream_tier ≤ upstream_tier | Permission | EDGE_CONTRACT_PLAN.md §2.6 | ⬜ |
| RC-13 | Edge contract sets no_hidden_execution = true | Safety | EDGE_CONTRACT_PLAN.md §2.7 | ⬜ |
| RC-14 | DAG policy enforces node count ≤ 2 | DAG Policy | DAG_POLICY_PLAN.md §2.1 | ⬜ |
| RC-15 | DAG policy enforces depth ≤ 2 | DAG Policy | DAG_POLICY_PLAN.md §2.3 | ⬜ |
| RC-16 | DAG policy rejects cycles at compile time | DAG Policy | DAG_POLICY_PLAN.md §3.1 | ⬜ |
| RC-17 | DAG policy rejects self-edges | DAG Policy | DAG_POLICY_PLAN.md §3.2 | ⬜ |
| RC-18 | DAG policy is strictly sequential (no branching) | DAG Policy | DAG_POLICY_PLAN.md §2.4 | ⬜ |
| RC-19 | Permission propagation: equal tier accepted | Permission | PERMISSION_PROPAGATION_PLAN.md §4.1 | ⬜ |
| RC-20 | Permission propagation: de-escalation accepted | Permission | PERMISSION_PROPAGATION_PLAN.md §4.1 | ⬜ |
| RC-21 | Permission propagation: escalation rejected | Permission | PERMISSION_PROPAGATION_PLAN.md §4.1 | ⬜ |
| RC-22 | Permission propagation: no write/production/broker tiers | Permission | PERMISSION_PROPAGATION_PLAN.md §6 | ⬜ |
| RC-23 | Evidence propagation: node hash is deterministic | Evidence | EVIDENCE_PROPAGATION_PLAN.md §3.2 | ⬜ |
| RC-24 | Evidence propagation: edge hash links upstream | Evidence | EVIDENCE_PROPAGATION_PLAN.md §4 | ⬜ |
| RC-25 | Evidence propagation: graph decision hash aggregates all | Evidence | EVIDENCE_PROPAGATION_PLAN.md §5 | ⬜ |
| RC-26 | Evidence propagation: no persistence | Evidence | EVIDENCE_PROPAGATION_PLAN.md §7 | ⬜ |
| RC-27 | Failure degradation: D1 NOOP on node failure | Failure | FAILURE_DEGRADATION_PLAN.md §3 | ⬜ |
| RC-28 | Failure degradation: D2 PLAN_ONLY on graph failure | Failure | FAILURE_DEGRADATION_PLAN.md §4 | ⬜ |
| RC-29 | Failure degradation: D3 Partial Invalidation | Failure | FAILURE_DEGRADATION_PLAN.md §5 | ⬜ |
| RC-30 | Failure degradation: no fail-closed, no blocking | Failure | FAILURE_DEGRADATION_PLAN.md §6 | ⬜ |
| RC-31 | Loop prevention: no self-edge possible | Loop | LOOP_PREVENTION_PLAN.md §3 | ⬜ |
| RC-32 | Loop prevention: no cycle possible in P0 topology | Loop | LOOP_PREVENTION_PLAN.md §3 | ⬜ |
| RC-33 | Loop prevention: no tool recursion | Loop | LOOP_PREVENTION_PLAN.md §4 | ⬜ |
| RC-34 | Loop prevention: no hidden agent loop | Loop | LOOP_PREVENTION_PLAN.md §5 | ⬜ |
| RC-35 | Output boundary: result_envelope is immutable | Output | OUTPUT_BOUNDARY_PLAN.md §2 | ⬜ |
| RC-36 | Output boundary: no caller-visible warnings | Output | OUTPUT_BOUNDARY_PLAN.md §3 | ⬜ |
| RC-37 | Output boundary: no user-visible side effects | Output | OUTPUT_BOUNDARY_PLAN.md §5 | ⬜ |
| RC-38 | All docs marked FUTURE_PLAN_ONLY and Level 5 BLOCKED | Meta | ALL PLANNING DOCS | ⬜ |
| RC-39 | No Z-MATRIX or implementation references in any doc | Meta | ALL PLANNING DOCS | ⬜ |
| RC-40 | PLANNING_SEAL applied and PLANNING_CLOSEOUT valid | Meta | PLANNING_SEAL.md, PLANNING_CLOSEOUT.md | ⬜ |

## 3. Check Statistics

| Metric | Count |
|--------|-------|
| Total checks | 40 |
| Node Contract checks | 7 (RC-01 to RC-07) |
| Edge Contract checks | 6 (RC-08 to RC-13) |
| DAG Policy checks | 5 (RC-14 to RC-18) |
| Permission checks | 4 (RC-19 to RC-22) |
| Evidence checks | 4 (RC-23 to RC-26) |
| Failure checks | 4 (RC-27 to RC-30) |
| Loop checks | 4 (RC-31 to RC-34) |
| Output checks | 3 (RC-35 to RC-37) |
| Meta checks | 3 (RC-38 to RC-40) |

## 4. Review Completion Criteria

All 40 checks must be marked ✅ before the Review phase can close.
Any ❌ check requires a finding documented in REVIEW_DECISION_RECORD.md.

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|REVIEW|CHECKLIST|v1.0.0-draft`
