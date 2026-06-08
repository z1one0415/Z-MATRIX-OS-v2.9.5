# Factor Library Read-Only Adapter Actual Implementation Branch Approval Risk Register

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_ACTUAL_IMPLEMENTATION_BRANCH_APPROVAL_RISK_REGISTER_READY
Base: postmerge @ c5ace3b | Level 5: BLOCKED | Items: 12

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|:--:|:--|:--:|:--:|:--|:--|:--|
| 1 | Implementation branch bypasses disabled-default (enables runtime) | CRITICAL | Medium | All enabled()→False hardcoded, no config bypass | CI: enabled()==False gate | Reject impl branch |
| 2 | Adapter implemented as executor (execute/run/trade methods) | CRITICAL | Medium | Allowed method whitelist; forbidden method grep in CI | Method name CI check | Block merge |
| 3 | Real factor call added (file/network read of factor library) | CRITICAL | Low | No file I/O, no network allowed | grep for imports | Revert code |
| 4 | Network/file IO leakage in adapter code | HIGH | Low | No network imports, no file writes in P0 | Import grep CI | Block PR |
| 5 | alpha_claim not filtered from output | CRITICAL | Medium | Output filter contract must remove alpha_claim | Filter presence CI | Block merge |
| 6 | buy/sell/position_weight not filtered | HIGH | Medium | Blocked outputs 5/5 enforced in output_filter | Output field check | Add filter |
| 7 | Forbidden execution method name leaks into adapter | HIGH | Medium | All 11 forbidden names listed, grep check | Method name grep | Block merge |
| 8 | C1 evidence handoff not implemented (missing source_commit) | HIGH | Medium | source_commit field required in evidence | Field presence CI | Reject evidence missing handoff |
| 9 | Denied factor degradation missing (DENY_* states) | HIGH | Medium | All 8 DENY states required in degradation module | State count CI | Add missing states |
| 10 | Tests only cover happy path, no disabled-default proof | MEDIUM | Medium | 6 test files required including test_disabled_default | Test presence CI | Add test |
| 11 | A1/B1 contract mismatch (FactorInvocationResponse field missing) | HIGH | Medium | FactorInvocationResponse schema must match A1 contract | Schema alignment check | Fix contract |
| 12 | Level 5 boundary drifts (production/broker path enabled) | CRITICAL | Low | Level 5 BLOCKED immutable; CI grep for production/broker | Production path CI | Block merge |

**Summary**: 4 CRITICAL | 5 HIGH | 2 MEDIUM | 1 LOW

> FactorLib Actual | Branch Approval Risk Register | 12 items | Level 5 BLOCKED