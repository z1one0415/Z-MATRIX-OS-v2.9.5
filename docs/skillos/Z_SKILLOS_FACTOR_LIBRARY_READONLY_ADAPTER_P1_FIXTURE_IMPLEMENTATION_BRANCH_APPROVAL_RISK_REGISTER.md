# Z-SkillOS Factor Library Read-Only Adapter P1 Fixture Implementation Branch Approval Risk Register

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_P1_FIXTURE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY

## Date: 2026-06-08
## Base Branch: postmerge/skillos-v0-baseline-freeze
## Base HEAD: 94ef1675e70cc165d683ead235be849c27db58e3

## Risk Register

### Risk 1: Fake fixture mistaken for real factor result

- **Severity**: CRITICAL
- **Likelihood**: LOW (with controls) / HIGH (without)
- **Description**: Downstream consumers treat fixture output as genuine factor analysis, leading to incorrect research conclusions or investment signals.
- **Mitigation**: All fixture outputs MUST carry `no_real_source_flag=True` and `P1_FIXTURE_ONLY=True`. Evidence bus rejects any output missing these markers.
- **Control**: Automated test assertion on every fixture output; merge-blocking CI check.
- **Rollback Trigger**: Any fixture output found without `no_real_source_flag=True` or `P1_FIXTURE_ONLY=True` markers.

### Risk 2: Copying real factor artifacts from parent branch

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Developer copies files from `v4.0-batch-0-final-hardgates-scope-lock` or `fix/research-f5-1-10-11-clean-rebuild` into the fixture branch, introducing real factor logic or data.
- **Mitigation**: Git diff whitelist verification at commit time. Only `skillos/adapters/` and `tests/` paths allowed. No file from research/ or parent branches.
- **Control**: Pre-merge diff audit; automated path filter in CI.
- **Rollback Trigger**: Any file traced to parent branch factor artifacts detected in diff.

### Risk 3: Fixture provider reads research/factor_library

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: `fixture_provider.py` imports or reads from `research/factor_library/` directory, accessing real factor computation code.
- **Mitigation**: Import blocklist test: `grep -r "research" skillos/` must return 0 hits. No pathlib/os.path references to research/.
- **Control**: Dedicated test `test_no_research_import.py`; merge-blocking.
- **Rollback Trigger**: Any import or path reference to `research/factor_library` found in implementation branch.

### Risk 4: no_real_source_flag missing from fixture output

- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Description**: A fixture method returns data without setting the `no_real_source_flag=True` field, making it indistinguishable from real data.
- **Mitigation**: Base class contract enforcement — all return types inherit from `FixtureResult` which has `no_real_source_flag=True` as immutable default.
- **Control**: Type system enforcement + parametrized test across all fixture methods.
- **Rollback Trigger**: Any fixture method returning a dict/object without `no_real_source_flag` field.

### Risk 5: P1_FIXTURE_ONLY evidence marker not propagated

- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Description**: Evidence bus entry created without `P1_FIXTURE_ONLY=True`, allowing fixture results to pass through downstream gates as if they were real.
- **Mitigation**: Evidence entry constructor requires `fixture_only=True` parameter for all P1 calls. Omission raises `EvidenceContractViolation`.
- **Control**: Contract test verifying evidence entries; integration test with evidence bus mock.
- **Rollback Trigger**: Any evidence entry without `P1_FIXTURE_ONLY` marker found in test output or runtime log.

### Risk 6: alpha_claim not filtered from fixture output

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Fixture output contains `alpha_claim_allowed=True` or any alpha signal, potentially triggering downstream trading logic.
- **Mitigation**: Fixture result contract explicitly sets `alpha_claim_allowed=False`. Assertion in every test.
- **Control**: Grep-based scan: `alpha_claim_allowed=True` must never appear outside test assertions. Merge-blocking.
- **Rollback Trigger**: `alpha_claim_allowed=True` found in any non-assertion context.

### Risk 7: position_weight or buy/sell signal in fixture output

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Fixture includes `position_weight`, `buy_signal`, `sell_signal`, or any tradeable signal field with non-zero/non-null values.
- **Mitigation**: Fixture contract enforces: `position_weight=0.0`, `buy_signal=None`, `sell_signal=None`. All trade-adjacent fields nullified.
- **Control**: Parametrized test scanning all fixture outputs for forbidden signal fields.
- **Rollback Trigger**: Any non-zero `position_weight` or non-None signal field in fixture output.

