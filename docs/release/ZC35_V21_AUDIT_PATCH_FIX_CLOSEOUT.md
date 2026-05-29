# ZC35-v2.1 Audit Patch Fix Closeout

## Status

ZC35-v2.1 status: **Research Prototype**
RC1 inclusion: FALSE
Production inclusion: FALSE
Broker/runtime inclusion: FALSE
Real trade inclusion: FALSE

## Fixes Applied

1. RC1_READINESS_SCORECARD.md restored to RC1_READY_RECOMMENDED (100/100).
2. ZC35-v2.1 explicitly marked as Research Prototype outside RC1 approval scope.
3. verify_zc35_v21_audit_patch.sh changed from local absolute path `$HOME/Documents/...` to repository-relative `ROOT=$(dirname $0)/..`.
4. pytest output no longer swallowed by `tail`.
5. LIVE_CASE_STUDY / not backtest / not cross-ticker / not production flags retained.
6. Added `tests/test_zc35_v21_audit_patch_fix.py` with 5 verification tests.

## Decision

ZC35-v2.1 may be used as **research evidence**.
ZC35-v2.1 must **not** be used as RC1 production capability.
ZC35-v2.1 requires **cross-ticker validation** before factor/pipeline promotion.
