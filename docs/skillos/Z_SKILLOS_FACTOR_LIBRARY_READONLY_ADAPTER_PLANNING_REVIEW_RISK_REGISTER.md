# Factor Library Read-Only Adapter Planning — Review Risk Register

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_REVIEW_RISK_REGISTER_READY
Branch: plan/...factor-library-adapter | Level 5: BLOCKED | Items: 15

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|:--:|:--|:--:|:--:|:--|:--|:--|
| 1 | Factor adapter mis-implemented as executor (run/trade/alpha) | CRITICAL | Medium | Allowed method names restricted to 5 read-only operations | Method name CI check | Reject adapter implementation |
| 2 | A1/B1 merge before factor alignment | CRITICAL | Medium | Factor Library planning blocks A1/B1 merge | Merge gate dependency check | Revert A1/B1 merge |
| 3 | Canonical intent not aligned with parent interface | HIGH | Medium | 8 intents explicitly mapped, legacy aliases 4/4 | Intent coverage CI | Remap missing intents |
| 4 | Legacy alias leaked into adapter output | HIGH | Low | No legacy mode in output; explicit mapping table | Output format CI | Strip legacy from response |
| 5 | alpha_claim not filtered from output | CRITICAL | Medium | alpha_claim_allowed=false in contract | Output filter CI | Block output |
| 6 | position_weight not filtered from output | HIGH | Medium | blocked_outputs 5/5 includes position_weight | Output filter CI | Strip from response |
| 7 | buy/sell signal not filtered from output | HIGH | Medium | blocked_outputs 5/5 includes buy_signal, sell_signal | Output filter CI | Strip from response |
| 8 | ready_for_candidate_review=[] misinterpreted as ready | HIGH | Medium | Explicit check: empty list = NOT ready | List presence CI | Reject empty-as-ready |
| 9 | Batch3 backfill misread as promotion readiness | MEDIUM | Low | ready_for_candidate_review=[] confirmed | Null check CI | Block pipeline |
| 10 | FactorFamilyProfile new family bypasses family gate | HIGH | Medium | new_family_requires_review flag required | Flag presence CI | Deny un-gated family |
| 11 | EvidenceEnvelope source_commit not in evidence chain | HIGH | Medium | source_commit field required in envelope | Field presence CI | Reject evidence |
| 12 | Z8/V3 downstream not blocked | CRITICAL | Low | blocked_downstream_consumers 4/4 enforced | Downstream check CI | Block downstream |
| 13 | production/broker/real_trade BLOCKED ignored | CRITICAL | Low | Level 5 BLOCKED immutable | Tier gate CI | Reject |
| 14 | result_envelope mutation in adapter output | HIGH | Low | No result_envelope fields on response | Grep check | Reject adapter |
| 15 | SkillOS adapter implementation starts before planning seal | HIGH | Medium | No implementation rule in every doc | No-code grep CI | Revert code |

**Summary**: 5 CRITICAL | 7 HIGH | 2 MEDIUM | 1 LOW

> Factor Library | Planning | Review Risk Register | 15 items | Level 5 BLOCKED
## Evidence
- Parent baseline: d02b60c9 (V13.F5.1.2.1 accepted)
- Impact review: 22252711 (APPROVE_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING)
- Batch3 factors: F21, F22, F24, F26, F27, F30, F31, F34
- 8 canonical intents with 4 legacy aliases
- 7 forbidden intents (ALPHA_SIGNAL through PRODUCTION)
- C1 evidence schema compatible (no rework)
- A1/B1 blocked until alignment

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file/read write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No tag. Level 5 remains BLOCKED.

## Next
Human merge approval decision only. After merge: A1 hardening -> B1 hardening.