### Risk 8: production/broker/real_trade leakage

- **Severity**: CRITICAL
- **Likelihood**: VERY_LOW
- **Description**: Implementation branch introduces imports or references to production trading, broker connections, or real trade execution.
- **Mitigation**: Import blocklist: `production`, `broker`, `real_trade`, `trade_executor`, `order_router` — all forbidden.
- **Control**: `test_no_forbidden_imports.py` scanning entire skillos/ tree. Merge-blocking.
- **Rollback Trigger**: Any forbidden import detected anywhere in implementation branch.

### Risk 9: Runtime enablement prematurely activated

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: `enabled()` method returns `True` or kill switch is deactivated, allowing the adapter to be called in production context.
- **Mitigation**: `enabled()` hardcoded to `return False`. Kill switch test asserts this for every adapter class.
- **Control**: Existing P0 kill switch test suite (48 tests) must continue passing unchanged.
- **Rollback Trigger**: Any `enabled()` returning `True` or kill switch test failure.

### Risk 10: Adapter execution enablement prematurely activated

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: An `execute()`, `run()`, `call()`, or `invoke()` method is added that performs real computation beyond returning fixture data.
- **Mitigation**: Method naming convention: only `get_fixture_*()` methods allowed. No `execute/run/call/invoke` method names permitted.
- **Control**: AST scan test: forbidden method names check across all adapter files. Merge-blocking.
- **Rollback Trigger**: Any `execute/run/call/invoke` method found in implementation branch adapter code.

### Risk 11: Tests only cover happy path

- **Severity**: MEDIUM
- **Likelihood**: MEDIUM
- **Description**: Fixture tests only verify correct fixture return, missing edge cases: missing fields, malformed input, contract violations.
- **Mitigation**: Test matrix must include: happy path, missing field assertion, contract violation assertion, evidence marker assertion, kill switch assertion.
- **Control**: Minimum test categories required in merge checklist. Code coverage threshold.
- **Rollback Trigger**: Merge review finds <5 test categories or <80% fixture code coverage.

### Risk 12: Level 5 boundary drift

- **Severity**: CRITICAL
- **Likelihood**: VERY_LOW
- **Description**: Implementation introduces any Level 5 planning, specification, or pathway that could be interpreted as moving toward production/broker/real_trade enablement.
- **Mitigation**: All documents and code must contain explicit `Level 5 remains BLOCKED` markers. No forward-looking language about Level 5 enablement.
- **Control**: Document review at merge time; grep scan for Level 5 enablement language.
- **Rollback Trigger**: Any document or code containing Level 5 enablement pathway, timeline, or approval language.

### Risk 13: Fixture data contains real market data

- **Severity**: HIGH
- **Likelihood**: LOW
- **Description**: Fake fixture JSON contains real stock prices, real factor scores, or real market data copied from actual sources, which could be confused with live data.
- **Mitigation**: All fixture data must use obviously fake values (e.g., ticker="FAKE001", price=99.99, score=0.5). No real ticker symbols in fixture data.
- **Control**: Fixture data review; automated scan for known real ticker patterns in fixture files.
- **Rollback Trigger**: Real market data or real ticker symbols found in fixture files.

### Risk 14: Merge without required tests

- **Severity**: HIGH
- **Likelihood**: LOW
- **Description**: Implementation branch is merged before fixture tests are written and passing, leaving fixture code untested.
- **Mitigation**: Merge checklist requires: all fixture tests passing, minimum test count met, coverage threshold met.
- **Control**: Merge gate blocks until test evidence is provided in merge decision document.
- **Rollback Trigger**: Merge attempted without test evidence or with failing tests.

## Summary

| Severity | Count |
|:--|:--:|
| CRITICAL | 9 |
| HIGH | 4 |
| MEDIUM | 1 |
| **Total** | **14** |

## Conclusion

All identified risks have defined mitigations, controls, and rollback triggers.
No risk is unmitigated. Gate is ready for human decision.
