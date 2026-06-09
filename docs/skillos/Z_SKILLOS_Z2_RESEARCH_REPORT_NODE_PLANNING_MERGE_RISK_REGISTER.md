# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — MERGE_RISK_REGISTER

> Merge risk register with ≥18 implementation risks for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | MERGE_RISK_REGISTER |
| Status | MERGE_REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | MERGE_CHECKLIST.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This risk register identifies 20 implementation-phase risks that could arise when
building the Z2 Research Report Node based on the sealed planning. Each risk has
severity, likelihood, mitigation, control, and rollback trigger.

The node consumes B1 CompositionGraphResponse and must maintain no_alpha_claim
and no_trade_signal invariants throughout implementation.

---

## 3. Dependency / Evidence

### Implementation Risk Register (20 Risks)

#### MRISK-01: Implementation Deviates from Planning
- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Mitigation**: Code review against sealed planning docs; automated spec compliance checks
- **Control**: PR review requires mapping each module to planning document; z2_report_node_hash must match specification
- **Rollback Trigger**: Deviation detected in code review → block PR + document gap

#### MRISK-02: Forbidden Import Introduced
- **Severity**: CRITICAL
- **Likelihood**: MEDIUM
- **Mitigation**: test_no_forbidden_imports.py in CI; import blocklist maintained in constants.py
- **Control**: CI gate fails on forbidden import; pre-commit hook scans imports
- **Rollback Trigger**: Forbidden import in merged code → immediate revert + audit

#### MRISK-03: alpha_claim Logic Leak via Indirect Path
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: no_alpha_claim enforced at output boundary; content scanner catches indirect expressions
- **Control**: Property-based test generates random content → verifies no alpha patterns pass; z9_review_snapshot_candidate validated
- **Rollback Trigger**: Alpha-like content in output → kill switch + pattern database update

#### MRISK-04: Blocked Output Scanner Incomplete
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: All 12 patterns explicitly tested; scanner runs integration test with injected forbidden content
- **Control**: test_report_builder.py BLOCKED_OUTPUT_12_PATTERNS; coverage must hit all branches
- **Rollback Trigger**: Undetected forbidden output in integration test → block release

#### MRISK-05: Hash Computation Bug
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: z2_report_node_hash tested with golden fixtures; determinism verified across runs
- **Control**: test_evidence.py EVIDENCE_Z2_REPORT_NODE_HASH with multiple fixture sets
- **Rollback Trigger**: Hash non-determinism detected → fix + re-verify all fixtures

#### MRISK-06: Degradation Pipeline Skip Path
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: Degradation check is first operation after input receipt; no alternate path exists
- **Control**: test_degradation.py verifies all 9 decisions reachable; no early return before check
- **Rollback Trigger**: Report emitted without degradation check → kill switch

#### MRISK-07: DISABLED_DEFAULT Accidentally Enabled
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: Enablement requires explicit configuration with documented key; default config has node disabled
- **Control**: test_disabled_default.py verifies fresh init → NOOP; config validation
- **Rollback Trigger**: Node active in production without explicit enable → immediate disable

#### MRISK-08: Section Builder Emits Extra Fields
- **Severity**: MEDIUM
- **Likelihood**: MEDIUM
- **Mitigation**: Output schema validation rejects unknown fields; allowlist enforcement
- **Control**: test_section_builder.py verifies only defined fields present per section
- **Rollback Trigger**: Extra field detected → reject report + investigate

#### MRISK-09: Z9 Snapshot Contains Forbidden Data
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: z9_review_snapshot_candidate validated against allowed/forbidden field lists
- **Control**: test_z9_snapshot.py Z9_SNAPSHOT_7_FORBIDDEN + Z9_SNAPSHOT_14_FIELDS
- **Rollback Trigger**: Forbidden field in snapshot → invalidate + patch

#### MRISK-10: Confidence Level Assignment Bug
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Three-level enum type; no other values possible at type level
- **Control**: test_report_builder.py CONFIDENCE_THREE_LEVELS_ONLY; type system enforcement
- **Rollback Trigger**: Non-standard confidence emitted → reject report

#### MRISK-11: B1 Contract Change Upstream
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: B1 CompositionGraphResponse pinned to 74c27fa contract; version check at input
- **Control**: Input validation checks B1 response version/schema; integration test with B1 fixture
- **Rollback Trigger**: B1 contract change detected → disable Z2 until contract updated

