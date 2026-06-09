# Z2 Research Report Node Implementation Branch Approval Risk Register
## Status: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY
## Date: 2026-06-10 | Base HEAD: 03cc80c

### Risk 1: Z2 node bypasses B1 and reads Factor Library directly
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: Z2 may only import from composition_graph/ | **Control**: Import scan | **Rollback**: Any factor_library import
### Risk 2: Z2 node consumes FactorInvocationResponse directly
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: Type annotations enforce CompositionGraphResponse | **Control**: isinstance check in contracts | **Rollback**: FactorInvocationResponse found in Z2 code
### Risk 3: Z2 node calls real Z2/Z8/Z9/V3 runtime
- **Severity**: CRITICAL | **Likelihood**: VERY LOW | **Mitigation**: Import blocklist | **Control**: AST scan | **Rollback**: Any runtime import
### Risk 4: Denied graph context converted to valid research conclusion
- **Severity**: CRITICAL | **Likelihood**: MEDIUM | **Mitigation**: contracts enforce: denied→degraded report only | **Control**: Parametrized tests | **Rollback**: Denied context producing non-degraded report
### Risk 5: confidence_level HIGH_WITH_STRUCTURE_ONLY misread as profit confidence
- **Severity**: HIGH | **Likelihood**: MEDIUM | **Mitigation**: Documentation and type constraints | **Control**: Test verifying confidence semantics | **Rollback**: Any report with confidence interpreted as profit indicator
### Risk 6: alpha_claim leaks into report output
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: Output filter blocks alpha_claim | **Control**: Grep scan | **Rollback**: alpha_claim found in report output
### Risk 7: buy/sell/position/order fields leak
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: Model has zero trading fields | **Control**: AST scan | **Rollback**: Trading fields found
### Risk 8: paper trading / broker / real_trade leakage
- **Severity**: CRITICAL | **Likelihood**: VERY LOW | **Mitigation**: Blocked outputs enforced | **Control**: Import + field scan | **Rollback**: Forbidden found
### Risk 9: trade_result / real_pnl leakage
- **Severity**: CRITICAL | **Likelihood**: VERY LOW | **Mitigation**: No trade/PNL fields on any model | **Control**: AST scan | **Rollback**: PNL fields found
### Risk 10: z9_snapshot candidate contains trade result
- **Severity**: HIGH | **Likelihood**: LOW | **Mitigation**: Snapshot model excludes trade fields | **Control**: Test on snapshot output | **Rollback**: Trade field in z9_snapshot
### Risk 11: Evidence chain loses graph_node_hash / graph_edge_hash
- **Severity**: HIGH | **Likelihood**: LOW | **Mitigation**: Evidence builder inherits from B1 | **Control**: Test on evidence fields | **Rollback**: Missing hash in evidence
### Risk 12: z2_report_node_hash non-deterministic
- **Severity**: MEDIUM | **Likelihood**: LOW | **Mitigation**: Hash from sorted JSON | **Control**: Repeat-call test | **Rollback**: Same input→different hash
### Risk 13: z2_report_section_hash unstable
- **Severity**: MEDIUM | **Likelihood**: LOW | **Mitigation**: Section hash from sorted field keys | **Control**: Deterministic test | **Rollback**: Non-deterministic hash
### Risk 14: Report section fabricates missing evidence
- **Severity**: HIGH | **Likelihood**: LOW | **Mitigation**: Missing evidence inherited only, not generated | **Control**: Content contract test | **Rollback**: Fabricated evidence found
### Risk 15: Degraded graph upgraded to accepted report
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: DENY→degraded report forced | **Control**: Degradation test | **Rollback**: Degraded graph→valid report
### Risk 16: Runtime enablement prematurely activated
- **Severity**: CRITICAL | **Likelihood**: LOW | **Mitigation**: enabled()→False hardcoded | **Control**: Kill switch test | **Rollback**: enabled() returning True
### Risk 17: Result_envelope mutation
- **Severity**: HIGH | **Likelihood**: LOW | **Mitigation**: Frozen dataclasses, no in-place mut | **Control**: Immutability test | **Rollback**: Input response mutated
### Risk 18: Tests only cover happy path
- **Severity**: MEDIUM | **Likelihood**: MEDIUM | **Mitigation**: Full deny/degraded scenario matrix | **Control**: Merge checklist | **Rollback**: Incomplete test coverage
### Risk 19: Level 5 boundary drift
- **Severity**: CRITICAL | **Likelihood**: VERY LOW | **Mitigation**: Level 5 BLOCKED markers | **Control**: Doc review at merge | **Rollback**: Level 5 language found
### Risk 20: HIGH_WITH_STRUCTURE_ONLY misleads downstream
- **Severity**: MEDIUM | **Likelihood**: MEDIUM | **Mitigation**: Explicit semantics in docs + contract | **Control**: Label required on every report | **Rollback**: Missing structure disclaimer

## Summary: 20 risks. CRITICAL 10, HIGH 6, MEDIUM 4. All mitigated.
