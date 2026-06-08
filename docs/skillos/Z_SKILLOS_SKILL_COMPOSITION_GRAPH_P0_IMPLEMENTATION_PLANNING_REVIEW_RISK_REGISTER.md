# Z-SkillOS Skill Composition Graph P0 Implementation Planning — REVIEW RISK REGISTER

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft
> Minimum: ≥12 risks

---

## 1. Purpose

This document registers all identified risks associated with the Skill Composition Graph P0
Implementation Planning package. Each risk is assessed for severity, likelihood, impact, and
mitigation strategy. Minimum: 12 risks.

## 2. Risk Register (≥12 Risks)

### Risk 1: Specification Drift from P0 Planning Designs
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R01 |
| Severity | HIGH |
| Likelihood | MEDIUM |
| Impact | Implementation specs may deviate from P0 Planning package designs |
| Mitigation | Cross-reference all planning docs against parent P0 Planning docs |
| Contingency | Mark deviations as intentional design decisions in DECISION_RECORD |
| Status | PENDING REVIEW |

### Risk 2: Incomplete Node Contract Specification
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R02 |
| Severity | HIGH |
| Likelihood | LOW |
| Impact | Missing fields or rules in node model cause P1+ implementation gaps |
| Mitigation | 10 NC rules with explicit pseudocode validation |
| Contingency | NC rules extensible to NC-11+ in P1 without breaking changes |
| Status | PENDING REVIEW |

### Risk 3: Edge Governance Model Too Permissive
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R03 |
| Severity | MEDIUM |
| Likelihood | LOW |
| Impact | Allow-list/deny-list intersection may have edge cases |
| Mitigation | EC-05 blocks any intersection; field governance tested in Cat 19-20 |
| Contingency | Add explicit field-level allow/deny decision log in P1 |
| Status | PENDING REVIEW |

### Risk 4: Hash Collision in SHA-256 Evidence
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R04 |
| Severity | LOW |
| Likelihood | VERY LOW |
| Impact | Two different node outputs produce same hash (cryptographically infeasible) |
| Mitigation | SHA-256 is collision-resistant; deterministic serialization prevents input ambiguity |
| Contingency | Add nonce or salt in P1 if hash uniqueness becomes critical |
| Status | PENDING REVIEW |

### Risk 5: Kahn's Algorithm Implementation Error in P1
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R05 |
| Severity | HIGH |
| Likelihood | MEDIUM |
| Impact | Cycle detection algorithm incorrectly implemented in P1 code |
| Mitigation | Pseudocode in DAG_VALIDATOR_PLAN §3; test vectors in TEST_AND_PROOF_PLAN |
| Contingency | Use well-tested library implementation if custom algorithm fails |
| Status | PENDING REVIEW |

### Risk 6: Permission Model Under-Specification
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R06 |
| Severity | MEDIUM |
| Likelihood | LOW |
| Impact | Tier 2-3 not defined, causing ambiguity when P1+ expands tiers |
| Mitigation | Clear enum in PERMISSION_PROPAGATION_PLAN §2 with P0 restrictions |
| Contingency | Tier definitions are extensible; monotonic rule applies to all tiers |
| Status | PENDING REVIEW |

### Risk 7: Degradation State Machine Ambiguity
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R07 |
| Severity | MEDIUM |
| Likelihood | LOW |
| Impact | Unclear when to degrade to PLAN_ONLY vs NOOP |
| Mitigation | Clear trigger table in DEGRADATION_PLAN §3 |
| Contingency | Add degradation decision matrix with explicit conditions in P1 |
| Status | PENDING REVIEW |

### Risk 8: Future File Path Conflicts
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R08 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Planned file paths conflict with existing or future SkillOS paths |
| Mitigation | Paths under `skillos/capability_invocation_os/composition/` are new |
| Contingency | Reserve paths in `.gitignore` or path registry |
| Status | PENDING REVIEW |

### Risk 9: Missing Edge Case Coverage
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R09 |
| Severity | MEDIUM |
| Likelihood | MEDIUM |
| Impact | Undiscovered edge cases cause P1+ implementation surprises |
| Mitigation | Edge case tables in NODE_MODEL_PLAN §5, EDGE_MODEL_PLAN §7, TEST §5 |
| Contingency | Add fuzz testing for node/edge contracts in P1 |
| Status | PENDING REVIEW |

