# Z-SkillOS v1.2 Runtime Isolation and Rollback Policy

## Status

Z_SKILLOS_V1_2_RUNTIME_ISOLATION_AND_ROLLBACK_POLICY_READY

## Core Policy

Any future Level 3 runtime observation must be isolated from the runtime decision path.

## Runtime Isolation Rules

1. No invoke_skill behavior change
2. No result_envelope mutation
3. No runtime blocking
4. No runtime warning returned to caller
5. No production/broker/real_trade linkage
6. No fail-closed behavior
7. No automatic baseline update
8. No runtime_reports write unless separately approved
9. Shadow output to dedicated non-runtime audit path only (future gate)

## Rollback Policy

Any future Level 3 implementation must include:

1. Single-switch disable path
2. Branch-level rollback instruction
3. Config-level disable instruction
4. Test proving disabled mode produces zero side effects
5. No persistence when disabled
6. No production exposure

## Kill-Switch Requirements

Future Level 3 cannot start unless it provides:

- `SKILLOS_LEVEL3_ENABLED=false` default
- Explicit opt-in only
- Test proving default disabled
- Test proving no runtime mutation
- Test proving no blocking

## Human Approval Policy

Before any future Level 3 implementation:

1. Planning gate approval required
2. Implementation gate approval required
3. Closeout review required
4. No automatic escalation to Level 4
5. No automatic escalation to Level 5

## Forbidden in v1.2 Planning Gate

- implementation
- runtime hook
- result_envelope mutation
- warning path
- blocking path
- fail-closed behavior
- production/broker/real_trade
- V12.x advancement
- tag

## Final Policy

v1.2 may plan Level 3. v1.2 may not implement Level 3.
