# Z-SkillOS A1 Factor Library Bridge Implementation Branch Approval Risk Register

## Status: Z_SKILLOS_A1_FACTOR_LIBRARY_BRIDGE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY

## Date: 2026-06-09
## Base Branch: postmerge/skillos-v0-baseline-freeze
## Base HEAD: af1fc9a5bfe234386984c3e5d98b7ae447a58955

## Risk Register

### Risk 1: A1 bridge bypasses Factor Library adapter and reads factor_library directly

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Bridge implementation imports from research/factor_library or reads factor files directly, bypassing the Factor Library adapter safety layer.
- **Mitigation**: Bridge may ONLY consume FactorInvocationResponse objects from the Factor Library adapter. No import from research/ permitted. Source scan test required.
- **Control**: AST scan test for forbidden imports; git diff path filter at merge.
- **Rollback Trigger**: Any import or path reference to research/factor_library found in bridge code.

### Risk 2: A1 bridge invokes real Z-MATRIX module

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Bridge calls a real Z-MATRIX module (Z2/Z8/Z9/V3/gate_data/etc.) rather than consuming Factor Library adapter responses.
- **Mitigation**: Bridge has no imports from Z-MATRIX runtime modules. Only consumes dataclass responses. Import blocklist enforced.
- **Control**: Import scan test: no zmatrix runtime, no gate_data, no Z2/Z8/Z9 modules.
- **Rollback Trigger**: Any Z-MATRIX runtime import found in bridge code.

### Risk 3: Fixture response mistaken for real factor output in bridge context

- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Description**: Downstream of bridge treats fixture-sourced data as real factor analysis due to missing markers.
- **Mitigation**: Bridge MUST pass through no_real_source_flag, P1_FIXTURE_ONLY, and source_class=factor_library_fixture unchanged. Evidence fields preserved.
- **Control**: Test assertion on every bridge output verifying marker preservation.
- **Rollback Trigger**: Any bridge output missing no_real_source_flag or P1_FIXTURE_ONLY markers.

### Risk 4: Denied factor converted to valid bridge context node

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: A FactorInvocationResponse with DENY decision is transformed into a valid/usable context in the bridge layer, bypassing factor validation.
- **Mitigation**: Bridge contract: DENY decisions MUST produce degraded bridge output. No DENY response may become a valid planning node or context node.
- **Control**: Parametrized test across all DENY scenarios verifying degradation.
- **Rollback Trigger**: Any DENY factor producing non-degraded bridge output.

### Risk 5: forbidden_outputs_removed not passed through bridge

- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Description**: Bridge constructs new response objects without copying the forbidden_outputs_removed list from upstream Factor Library response.
- **Mitigation**: Bridge response builder MUST include forbidden_outputs_removed from source FactorInvocationResponse. Test assertion required.
- **Control**: Test verifying bridge output.forbidden_outputs_removed == source.forbidden_outputs_removed.
- **Rollback Trigger**: Any bridge output with empty or missing forbidden_outputs_removed.

### Risk 6: no_real_source_flag lost in bridge transformation

- **Severity**: HIGH
- **Likelihood**: MEDIUM
- **Description**: Bridge transforms or wraps Factor Library response without preserving the no_real_source_flag field.
- **Mitigation**: Bridge evidence envelope MUST include no_real_source_flag=True when source has it. Cannot drop or override.
- **Control**: Explicit test assertion on every bridge output evidence.
- **Rollback Trigger**: Any bridge evidence without no_real_source_flag when source had it.

### Risk 7: alpha_claim / position_weight / buy_signal leakage through bridge

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Bridge output contains alpha_claim, position_weight, buy_signal, sell_signal, or order_signal fields with actionable values.
- **Mitigation**: Bridge output filter removes all BLOCKED_OUTPUTS. Bridge never generates these fields. Test assertion required.
- **Control**: Parametrized test scanning all bridge outputs for forbidden signal fields.
- **Rollback Trigger**: Any non-null/non-zero signal field in bridge output.

