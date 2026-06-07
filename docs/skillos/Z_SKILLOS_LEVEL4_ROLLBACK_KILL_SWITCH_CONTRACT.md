# Z-SkillOS Level 4 Rollback Kill-Switch Contract

## Status

Z_SKILLOS_LEVEL4_ROLLBACK_KILL_SWITCH_CONTRACT_READY

## Required Controls

LEVEL4_WARNING_ENABLED=false default, emergency disable, rollback, suppression, cleanup scope, operator approval, regression pack.

## Required Behavior

Default disabled. Failure = CONTINUE. No mutation/blocking. Full disable. Rollback restores Level 3. No broker/real_trade.

## Tests Required

Default disabled emits nothing. Kill-switch disables. Rollback restores. Failure no block/mutation. No broker/real_trade.
