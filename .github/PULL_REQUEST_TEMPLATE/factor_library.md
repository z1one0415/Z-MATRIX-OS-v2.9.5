# Factor Library PR Template

## Summary

<!-- Brief description of the factor library change -->

## Factor Changes

<!-- List factors added/modified/removed -->
- FXX: description

## Interface Compliance

- [ ] manifests/schemas/templates are valid JSON
- [ ] all `alpha_claim_allowed` = `false`
- [ ] all `production` = `"BLOCKED"`
- [ ] all `broker_runtime` = `"BLOCKED"`
- [ ] all `real_trade` = `"BLOCKED"`

## Safety Checks

- [ ] No alpha claim
- [ ] No trade signal
- [ ] No position/order/broker instruction
- [ ] No V13.6 execution
- [ ] No paper trading
- [ ] Frozen candidates preserved
- [ ] Rejected factors preserved
- [ ] coverage fail + PASS not present
- [ ] PIT fail + PASS not present
- [ ] source block + PASS not present

## CI Validation

- [ ] All JSON files pass `python3 -m json.tool`
- [ ] No SkillOS code modified
- [ ] No broker/trading/execution code modified
- [ ] No production/runtime_reports modified

## Pre-Interface Artifacts

- [ ] Any `pre_interface_artifacts = true` factors are NOT in `ready_for_candidate_review`

/label factor-library
