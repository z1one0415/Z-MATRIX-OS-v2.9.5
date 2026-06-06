# Z-SkillOS v1.2-A Runtime Isolation Spec

## Status

Z_SKILLOS_V1_2_A_RUNTIME_ISOLATION_SPEC_READY

## Core Rule

Level 3 may observe only. Level 3 may not influence runtime behavior.

## Isolation Requirements

1. No invoke_skill behavior change
2. No result_envelope mutation
3. No runtime blocking
4. No runtime warning returned to caller
5. No production/broker/real_trade linkage
6. No fail-closed behavior
7. No automatic baseline update
8. No runtime_reports write unless later gate approves dedicated non-runtime audit path
9. No hidden persistence
10. No implicit opt-in

## Future Dedicated Shadow Output Path

Any future Level 3 implementation must use a dedicated non-runtime audit path.

Required properties:

```text
path_type: non-runtime audit path
default_enabled: false
caller_visible: false
runtime_blocking: false
result_envelope_mutation: false
production_linkage: false
broker_linkage: false
real_trade_linkage: false
```

## Forbidden Runtime Effects

- changing skill result
- changing status
- changing risk_level
- appending warning metadata
- blocking invocation
- retrying invocation
- suppressing invocation
- writing production runtime reports
- creating broker-side side effects

## Required Future Proofs

Tests proving: disabled mode produces zero writes, shadow mode does not mutate result_envelope, shadow mode does not block runtime, shadow mode does not return warnings, shadow mode does not touch production/broker/real_trade, failure inside shadow auditor does not fail runtime.

## Final Policy

Runtime isolation is mandatory before Level 3 can be implemented.
