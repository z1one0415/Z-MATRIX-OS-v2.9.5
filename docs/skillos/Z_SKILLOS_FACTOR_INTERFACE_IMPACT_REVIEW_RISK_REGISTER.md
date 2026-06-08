# Factor Interface Impact Review — Risk Register

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_RISK_REGISTER_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED | Items: 12

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|:--:|:--|:--:|:--:|:--|:--|:--|
| RR1 | A1/B1 merged without factor interface alignment | CRITICAL | Medium | Insert factor adapter planning first | Block merge until alignment | Revert merge |
| RR2 | FactorLibraryReadonlyAdapter scope too narrow | HIGH | Medium | Cover all 8 canonical intents | Intent count CI check | Expand scope |
| RR3 | Canonical intent mapping conflicts with existing A1 | HIGH | Low | Map intent to permission tier explicitly | Intent tier matrix review | Remap |
| RR4 | FactorEvidenceEnvelope incompatible with sandbox evidence | HIGH | Medium | Add factor evidence fields to schema | Schema compatibility check | Extend schema |
| RR5 | B1 composition graph skips factor permission propagation | HIGH | Low | Require factor permission in edge contract | Edge contract CI check | Add propagation |
| RR6 | Forbidden intent leak through composition graph | CRITICAL | Low | Blocked-output filtering on every edge | Edge output filter CI | Block graph |
| RR7 | alpha_claim leak through research context | CRITICAL | Low | Contract alpha_claim_allowed=false | Contract enforce CI | Strip alpha |
| RR8 | Degraded node state missing for denied factor | HIGH | Low | All 8 DENY states defined | DENY state count check | Add missing |
| RR9 | Factor adapter planning takes too long | MEDIUM | Medium | Parallelize with A1 scope freezing | Schedule tracking | Freeze scope |
| RR10 | C1 needs factor evidence rework | LOW | Low | Evidence schema already generic | Schema mapping proof | No change needed |
| RR11 | Parent interface baseline changes mid-review | MEDIUM | Low | Pin to d02b60c9 | Baseline SHA check | Update baseline |
| RR12 | Insufficient test coverage for factor intents | MEDIUM | Medium | 18 proof categories planned | Proof count CI | Add tests |

**Summary: 3 CRITICAL | 5 HIGH | 3 MEDIUM | 1 LOW**

## Boundary
No implementation. No code change. Level 5 BLOCKED.

> Factor Interface | Impact Review | Risk Register | 12 items | Level 5 BLOCKED