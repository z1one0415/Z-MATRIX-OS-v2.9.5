# Factor Interface Impact Review — Risk Register

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_RISK_REGISTER_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED | Items: 15

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|:--:|:--|:--:|:--:|:--|:--|:--|
| R01 | A1 treats factor library as generic Z2 output, bypassing FactorApplicationContract validation | CRITICAL | Medium | Factor Library adapter must validate contract before passing to Z2 output reader | Factor contract check gate | Block A1 merge until factor adapter planned |
| R02 | B1 composition graph propagates alpha_claim / position_weight / buy_signal / sell_signal through unblocked edges | CRITICAL | Medium | Blocked-output filtering on every graph edge; forbidden_intent list in edge contract | Edge output filter CI | Reject graph if any forbidden output detected |
| R03 | Canonical intent (REGISTRY_READ) used interchangeably with legacy alias (RESEARCH_EVIDENCE_READ), causing permission bypass | HIGH | Medium | Explicit intent mapping table; reject legacy aliases in new code | Intent string CI check | Revert to canonical only |
| R04 | Batch3 interface backfill (F21-F34) misinterpreted as candidate promotion, triggering alpha pipeline | HIGH | Low | `ready_for_candidate_review=[]` confirmed empty; backfill is NOT promotion readiness | Empty-list CI check | Block promotion pipeline |
| R05 | `ready_for_candidate_review=[]` mistaken as "ready" by downstream parsers | HIGH | Medium | Explicit check: empty list means NOT ready. Require explicit `ready_for_candidate_review=["v13.5.n4"]` format. | List presence CI check | Reject empty-as-ready interpretation |
| R06 | New FactorFamilyProfile loaded without passing family gate validation | HIGH | Medium | Family gate required before any profile is used in composition graph | Family gate presence check | Block graph node if family gate missing |
| R07 | `promotion_allowed=false` ignored by downstream consumer (e.g., Z8 execution plan generator) | CRITICAL | Low | Contract must be checked before any downstream call; reject downstream if promotion_not_allowed | Contract check gate | Block downstream call |
| R08 | `production/broker/real_trade BLOCKED` bypassed by composition graph or adapter chain | CRITICAL | Low | Hard block at permission gate; Level 5 BLOCKED immutable | Permission tier CI | Reject graph if any production path detected |
| R09 | FactorEvidenceEnvelope `source_commit` field not propagated into evidence chain, breaking audit trail | HIGH | Medium | Evidence schema must include `source_commit` field; hash chain must commit to it | Field presence CI | Reject evidence without source_commit |
| R10 | Composition graph treats DENIED factor as valid node, allowing execution through denied path | CRITICAL | Medium | Degraded node state for all 8 DENY states; graph edge must check node state before propagation | Node state check | Block graph if degraded node has outgoing edges |
| R11 | SkillOS Factor Adapter implementation starts before planning is sealed (scope creep) | HIGH | Medium | Explicit no-implementation rule in every doc; planning seal required before any code | No-code grep CI | Revert implementation code |
| R12 | V13.F5.1.3 candidate review confuses SkillOS interface review timeline | MEDIUM | Medium | Separate review tracks; factor interface review is SkillOS-side, candidate review is research-side | Review ID tracking | Block merge if tracks cross |
| R13 | FactorInvocationResponse lacks unified `blocked_outputs_removed` flag, forcing duplicate filtering | MEDIUM | Low | Add `blocked_outputs_removed` bool to FactorInvocationResponse schema | Field presence CI | Reject response missing flag |
| R14 | A1/B1 merge order wrong: B1 merged before Factor Library adapter contract frozen, causing composition graph to reference nonexistent contract | HIGH | Medium | Enforce sequential merge: Factor Library → A1 → B1 | Merge order CI gate | Revert B1 merge |
| R15 | C1 evidence schema lacks `source_class=factor` but does not require rework — generic evidence handles all source classes | LOW | Low | Generic `source_class` field already in C1 evidence schema. Factor source_class is just one more value. | Schema mapping proof | No action needed |

**Summary**: 5 CRITICAL | 6 HIGH | 3 MEDIUM | 1 LOW

## Risk Severity Legend
- CRITICAL: Must be eliminated before A1/B1 merge
- HIGH: Must be mitigated with documented control
- MEDIUM: Monitored, accepted with mitigation
- LOW: Documented and accepted as-is

## Next
Human reviews all 15 risks → accept/reject each → decision seal

> Factor Interface | Impact Review | Risk Register | 15 items | Level 5 BLOCKED