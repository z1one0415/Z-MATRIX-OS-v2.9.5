# Z-SkillOS Level 4 Rollback Proof Plan

## Status

Z_SKILLOS_LEVEL4_ROLLBACK_PROOF_PLAN_READY

## Purpose

Define the proof plan for Gate-6: Rollback Safety. This document is a proof plan only. No proof execution. No code.

## Future Proof Objective

Disabling Level 4 fully restores Level 3 behavior. No residual Level 4 artifacts remain.

## Required Controls

| Control | Behavior |
|:--|:--|
| Master disable | `LEVEL4_WARNING_ENABLED=false` — instantly stops all Level 4 behavior |
| Suppression | Human- or auto-suppress specific warning categories |
| Audit cleanup policy | Configurable retention; auto-cleanup on disable |
| Operator approval | Required for suppression override and emergency disable |
| Emergency disable | Immediate stop; all level 4 processes terminated |

## Required Future Evidence

| # | Evidence Item | Verification Method |
|:--|:--|:--|
| 1 | Disabled mode emits nothing | Same as Gate-1 proof |
| 2 | Rollback removes Level 4 side effects | File audit: no Level 4 files remain |
| 3 | Rollback preserves Level 3 outputs | Hash comparison of Level 3 outputs pre/post |
| 4 | Rollback never touches production/broker/real_trade | Static analysis for production writes |
| 5 | Disable preserves existing Level 3 state | Level 3 config/evidence/state unchanged |
| 6 | Enable→emit→disable→verify zero output | Full cycle test |

## Cycle Test Design

```
1. LEVEL4_WARNING_ENABLED=true              # Enable
2. Trigger warnings across all 10 categories # Emit
3. LEVEL4_WARNING_ENABLED=false              # Disable
4. Verify: no warnings emitted                # Verify
5. Verify: no Level 4 files modified          # Verify
6. Verify: Level 3 outputs unchanged          # Verify
```

## Forbidden

- Rollback leaves residual Level 4 artifacts
- Rollback touches production/broker/real_trade data
- Disable state is not fully reversible (enable→disable→enable should work)

## Explicit Statement

This document is a proof plan only. No proof execution. No code.
