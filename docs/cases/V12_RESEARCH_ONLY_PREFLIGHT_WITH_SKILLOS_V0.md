# V12 Research-only Preflight with Z-SkillOS v0

## Status

V12_RESEARCH_ONLY_PREFLIGHT_PENDING

## Preconditions

Required state before V12 work starts:

- V11.6.3 OOS completion audit PASS
- contract_purity_ok=true
- completion_ready_for_v12_gate=true
- v12_blocking_reasons=[]
- Z-SkillOS v0 merged
- full-system verify PASS
- agent kernel verify PASS
- production=BLOCKED
- broker_runtime=BLOCKED
- real_trade=BLOCKED
- ready_for_alpha_claim=false
- alpha_validated=false

## V12 Scope

Allowed:

- research-only Alpha Operating Loop design
- factor lifecycle registry draft
- Z9 autopsy schema draft
- parameter calibration draft
- factor promotion/downgrade/retirement review draft
- no-production safety gates

Forbidden:

- alpha claim
- production runtime
- broker/runtime
- real trade
- buy/sell/hold
- portfolio decision
- order generation
- main ResearchDB write
- main Memory write

## Required V12 Gate

V12 must start with a preflight gate, not implementation.

The first V12 task must produce:

- V12_ALPHA_LOOP_RESEARCH_ONLY_PREFLIGHT.json
- V12 safety gate audit
- V12 input contract
- V12 output contract
- V12 forbidden action list
- V12 verify script
- V12 closeout skeleton

## Decision

V12 may only begin after this preflight is verified.

## Forbidden

Do not treat V12 as alpha validation.

Do not treat paper completion as tradable alpha.

Do not open production/broker/real_trade.
