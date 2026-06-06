# Z-SkillOS v1.2-A Rollback and Kill-Switch Spec

## Status

Z_SKILLOS_V1_2_A_ROLLBACK_KILL_SWITCH_SPEC_READY

## Default State

Any future Level 3 implementation must default to disabled:

```text
SKILLOS_LEVEL3_ENABLED=false
```

## Kill-Switch Requirements

A future Level 3 system must include:

1. Single config switch
2. Default-off behavior
3. Explicit opt-in only
4. No runtime writes when disabled
5. No audit path writes when disabled
6. No hidden background process
7. No broker/real_trade exposure
8. No automatic re-enable

## Rollback Requirements

A future implementation must include:

1. Branch-level rollback command
2. Config-level disable command
3. Test rollback command
4. Verification command proving no Level 3 side effects
5. Documented recovery path
6. Safe failure mode

## Required Future Commands (examples only)

```bash
export SKILLOS_LEVEL3_ENABLED=false
python3 scripts/skillos/verify_level3_disabled_mode.py
git revert <level3_commit>
```

These are examples for future implementation. Must not be created in this spec pack.

## Failure Policy

If Level 3 shadow observer fails:

```text
runtime_action: CONTINUE
caller_visible_warning: false
result_envelope_mutation: false
runtime_blocking: false
enforcement: DISABLED
```

## Final Policy

No Level 3 implementation can proceed without rollback and kill-switch proof.
