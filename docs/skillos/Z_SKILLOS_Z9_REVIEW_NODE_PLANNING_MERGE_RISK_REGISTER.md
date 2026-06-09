# Z9 Review Node Planning — MERGE RISK REGISTER

> Status: MERGE | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Merge Reviewer: Final Gate

---

## 1. Merge Risk Register Purpose

This register identifies risks specific to merging the planning documentation branch.
Since this is a docs-only branch, risks are primarily about completeness, accuracy, and
future implementation misinterpretation. z9_review_snapshot_candidate is sole input.

## 2. Merge Risk Table

| # | Risk ID | Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| 1 | MRG-RSK-001 | Incomplete specification leads to wrong implementation | Medium | High | 42 test categories pre-specified |
| 2 | MRG-RSK-002 | Forbidden field list incomplete | Low | Critical | Comprehensive enumeration in contracts |
| 3 | MRG-RSK-003 | Contradictions between docs found post-merge | Low | Medium | Cross-doc consistency review |
| 4 | MRG-RSK-004 | trade_result not consistently forbidden | Low | Critical | Grep verification across all docs |
| 5 | MRG-RSK-005 | z2_feedback_candidate scope creep post-merge | Medium | High | Locked specification in policy doc |
| 6 | MRG-RSK-006 | Implementation deviates from planning | Medium | High | Planning docs as binding spec |
| 7 | MRG-RSK-007 | DENY_Z9_TRADE_RESULT_FORBIDDEN not comprehensive | Low | Critical | All trade fields listed |
| 8 | MRG-RSK-008 | Missing degradation state in spec | Low | Medium | 10 states fully enumerated |
| 9 | MRG-RSK-009 | Kill switch specification insufficient | Low | High | Defense-in-depth layers |
| 10 | MRG-RSK-010 | Test plan gaps discovered during implementation | Medium | Medium | 42 categories with mapping |
| 11 | MRG-RSK-011 | Import guard specification too narrow | Low | High | Explicit module blocklist |
| 12 | MRG-RSK-012 | Hash chain specification ambiguous | Low | Medium | Explicit field listing |
| 13 | MRG-RSK-013 | Review schema section count changes | Low | Low | 12 sections locked in spec |
| 14 | MRG-RSK-014 | Attribution policy misinterpreted | Low | High | Clear allowed/forbidden partition |
| 15 | MRG-RSK-015 | DISABLED_DEFAULT_NOOP not enforced in impl | Low | Critical | Test category #1 covers this |
| 16 | MRG-RSK-016 | Merge conflicts with concurrent changes | Low | Low | New files only, no conflicts expected |
| 17 | MRG-RSK-017 | Documentation becomes stale post-merge | Medium | Low | Living document maintenance |
| 18 | MRG-RSK-018 | Z9 feedback wrongly assumed to be binding | Medium | High | "advisory and readonly" in all docs |
| 19 | MRG-RSK-019 | no_trade_result marker omitted in future impl | Low | Critical | Output contract enforcement |
| 20 | MRG-RSK-020 | Execution path added in implementation phase | Medium | Critical | Kill switch + import guard tests |
| 21 | MRG-RSK-021 | V3 sandbox accidentally connected | Low | Critical | test_no_forbidden_imports coverage |
| 22 | MRG-RSK-022 | Z8 execution module imported | Low | Critical | Import guard in test suite |

## 3. Risk Summary by Category

| Category | Count | Highest Impact |
|---|---|---|
| Specification completeness | 6 | High |
| Safety/forbidden fields | 7 | Critical |
| Implementation deviation | 5 | Critical |
| Documentation quality | 2 | Medium |
| Merge mechanics | 2 | Low |

## 4. Critical Merge Risks

Critical risks that could block merge:
- MRG-RSK-002: Incomplete forbidden field list (mitigated by comprehensive enumeration)
- MRG-RSK-004: trade_result inconsistently forbidden (mitigated by grep verification)
- MRG-RSK-007: DENY_Z9_TRADE_RESULT_FORBIDDEN gaps (mitigated by listing all trade fields)
- MRG-RSK-015: DISABLED_DEFAULT_NOOP not enforced (mitigated by test category #1)
- MRG-RSK-019: no_trade_result omitted (mitigated by output contract)
- MRG-RSK-020: Execution path added (mitigated by kill switch + import guard)

## 5. Risk Acceptance for Merge

For docs-only merge, acceptable residual risks are:
- Documentation becoming stale (low impact, addressable later)
- Implementation deviation (mitigated by binding spec + tests)
- All critical risks have mitigation paths defined

## 6. Post-Merge Risk Monitoring

After merge:
- Implementation must reference planning docs
- Any deviation requires planning doc update
- Z9 feedback is advisory and readonly — enforce in code review
- Kill switch must be first implemented module
- test_no_forbidden_imports must be first test

## 7. Risk Register Sign-Off

Total risks: 22
Critical risks: 7 (all mitigated)
High risks: 6 (all mitigated)
Medium risks: 5 (all mitigated)
Low risks: 4 (accepted)
Sign-off: PENDING HUMAN REVIEW
Base: 5032c4d
