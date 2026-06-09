# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — MERGE RISK REGISTER

## 1. Status

- Phase: MERGE REVIEW
- Risk Count: 20 (≥18 required)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Merge: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION

## 2. Scope

Merge-specific risk register for B1 Composition Graph Factor Bridge Implementation
Planning. B1 consumes A1FactorBridgeResponse ONLY. Denied context cannot become
valid node. Each risk has severity, likelihood, mitigation, control, and rollback trigger.

### 2.1 Merge Risk Register (20 risks)

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|---|---|---|---|---|---|---|
| MR-01 | Code file accidentally included in merge | CRITICAL | LOW | git diff --name-only verification | Pre-merge CI check | .py file in merge diff |
| MR-02 | Test file accidentally included | CRITICAL | LOW | git diff --name-only verification | Pre-merge CI check | test_*.py in merge diff |
| MR-03 | Merge conflict corrupts planning doc | HIGH | LOW | Rebase before merge + conflict check | Manual review | Conflict markers in merged file |
| MR-04 | Seal marker removed during merge | HIGH | VERY LOW | Post-merge grep verification | Marker check script | Seal marker absent post-merge |
| MR-05 | Closeout marker removed during merge | HIGH | VERY LOW | Post-merge grep verification | Marker check script | Closeout marker absent |
| MR-06 | Dependency seal reference corrupted | HIGH | VERY LOW | Hash comparison post-merge | Automated hash check | Seal hash mismatch |
| MR-07 | Branch merged without review approval | CRITICAL | LOW | Branch protection rules | GitHub/GitLab settings | Merge without APPROVE record |
| MR-08 | Fast-forward merge instead of squash | MEDIUM | LOW | Merge command verification | --squash flag enforcement | Non-squash merge detected |
| MR-09 | "runtime enablement authorized" phrase introduced | CRITICAL | VERY LOW | grep verification post-merge | CI content check | Forbidden phrase found |
| MR-10 | Research/data/runtime files included | HIGH | LOW | Directory diff verification | Pre-merge check | Non-docs files in diff |
| MR-11 | Incomplete document set merged (< 26 files) | HIGH | LOW | File count verification | find + wc check | File count < 26 |
| MR-12 | Document below line count minimum | MEDIUM | LOW | wc -l verification per file | Automated line count | Any file below minimum |
| MR-13 | A1FactorBridgeResponse reference removed | HIGH | VERY LOW | grep verification | Content check | Phrase absent in merged docs |
| MR-14 | c1_handoff_marker reference removed | HIGH | VERY LOW | grep verification | Content check | Phrase absent in merged docs |
| MR-15 | denied context becomes valid node phrase removed | HIGH | VERY LOW | grep verification | Content check | Invariant phrase absent |
| MR-16 | Git tag accidentally created | MEDIUM | LOW | git tag list verification | Pre-merge check | Unexpected tag on branch |
| MR-17 | Merge to wrong target branch | CRITICAL | LOW | Target branch verification | Branch protection | Merged to non-main branch |
| MR-18 | Post-merge implementation without separate branch | CRITICAL | MEDIUM | Process enforcement | Branch naming convention | Code on main after merge |
| MR-19 | Duplicate document names causing overwrite | LOW | VERY LOW | ls + sort verification | File name uniqueness | Fewer files than expected |
| MR-20 | Stale branch merged (outdated relative to main) | MEDIUM | LOW | Rebase verification | Age check | Branch >7 days behind main |

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Merge risks are separate from review risks (no duplication)
- Each merge risk is specific to the merge operation itself
- All risks must have complete fields
- CRITICAL risks block merge if unmitigated

## 5. Forbidden Actions

- NO merge without all CRITICAL risks mitigated
- NO runtime enablement (runtime enablement is not authorized)
- NO acceptance of unmitigated CRITICAL risks
- NO code creation to address merge risks

## 6. Proof / Review Requirements

- All 20 risks must be acknowledged by merge approver
- CRITICAL risks require explicit mitigation verification
- Rollback triggers must be monitorable post-merge

## 7. Next Legal Entry

- MERGE_DECISION_BRIEF: final merge executive summary
- MERGE_CLOSEOUT: merge completion

---
