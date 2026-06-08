# Wave0 Execution Enablement P0 Branch Risk Register

## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_WAVE0_EXECUTION_ENABLEMENT_P0_BRANCH_RISK_REGISTER_READY
Base: postmerge @ bd4ac44 | Level 5: BLOCKED | Items: 10

| # | Risk | Prob | Impact | Level | Mitigation |
|:--|:--|:--:|:--:|:--:|:--|
| BR1 | Enablement code accidentally enables runtime | L | C | 🔴CRIT | All enabled() return False hardcoded |
| BR2 | Kill switch not wired | L | H | 🔴HIGH | Explicit test: kill=true→all disabled |
| BR3 | Config requested→enabled leak | L | H | 🔴HIGH | Strict separation: requested≠enabled |
| BR4 | Triple gate bypass | L | H | 🔴HIGH | Any false→DENY_DISABLED |
| BR5 | Network import in new code | L | C | 🔴CRIT | grep guard in CI |
| BR6 | Z-MATRIX import creep | L | H | 🟡MED | grep guard, explicit boundary |
| BR7 | Test pollution (real calls) | L | H | 🔴HIGH | All tests mock/in-memory only |
| BR8 | File write side effect | L | M | 🟡MED | Evidence noop proof |
| BR9 | Decision model leak (caller-visible) | L | M | 🟡MED | Internal-only decision objects |
| BR10 | Branch name collision | L | L | 🟢LOW | Unique branch name |

**Summary**: 2 CRITICAL | 4 HIGH | 3 MEDIUM | 1 LOW

> Cap OS Wave0 P0 | Branch Risk Register | 10 risks | Level 5 BLOCKED