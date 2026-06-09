# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — TEST_AND_PROOF_PLAN

> Comprehensive test and proof plan for Z2 Research Report Node (≥41 proof categories).
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | TEST_AND_PROOF_PLAN |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | Z9_HANDOFF_PREP.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document enumerates ALL proof categories required to validate the Z2 Research Report Node.
Each category represents a class of tests that must pass before the node is considered
implementation-ready. The node consumes B1 CompositionGraphResponse and produces explanatory
research reports with no_alpha_claim and no_trade_signal invariants.

---

## 3. Dependency / Evidence

### 3.1 Proof Categories (41 items)

| # | Category | Test File | Description |
|---|----------|-----------|-------------|
| 1 | DISABLED_DEFAULT_NOOP | test_disabled_default.py | Node returns NOOP when not explicitly enabled |
| 2 | INPUT_B1_ONLY | test_contracts.py | Only B1 CompositionGraphResponse accepted as primary input |
| 3 | INPUT_REJECT_FACTOR_INVOCATION | test_contracts.py | FactorInvocationResponse rejected at input |
| 4 | INPUT_REJECT_RAW_FACTORS | test_contracts.py | Raw factor values rejected at input |
| 5 | INPUT_REJECT_BROKER_DATA | test_contracts.py | Broker data rejected at input |
| 6 | INPUT_REJECT_REAL_TRADES | test_contracts.py | Real trade data rejected at input |
| 7 | INPUT_REJECT_PAPER_TRADES | test_contracts.py | Paper trade data rejected at input |
| 8 | INPUT_REJECT_Z8_Z9_V3 | test_contracts.py | Z8/Z9/V3 runtime data rejected at input |
| 9 | OUTPUT_ALLOWED_FIELDS_ONLY | test_models.py | Only 22 allowed output fields present |
| 10 | OUTPUT_FORBIDDEN_ALPHA_CLAIM | test_models.py | alpha_claim never in output |
| 11 | OUTPUT_FORBIDDEN_BUY_SIGNAL | test_models.py | buy_signal never in output |
| 12 | OUTPUT_FORBIDDEN_SELL_SIGNAL | test_models.py | sell_signal never in output |
| 13 | OUTPUT_FORBIDDEN_POSITION_WEIGHT | test_models.py | position_weight never in output |
| 14 | OUTPUT_FORBIDDEN_ORDER_SIGNAL | test_models.py | order_signal never in output |
| 15 | OUTPUT_FORBIDDEN_TRADE_INSTRUCTION | test_models.py | trade_instruction never in output |
| 16 | OUTPUT_FORBIDDEN_BROKER_ACTION | test_models.py | broker_action never in output |
| 17 | OUTPUT_FORBIDDEN_REAL_TRADE_ORDER | test_models.py | real_trade_order never in output |
| 18 | OUTPUT_FORBIDDEN_PRODUCTION_DECISION | test_models.py | production_decision never in output |
| 19 | REPORT_12_SECTIONS | test_report_builder.py | All 12 sections present in every report |
| 20 | REPORT_SECTION_ORDER | test_report_builder.py | Sections in fixed order 1-12 |
| 21 | REPORT_SECTION_METADATA | test_section_builder.py | Each section has required metadata fields |
| 22 | EVIDENCE_CHAIN_14_INHERITED | test_evidence.py | All 14 inherited fields from B1 present |
| 23 | EVIDENCE_CHAIN_HASH_DETERMINISM | test_evidence.py | Same input → same hash output |
| 24 | EVIDENCE_Z2_REPORT_NODE_HASH | test_evidence.py | z2_report_node_hash computed correctly |
| 25 | EVIDENCE_Z2_SECTION_HASH | test_evidence.py | z2_report_section_hash per section correct |
| 26 | EVIDENCE_Z2_EVIDENCE_HASH | test_evidence.py | z2_report_evidence_hash computed correctly |
| 27 | CONFIDENCE_THREE_LEVELS_ONLY | test_report_builder.py | Only LOW/MEDIUM/HIGH_WITH_STRUCTURE_ONLY |
| 28 | CONFIDENCE_REASON_NON_EMPTY | test_report_builder.py | confidence_reason always populated |
| 29 | CONFIDENCE_ASSIGNMENT_RULES | test_report_builder.py | Correct level assigned per evidence state |
| 30 | BLOCKED_OUTPUT_SCANNER_RUNS | test_report_builder.py | Scanner always executes before emission |
| 31 | BLOCKED_OUTPUT_12_PATTERNS | test_report_builder.py | All 12 forbidden patterns detected |
| 32 | BLOCKED_OUTPUT_REMOVAL_LOGGED | test_report_builder.py | Removed items logged in blocked_outputs_removed |
| 33 | DEGRADATION_9_DECISIONS | test_degradation.py | All 9 degradation decisions testable |
| 34 | DEGRADATION_PRIORITY_ORDER | test_degradation.py | Higher priority DENY overrides lower ALLOW |
| 35 | DEGRADATION_DENY_NO_REPORT | test_degradation.py | DENY decisions prevent report emission |
| 36 | Z9_SNAPSHOT_ALLOW_ONLY | test_z9_snapshot.py | Snapshot only under ALLOW decisions |
| 37 | Z9_SNAPSHOT_14_FIELDS | test_z9_snapshot.py | All 14 allowed fields present |
| 38 | Z9_SNAPSHOT_7_FORBIDDEN | test_z9_snapshot.py | All 7 forbidden fields absent |
| 39 | Z9_SNAPSHOT_HASH_IN_REPORT | test_z9_snapshot.py | Snapshot hash included in z2_report_node_hash |
| 40 | NO_FORBIDDEN_IMPORTS | test_no_forbidden_imports.py | No broker/trade/execution imports in codebase |
| 41 | READONLY_INVARIANT | test_models.py | readonly_only = true, no_alpha_claim = true, no_trade_signal = true always |

### 3.2 Test Infrastructure Requirements

- Fixture: Valid B1 CompositionGraphResponse with complete evidence chain
- Fixture: B1 response with missing optional fields (for degradation testing)
- Fixture: Deliberately corrupted inputs (for rejection testing)
- Fixture: Inputs containing forbidden output patterns (for scanner testing)
- All fixtures must reference fixture_source_commit traceable to 74c27fa

---

## 4. Boundary

- All 41 proof categories must have at least one test
- Tests must be deterministic (no random, no network, no time-dependent)
- Tests must run in isolation (no shared mutable state)
- Tests must not import forbidden modules even for testing purposes
- Test fixtures must use only synthetic/fixture data, never real market data

---

## 5. Forbidden Actions

- Skipping any of the 41 proof categories
- Using real market data in test fixtures
- Importing forbidden modules in test code
- Creating tests that depend on network access
- Creating tests that depend on Z8/Z9/V3 runtime
- Marking tests as skip/xfail without documented reason

---

## 6. Proof / Review Requirements

- All 41 categories must be listed in this document (verified ✓)
- Each category must map to a specific test file
- Test files listed in Future Files section of OVERVIEW.md
- Coverage must be verifiable through test runner output
- z9_review_snapshot_candidate testing must cover both ALLOW and DENY paths

---

## 7. Next Legal Entry

- Proceed to CLOSEOUT.md for planning phase closeout
- Test plan feeds into REVIEW_CHECKLIST.md verification
- Test results (future) feed into MERGE_CHECKLIST.md
