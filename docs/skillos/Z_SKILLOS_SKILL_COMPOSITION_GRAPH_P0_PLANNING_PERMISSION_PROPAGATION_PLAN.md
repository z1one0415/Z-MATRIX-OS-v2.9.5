# Z-SkillOS Skill Composition Graph P0 Planning — PERMISSION PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Permission Propagation Definition

Permission Propagation governs how permission tiers flow through the composition graph.
The core principle is **monotonic non-increasing**: downstream nodes must never have higher
permission than upstream nodes. Permission escalation is strictly forbidden.

## 2. Permission Tier Hierarchy (P0)

| Tier | Name | Allowed Operations | P0 Status |
|------|------|-------------------|-----------|
| 0 | READONLY | Read data only | Allowed |
| 1 | PLANNING | Read data + produce plans | Allowed |
| 2 | RESEARCH | Market research, external data fetch | BLOCKED |
| 3 | ADVISORY | Produce recommendations | BLOCKED |
| 4 | EXECUTION | Execute trades/actions | BLOCKED |
| 5 | PRODUCTION | Full production access | BLOCKED |

## 3. Core Rule: Downstream ≤ Upstream

The fundamental invariant:
```
For every edge (U → D): D.permission_tier ≤ U.permission_tier
```

If violated, the entire graph is FORBIDDEN from execution. No partial execution allowed.

## 4. Propagation Rules

### 4.1 Valid Propagation Patterns (P0)
| Upstream Tier | Downstream Tier | Valid? | Reason |
|--------------|----------------|--------|--------|
| 1 (PLANNING) | 1 (PLANNING) | ✅ | Equal propagation |
| 1 (PLANNING) | 0 (READONLY) | ✅ | Legitimate de-escalation |
| 0 (READONLY) | 0 (READONLY) | ✅ | Equal propagation |
| 0 (READONLY) | 1 (PLANNING) | ❌ | Escalation forbidden |

### 4.2 De-escalation Semantics
When downstream has lower tier than upstream:
- Upstream produces full results at its tier
- Downstream receives only data allowed at its lower tier
- Data filtering is applied at the edge level
- Evidence hash chain records the tier transition

## 5. Boundary Violations

### 5.1 Detection
Permission boundary violations are detected at compile-time during edge contract validation.
Every edge contract must include `permission_propagation` with explicit tier comparison.

### 5.2 Response to Violation
1. Edge is marked as FORBIDDEN
2. `propagation_valid` set to `false`
3. `violation_action` set to "FORBIDDEN"
4. Graph is placed in FORBIDDEN state
5. No node processing occurs
6. Graph decision hash includes FORBIDDEN marker
7. Reason is recorded: "Permission escalation detected: downstream tier X > upstream tier Y"

## 6. No Write Propagation

The following tier transitions are ABSOLUTELY FORBIDDEN in P0:
- Any transition to Tier 4 (EXECUTION)
- Any transition to Tier 5 (PRODUCTION)
- Any transition involving broker integration
- Any transition involving real_trade pathways
- Any transition from readonly/planning to advisory without explicit human approval

## 7. Permission Check Sequence

```
For each edge in graph:
  1. Read upstream node's permission_tier
  2. Read downstream node's permission_tier
  3. if downstream_tier > upstream_tier:
       → FORBIDDEN: permission escalation
  4. if downstream_tier > P0_MAX_TIER (1):
       → FORBIDDEN: P0 tier boundary exceeded
  5. if downstream_tier is PRODUCTION/BROKER/REAL_TRADE:
       → FORBIDDEN: write propagation
  6. → VALID: permission propagation consistent
```

## 8. Escalation Approval (Future Phase)

P0 does not support permission escalation. In future phases (P3+), escalation MAY be allowed
if ALL of the following conditions are met:
1. Explicit human approval in the approval chain
2. Documented justification for escalation
3. Audit trail recording the escalation
4. Time-bounded escalation window
5. Automatic de-escalation after completion

None of these are available in P0. Any escalation attempt is rejected.

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|PERMISSION_PROPAGATION|v1.0.0-draft`
