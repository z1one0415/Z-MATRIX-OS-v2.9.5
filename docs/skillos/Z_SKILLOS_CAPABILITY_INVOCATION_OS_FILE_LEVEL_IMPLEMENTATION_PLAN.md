# Z-SkillOS Capability Invocation OS File-Level Implementation Plan

## Status
Z_SKILLOS_CAPABILITY_OS_FILE_LEVEL_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Proposed file structure. Do not create these files in this phase.

## Future Registry Files
- skillos/capability_invocation_os/registry/schema.py
- skillos/capability_invocation_os/registry/loader.py
- skillos/capability_invocation_os/registry/z2_registry.json
- skillos/capability_invocation_os/registry/z8_registry.json

## Future Contract Files
- skillos/capability_invocation_os/contracts/skill_contract.py
- skillos/capability_invocation_os/contracts/validator.py

## Future Router Files
- skillos/capability_invocation_os/router/intent_parser.py
- skillos/capability_invocation_os/router/policy_engine.py
- skillos/capability_invocation_os/router/permission_checker.py

## Future Composition Files
- skillos/capability_invocation_os/composition/composer.py
- skillos/capability_invocation_os/composition/conflict_detector.py

## Future Guard Files
- skillos/capability_invocation_os/guard/preflight.py
- skillos/capability_invocation_os/guard/permission_guard.py
- skillos/capability_invocation_os/guard/side_effect_guard.py

## Future Evidence Files
- skillos/capability_invocation_os/evidence/bus.py
- skillos/capability_invocation_os/evidence/sealer.py

## Future Adapter Files (per Wave)
- skillos/capability_invocation_os/adapters/z2_adapter.py
- skillos/capability_invocation_os/adapters/z8_adapter.py

## Future Test Files
- tests/skillos/capability_invocation_os/test_registry.py
- tests/skillos/capability_invocation_os/test_router.py
- tests/skillos/capability_invocation_os/test_guard.py
- tests/skillos/capability_invocation_os/test_e2e.py

## Do not create these files in this phase. All FUTURE_PLAN_ONLY. Level 5 remains BLOCKED.
