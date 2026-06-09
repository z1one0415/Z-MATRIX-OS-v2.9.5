# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — REVIEW_RISK_REGISTER

> Risk register with ≥20 identified risks for Z2 Research Report Node review.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | REVIEW_RISK_REGISTER |
| Status | REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | REVIEW_CHECKLIST.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This risk register identifies 22 risks associated with the Z2 Research Report Node planning
and implementation. Each risk includes severity, likelihood, mitigation, control mechanism,
and rollback trigger. The node consumes B1 CompositionGraphResponse and produces reports
with no_alpha_claim and no_trade_signal invariants.

---

## 3. Dependency / Evidence

### Risk Register (22 Risks)

#### RISK-01: Forbidden Output Leakage
- **Severity**: CRITICAL
- **Likelihood**: LOW (with scanner) / HIGH (without)
- **Mitigation**: Blocked output scanner runs on every emission; 12 forbidden patterns checked
- **Control**: test_report_builder.py validates all 12 patterns blocked; z2_report_node_hash includes blocked_outputs_removed
- **Rollback Trigger**: Any forbidden output detected in production emission → immediate DISABLED_DEFAULT_NOOP

#### RISK-02: alpha_claim Emission
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: no_alpha_claim = true hardcoded invariant; scanner detects alpha_claim pattern
- **Control**: test_models.py OUTPUT_FORBIDDEN_ALPHA_CLAIM; contract validation at output boundary
- **Rollback Trigger**: alpha_claim field detected in any Z2 output → kill switch + full audit

#### RISK-03: Trade Signal Generation
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: no_trade_signal = true hardcoded invariant; buy_signal/sell_signal in blocklist
- **Control**: test_models.py OUTPUT_FORBIDDEN_BUY_SIGNAL/SELL_SIGNAL; output schema enforcement
- **Rollback Trigger**: Any trade signal field in output → kill switch + disable node

#### RISK-04: Non-B1 Input Acceptance
- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Mitigation**: Input contract validation rejects all non-B1 inputs; type checking at entry
- **Control**: test_contracts.py INPUT_B1_ONLY + 6 rejection tests; schema validation
- **Rollback Trigger**: Non-B1 input accepted → DENY_Z2_SOURCE_FORBIDDEN + audit log

#### RISK-05: Real Data Source Contamination
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: no_real_source_flag validation; DENY_Z2_REAL_SOURCE_FORBIDDEN decision
- **Control**: Evidence chain field verification; test_evidence.py validates flag propagation
- **Rollback Trigger**: Real source detected → immediate deny + node disable

#### RISK-06: Evidence Chain Integrity Failure
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: All 14 inherited fields verified present; hash determinism enforced
- **Control**: test_evidence.py EVIDENCE_CHAIN_14_INHERITED + HASH_DETERMINISM
- **Rollback Trigger**: Hash mismatch detected → DENY_Z2_EVIDENCE_INCOMPLETE

#### RISK-07: z2_report_node_hash Non-Determinism
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: Hash computation excludes non-deterministic inputs (timestamps, random)
- **Control**: test_evidence.py EVIDENCE_Z2_REPORT_NODE_HASH with fixture verification
- **Rollback Trigger**: Same input produces different hash → implementation bug, block release

#### RISK-08: Degradation Bypass
- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Mitigation**: Degradation pipeline is mandatory; cannot be skipped via configuration
- **Control**: test_degradation.py all 9 decisions tested; priority order enforced
- **Rollback Trigger**: Report emitted without degradation check → kill switch

#### RISK-09: DISABLED_DEFAULT_NOOP Overridden
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: Default state hardcoded; requires explicit enablement
- **Control**: test_disabled_default.py verifies NOOP on fresh initialization
- **Rollback Trigger**: Node active without explicit enablement → disable + investigate

#### RISK-10: z9_review_snapshot_candidate Under DENY
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Snapshot generation gated by ALLOW-only check
- **Control**: test_z9_snapshot.py Z9_SNAPSHOT_ALLOW_ONLY
- **Rollback Trigger**: Snapshot generated under DENY → invalidate snapshot + audit

#### RISK-11: Forbidden Import in Codebase
- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Mitigation**: Import guard checks; test_no_forbidden_imports.py scans all module files
- **Control**: CI gate prevents merge with forbidden imports; static analysis
- **Rollback Trigger**: Forbidden import detected → block PR, require removal

