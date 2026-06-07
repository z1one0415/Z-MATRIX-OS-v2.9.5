# Z-SkillOS Level 4 No-Production Proof Plan

## Status

Z_SKILLOS_LEVEL4_NO_PRODUCTION_PROOF_PLAN_READY

## Purpose

Define the proof plan for Gate-4: No-Production Linkage. This document is a proof plan only. No proof execution. No code.

## Future Proof Objective

Level 4 has zero production/broker/real_trade linkage.

## Required Future Static Checks (CI)

| # | Check | Tool | Expected |
|:--|:--|:--|:--:|
| 1 | No broker imports | `grep -r "import broker\|from broker"` | 0 matches |
| 2 | No real_trade imports | `grep -r "import real_trade\|from real_trade"` | 0 matches |
| 3 | No production imports | `grep -r "import production\|from production"` | 0 matches |
| 4 | No trading credentials | `grep -r "api_key\|secret\|token\|credential"` | 0 matches (Level 4 only) |
| 5 | No production endpoints | `grep -r "live\.\|prod\.\|trading\."` | 0 matches |
| 6 | No real_trade payload | `grep -r "order\|execution\|position"` | 0 matches (Level 4 only) |
| 7 | No account identifiers | `grep -r "account_id\|user_id\|broker_account"` | 0 matches |
| 8 | AST scan for prohibited imports | `python3 -c "import ast; ..."` | Clean |

## Required Future Runtime Checks

| # | Check | Method |
|:--|:--|:--:|
| 1 | No network call | Mock all network calls; assert none reached |
| 2 | No order object | Mock all broker modules; assert none imported |
| 3 | No broker event | Assert no broker event handlers registered |
| 4 | No production write | Assert no production filesystem writes |

## Import Allowlist

Level 4 modules may only import from:

- `skillos/contract/` — read-only
- `skillos/audit/` — read-only
- `skillos/level3/` — observation evidence, read-only
- Standard library: `json`, `os.path`, `datetime`, `hashlib`, `logging`
- `zmatrix/config/` — config reader (Level 4 keys only)

Explicitly forbidden: `zmatrix/broker/`, `zmatrix/real_trade/`, `zmatrix/production/`, `zmatrix/order/`, `zmatrix/live/`.

## Explicit Statement

This document is a proof plan only. No proof execution. No code.