### Risk 10: Branch Merge Conflict with Parent
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R10 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Merge conflicts when merging into parent branch |
| Mitigation | This branch is docs-only; conflicts unlikely with code branches |
| Contingency | Manual resolution; docs are independent of code |
| Status | PENDING REVIEW |

### Risk 11: Immutability Contract Violation in P1
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R11 |
| Severity | HIGH |
| Likelihood | LOW |
| Impact | P1 implementation allows post-build mutation, breaking evidence chain |
| Mitigation | Clear immutability contracts in NODE_MODEL_PLAN §4, OUTPUT_BOUNDARY_PLAN §5 |
| Contingency | Add runtime immutability enforcement with frozen flags |
| Status | PENDING REVIEW |

### Risk 12: Inconsistent Terminology Across Documents
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R12 |
| Severity | LOW |
| Likelihood | LOW |
| Impact | Same concept named differently in different docs |
| Mitigation | Standardized terminology: node, edge, graph, tier, degradation, evidence |
| Contingency | Add glossary in P1 if terminology drift detected |
| Status | PENDING REVIEW |

### Risk 13: Over-Specification Freezing P1+ Flexibility
| Attribute | Value |
|-----------|-------|
| Risk ID | R-R13 |
| Severity | MEDIUM |
| Likelihood | MEDIUM |
| Impact | Too-rigid P0 specs prevent natural evolution in P1+ |
| Mitigation | Explicitly mark P0 constraints as P0-only; note P1+ expansion paths |
| Contingency | P0 constraints are minimums; P1+ can expand without breaking |
| Status | PENDING REVIEW |

## 3. Risk Summary

| Severity | Count | Risk IDs |
|----------|:---:|------|
| HIGH | 4 | R-R01, R-R02, R-R05, R-R11 |
| MEDIUM | 6 | R-R03, R-R06, R-R07, R-R09, R-R13 |
| LOW | 3 | R-R04, R-R08, R-R10, R-R12 |
| **Total** | **13 risks** | ✅ ≥ 12 |

## 4. Risk Heat Map

```
Likelihood
  HIGH    │ [   ] [   ] [   ]
  MEDIUM  │ [   ] [R01] [   ]
          │       [R09]
          │       [R13]
  LOW     │ [R10] [R03] [R02]
          │ [R04] [R06] [R05]
          │ [R08] [R07] [R11]
          │ [R12]
  VERY LOW│ [   ] [   ] [   ]
          └──────────────────
            LOW   MED   HIGH
                Severity
```

## 5. Risk Monitoring

| Activity | Frequency |
|----------|-----------|
| Risk register review | At each review checkpoint |
| New risk identification | During review of each document |
| Risk mitigation verification | Before REVIEW_CLOSEOUT |
| Residual risk acceptance | In REVIEW_CLOSEOUT |

## 6. Mitigation Status

| Risk | Mitigation Implemented? | Residual Risk |
|------|:---:|------|
| R-R01 | PENDING | Needs cross-reference verification |
| R-R02 | ✅ 10 NC rules | Very Low |
| R-R03 | ✅ EC-05 blocks intersection | Very Low |
| R-R04 | ✅ SHA-256 + deterministic JSON | Negligible |
| R-R05 | PENDING | Depends on P1 implementation quality |
| R-R06 | ✅ Clear tier enum | Low |
| R-R07 | ✅ Trigger table | Low |
| R-R08 | ✅ New path prefix | Very Low |
| R-R09 | ✅ Edge case tables | Low |
| R-R10 | ✅ Docs-only branch | Very Low |
| R-R11 | PENDING | Depends on P1 implementation |
| R-R12 | ✅ Standardized terminology | Very Low |
| R-R13 | ✅ P0-only markers | Low |

## 7. Risk Governance

- Risks are tracked from REVIEW_GATE through MERGE_CLOSEOUT
- No unmitigated HIGH-severity risk may remain at REVIEW_CLOSEOUT
- Residual risks must be accepted and documented
- Risk register is reviewed during MERGE_REVIEW