### Risk 8: Runtime enablement prematurely activated in bridge

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Bridge adapter enabled() returns True or bridge config enables runtime features.
- **Mitigation**: Bridge adapter enabled() hardcoded False. Kill switch pattern from Factor Library P0 replicated.
- **Control**: Kill switch test for bridge adapter. Merge-blocking.
- **Rollback Trigger**: Any enabled() returning True in bridge adapter.

### Risk 9: Adapter execution enablement prematurely activated in bridge

- **Severity**: CRITICAL
- **Likelihood**: LOW
- **Description**: Bridge adds execute/run/call/invoke methods that perform real computation.
- **Mitigation**: No forbidden method names permitted. Only get_*/list_*/build_* methods allowed.
- **Control**: AST scan for forbidden method names. Merge-blocking.
- **Rollback Trigger**: Any execute/run/call/invoke method found in bridge code.

### Risk 10: result_envelope mutation in bridge layer

- **Severity**: HIGH
- **Likelihood**: LOW
- **Description**: Bridge modifies result_envelope safety markers, removing warnings or safety flags.
- **Mitigation**: Bridge MUST NOT mutate input responses. All operations produce new objects. No in-place modification.
- **Control**: Immutability test: verify source response unchanged after bridge processing.
- **Rollback Trigger**: Any mutation of input FactorInvocationResponse detected.

### Risk 11: Tests only cover happy path (safe fixture) in bridge

- **Severity**: MEDIUM
- **Likelihood**: MEDIUM
- **Description**: Bridge tests only verify the ALLOW_READONLY_CONTEXT fixture, missing all DENY scenarios and degradation paths.
- **Mitigation**: Test matrix must include: all 6 fixture scenarios, degradation for all 5 DENY paths, marker preservation, output filtering.
- **Control**: Minimum test category count in merge checklist.
- **Rollback Trigger**: Merge review finds incomplete test coverage of DENY scenarios.

### Risk 12: Level 5 boundary drift in bridge planning

- **Severity**: CRITICAL
- **Likelihood**: VERY_LOW
- **Description**: Bridge implementation introduces Level 5 planning language or pathway toward production/broker/real_trade enablement.
- **Mitigation**: All bridge documents and code must contain explicit Level 5 BLOCKED markers. No forward-looking Level 5 language.
- **Control**: Document review at merge; grep scan for Level 5 enablement language.
- **Rollback Trigger**: Any Level 5 enablement pathway found in bridge code or docs.

### Risk 13: Bridge creates dependency on unmerged parent branch code

- **Severity**: HIGH
- **Likelihood**: LOW
- **Description**: Bridge imports or references modules from v4.0-batch-0 or fix/ branches that are not on postmerge, creating unresolvable dependencies.
- **Mitigation**: Bridge may only import from skillos/capability_invocation_os/ modules that exist on postmerge. No cross-branch imports.
- **Control**: Import resolution test: all bridge imports must resolve on postmerge base.
- **Rollback Trigger**: Any unresolvable import in bridge code on postmerge base.

### Risk 14: Bridge duplicates Factor Library logic instead of consuming responses

- **Severity**: MEDIUM
- **Likelihood**: LOW
- **Description**: Bridge re-implements factor validation/scoring instead of consuming pre-validated FactorInvocationResponse.
- **Mitigation**: Bridge has no factor computation logic. Only response consumption, marker preservation, and degradation.
- **Control**: Code review at merge; no factor scoring or calculation functions.
- **Rollback Trigger**: Factor computation logic found in bridge code.

## Summary

| Severity | Count |
|:--|:--:|
| CRITICAL | 8 |
| HIGH | 4 |
| MEDIUM | 2 |
| **Total** | **14** |

## Conclusion

All identified risks have defined mitigations, controls, and rollback triggers.
No risk is unmitigated. Gate is ready for human decision.
