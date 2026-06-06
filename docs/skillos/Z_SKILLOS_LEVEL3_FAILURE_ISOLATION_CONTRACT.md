# Z-SkillOS Level 3 Failure Isolation Contract

## Status

Z_SKILLOS_LEVEL3_FAILURE_ISOLATION_CONTRACT_READY

## Core Rule

Any Level 3 failure must not affect runtime behavior.

## Failure Behavior

| Source | Runtime Action | Caller Warning | Result Mutation |
|:--|:--:|:--:|:--:|
| config failure | CONTINUE | false | false |
| redaction failure | CONTINUE | false | false |
| audit writer failure | CONTINUE | false | false |
| observer failure | CONTINUE | false | false |
| adapter failure | CONTINUE | false | false |

## Required Future Tests

Config/redaction/writer/observer/adapter failures don't block runtime, don't mutate result_envelope, don't return caller warning.

## Final

Failure isolation mandatory before any runtime integration.
