# Wave0 Controlled Read-Only Execution P0 Branch Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_CONTROLLED_READONLY_EXECUTION_P0_BRANCH_RISK_REGISTER_READY
Base: postmerge @ eca3f48 | Level 5: BLOCKED | Items: 12
| # | Risk | Sev | Lik | Mitigation | Rollback |
|:--|:--|:--:|:--:|:--|:--|
| BR1 | Code enables runtime accidentally | C | L | All enabled()→False hardcoded | Enabled() check |
| BR2 | Kill switch not wired | H | L | Explicit test: kill→all disabled | Kill active |
| BR3 | Config requested→enabled leak | H | L | Strict separation | Config rollback |
| BR4 | Seven-gate bypass | H | L | Any false→DENY | Gates→disabled |
| BR5 | Network import creep | C | L | grep guard in CI | Revert |
| BR6 | Z-MATRIX import creep | C | L | grep guard, explicit boundary | Revert |
| BR7 | Test pollution (real calls) | H | L | All tests mock/in-memory | Revert tests |
| BR8 | File write side effect | M | L | Evidence noop proof | Revert |
| BR9 | Decision model leak | M | L | Internal-only objects | Revert |
| BR10 | Boundary assertion raises | M | L | Degrade, never raise | Fix assertion |
| BR11 | Canary implies real execution | C | L | PLAN_ONLY, no real call | Canary blocked |
| BR12 | Scope creep to Wave1 | H | M | Explicit scope boundary | Reject creep |
Summary: 4 CRITICAL | 4 HIGH | 3 MEDIUM | 1 LOW
> Cap OS Wave0 | Controlled Exec P0 | Risk Register | 12 items
