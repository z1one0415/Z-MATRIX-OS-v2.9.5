# Z-SkillOS Level 4 P1 Config Contract Plan

## Status

Z_SKILLOS_LEVEL4_P1_CONFIG_CONTRACT_PLAN_READY

## Scope

FUTURE_PLAN_ONLY. Defines Level 4 configuration safety rules for P1 and beyond. No code.

## Config Defaults

| Key | Default | Constraint |
|:--|:--|:--|
| `LEVEL4_WARNING_ENABLED` | `false` | Must remain false unless separately approved |
| `LEVEL4_AUDIT_FILE_ENABLED` | `false` | Sub-control; blocked unless master is true |
| `LEVEL4_OPERATOR_REPORT_ENABLED` | `false` | Sub-control; blocked unless master is true |

## Safety Rules

| # | Rule | Status |
|:--|:--|:--:|
| 1 | strict bool True only (P0 hardened) | ✅ ENFORCED |
| 2 | non-bool truthy values remain disabled | ✅ ENFORCED |
| 3 | missing config = disabled | ✅ ENFORCED |
| 4 | malformed config = disabled | ✅ ENFORCED |
| 5 | config parse failure = disabled | ✅ ENFORCED |
| 6 | env CANNOT enable (no env override path) | ✅ ENFORCED |
| 7 | config CANNOT read production/broker/real_trade path | FULLY FORBIDDEN |
| 8 | config CANNOT read account/credential/secret files | FULLY FORBIDDEN |
| 9 | enablement remains NOT AUTHORIZED | REQUIRED |
| 10 | Any enable requires separate human approval | REQUIRED |

## No implementation. No warning enablement.Level 5 remains BLOCKED.
