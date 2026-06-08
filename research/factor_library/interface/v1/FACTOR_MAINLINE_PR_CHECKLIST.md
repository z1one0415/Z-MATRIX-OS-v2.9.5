# Factor Library Mainline PR Checklist

**Purpose**: Ensure all factor library PRs are safe, consistent, and interface-compliant.

## PR MUST include:

### Safety Checks
- [ ] All `alpha_claim_allowed` fields are `false`.
- [ ] All `production` fields are `"BLOCKED"`.
- [ ] All `broker_runtime` fields are `"BLOCKED"`.
- [ ] All `real_trade` fields are `"BLOCKED"`.
- [ ] No `buy_signal` / `sell_signal` / `position_weight` / `alpha_claim` fields.
- [ ] No trade signal generated.
- [ ] No order generated.
- [ ] No broker instruction generated.
- [ ] No V13.6 execution.
- [ ] No paper trading execution.
- [ ] No alpha claim.

### Interface Compliance
- [ ] New factors include interface-compliant manifest.
- [ ] New factors include validation snapshot.
- [ ] New factors include guardrail profile.
- [ ] New factors include application contract.
- [ ] Pre-interface artifacts are marked `pre_interface_artifacts: true`.

### Consistency Checks
- [ ] Existing frozen candidates not mutated.
- [ ] Existing rejected factors not restored.
- [ ] No same-sample promotion.
- [ ] coverage fail + PASS conflict not present.
- [ ] PIT fail + PASS conflict not present.
- [ ] Source block + PASS conflict not present.

### CI Gate Compliance
- [ ] All schema files pass `json.tool` validation.
- [ ] No reference to alpha/production/broker/real_trade as "ALLOWED".
- [ ] No modification to SkillOS code.
- [ ] No modification to broker/trading/execution code.