#### MRISK-12: Test Coverage Gap
- **Severity**: MEDIUM
- **Likelihood**: MEDIUM
- **Mitigation**: 41 proof categories explicitly enumerated; coverage report required ≥95%
- **Control**: CI coverage gate; each proof category maps to specific test
- **Rollback Trigger**: Coverage below threshold → block merge

#### MRISK-13: Evidence Chain Field Dropped
- **Severity**: HIGH
- **Likelihood**: LOW
- **Mitigation**: All 14 inherited fields validated at input; missing field → DENY_Z2_EVIDENCE_INCOMPLETE
- **Control**: test_evidence.py EVIDENCE_CHAIN_14_INHERITED; field presence assertions
- **Rollback Trigger**: Missing field not caught → fix validation + regression test

#### MRISK-14: Report Section Ordering Violated
- **Severity**: LOW
- **Likelihood**: LOW
- **Mitigation**: Fixed ordering enforced by builder; sections numbered 1-12
- **Control**: test_report_builder.py REPORT_SECTION_ORDER
- **Rollback Trigger**: Out-of-order section → fix builder + regression test

#### MRISK-15: Kill Switch Mechanism Failure
- **Severity**: CRITICAL
- **Likelihood**: VERY LOW
- **Mitigation**: Kill switch is simple boolean check at entry; minimal code path
- **Control**: Dedicated kill_switch.py module; test verifies disable path works
- **Rollback Trigger**: Kill switch fails to disable → escalate to system admin

#### MRISK-16: no_trade_signal Bypass via Content
- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Mitigation**: Content scanner checks for trade signal language patterns beyond field names
- **Control**: Property-based tests with adversarial content; blocked_outputs_removed validation
- **Rollback Trigger**: Trade signal language in output → kill switch + pattern update

#### MRISK-17: Circular Dependency with Z9
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Z2 produces snapshot for Z9; Z9 never writes back to Z2; unidirectional
- **Control**: Import analysis ensures no Z9 imports in Z2 codebase
- **Rollback Trigger**: Z9 import detected in Z2 → remove + audit dependency

#### MRISK-18: Performance Degradation with Large Graphs
- **Severity**: LOW
- **Likelihood**: MEDIUM
- **Mitigation**: Input size limits defined (500KB B1 response, 100 nodes, 500 edges)
- **Control**: Integration test with max-size fixtures; timeout enforcement
- **Rollback Trigger**: Timeout in production → reject oversized input gracefully

#### MRISK-19: Template Injection via Research Question
- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Mitigation**: Research question treated as opaque string; no template interpolation
- **Control**: Test with adversarial research question content (injection attempts)
- **Rollback Trigger**: Template injection detected → sanitize + patch

#### MRISK-20: Stale Planning After Merge
- **Severity**: LOW
- **Likelihood**: MEDIUM
- **Mitigation**: Planning docs sealed and immutable; implementation must match sealed version
- **Control**: Implementation PR must reference planning commit; no planning modifications allowed
- **Rollback Trigger**: Planning modified post-merge → revert modifications + re-review

---

## 4. Boundary

- All 20 risks must be acknowledged before merge approval
- CRITICAL risks (4) require confirmed controls before implementation begins
- HIGH risks (5) require mitigation plan accepted
- MEDIUM risks (7) require monitoring plan
- LOW risks (4) acknowledged with standard development practices
- B1 CompositionGraphResponse stability is external dependency risk

---

## 5. Forbidden Actions

- Dismissing CRITICAL risks without verified controls
- Reducing severity without new evidence
- Removing risks from register
- Approving merge with unmitigated CRITICAL risks
- Implementing without kill switch mechanism
- Skipping test coverage for any proof category

---

## 6. Proof / Review Requirements

- Each risk control must map to at least one test in TEST_AND_PROOF_PLAN.md
- CRITICAL risks require multiple independent controls
- Rollback triggers must be automatable
- z9_review_snapshot_candidate risks verified with integration tests
- no_alpha_claim and no_trade_signal risks are non-negotiable

---

## 7. Next Legal Entry

- Proceed to MERGE_DECISION_BRIEF.md with risk summary
- After brief: MERGE_CLOSEOUT.md records final status
- Target: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