#### RISK-12: Confidence Level Inflation
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Only 3 levels permitted; HIGH_WITH_STRUCTURE_ONLY never implies trade confidence
- **Control**: test_report_builder.py CONFIDENCE_THREE_LEVELS_ONLY
- **Rollback Trigger**: Non-standard confidence level detected → reject report

#### RISK-13: Section Omission in Report
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: All 12 sections mandatory; schema validation ensures presence
- **Control**: test_report_builder.py REPORT_12_SECTIONS
- **Rollback Trigger**: Report with <12 sections → reject + log

#### RISK-14: blocked_outputs_removed Omission
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: Field is mandatory even when empty (empty list); validator checks presence
- **Control**: test_report_builder.py BLOCKED_OUTPUT_SCANNER_RUNS
- **Rollback Trigger**: Output without blocked_outputs_removed → reject emission

#### RISK-15: Z9 Forbidden Field Inclusion
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: 7 forbidden Z9 fields checked at snapshot generation
- **Control**: test_z9_snapshot.py Z9_SNAPSHOT_7_FORBIDDEN
- **Rollback Trigger**: Forbidden field in snapshot → invalidate + re-generate

#### RISK-16: Stale B1 Input Processing
- **Severity**: LOW
- **Likelihood**: MEDIUM
- **Mitigation**: Freshness check on B1 response; stale input → ALLOW_Z2_DEGRADED_REPORT
- **Control**: Input validation checks fixture_source_commit lineage
- **Rollback Trigger**: Extremely stale input (>7d) → DENY_Z2_EVIDENCE_INCOMPLETE

#### RISK-17: Position Weight Emission
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: position_weight in forbidden output blocklist; no_position_weight = true invariant
- **Control**: test_models.py OUTPUT_FORBIDDEN_POSITION_WEIGHT
- **Rollback Trigger**: position_weight in output → kill switch + full audit

#### RISK-18: Broker Action Emission
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: broker_action in forbidden output blocklist; no broker module imports permitted
- **Control**: test_models.py OUTPUT_FORBIDDEN_BROKER_ACTION + test_no_forbidden_imports.py
- **Rollback Trigger**: broker_action in output → kill switch + immediate disable

#### RISK-19: Report Template Injection
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Template is internal, immutable at runtime; no external template loading
- **Control**: Template loaded from constants.py only; no file system reads for templates
- **Rollback Trigger**: Template modification at runtime detected → DENY_Z2_EXECUTION_FORBIDDEN

#### RISK-20: Hash Collision in Evidence Chain
- **Severity**: LOW
- **Likelihood**: VERY LOW
- **Mitigation**: SHA256 used for all hash computations; collision probability negligible
- **Control**: Hash computation tests with diverse inputs verify no collisions in test set
- **Rollback Trigger**: Collision detected (astronomically unlikely) → investigate + rotate hash algorithm

#### RISK-21: Incomplete Planning Coverage
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: 41 proof categories explicitly enumerated; each maps to test file
- **Control**: REVIEW_CHECKLIST.md check #26 verifies all 41 present
- **Rollback Trigger**: Missing proof category discovered post-seal → new planning cycle required

#### RISK-22: Implementation Drift from Planning
- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Mitigation**: Sealed planning documents are binding; implementation must match exactly
- **Control**: Code review against planning docs; test suite validates all planned behaviors
- **Rollback Trigger**: Implementation deviates from plan → block merge + document deviation

---

## 4. Boundary

- All 22 risks must be addressed before merge approval
- CRITICAL risks require verified controls before any code is written
- HIGH risks require mitigation plan accepted before implementation
- MEDIUM/LOW risks must be acknowledged with monitoring plan
- No risk may be dismissed without documented justification

---

## 5. Forbidden Actions

- Dismissing CRITICAL risks without mitigation
- Reducing severity without evidence
- Removing risks from the register
- Approving merge with unaddressed CRITICAL risks
- Implementing without all control mechanisms in place
- Ignoring rollback triggers in production

---

## 6. Proof / Review Requirements

- Each risk mitigation must map to at least one test in TEST_AND_PROOF_PLAN.md
- CRITICAL risks must have multiple independent controls
- Rollback triggers must be automatable (not manual-only)
- z9_review_snapshot_candidate risks must be verified end-to-end
- no_alpha_claim and no_trade_signal risks are non-negotiable CRITICAL

---

## 7. Next Legal Entry

- Proceed to REVIEW_DECISION_BRIEF.md with risk summary for human
- All CRITICAL risks feed into MERGE_RISK_REGISTER.md
- Rollback triggers documented for operational readiness
