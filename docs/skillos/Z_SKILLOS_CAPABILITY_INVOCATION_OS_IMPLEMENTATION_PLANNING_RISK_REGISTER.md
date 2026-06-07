# Z-SkillOS Capability Invocation OS Implementation Planning Risk Register

## Status
Z_SKILLOS_CAPABILITY_INVOCATION_OS_IMPLEMENTATION_PLANNING_RISK_REGISTER_READY

R1: Planning confounded with runtime | S:Critical L:Medium | Control: Gate rejects DIRECT_RUNTIME | Rollback: Runtime code
R2: Adapter plan misinterpreted | S:Critical L:Medium | Control: Separate adapter gate | Rollback: Adapter code
R3: Registry becomes executable | S:Medium L:Low | Control: FUTURE_PLAN_ONLY | Rollback: Executable registry
R4: Router becomes runtime | S:Critical L:Low | Control: FUTURE_PLAN_ONLY | Rollback: Router code
R5: Composition becomes runtime | S:Critical L:Low | Control: FUTURE_PLAN_ONLY | Rollback: Engine code
R6: Guard becomes runtime | S:Critical L:Low | Control: FUTURE_PLAN_ONLY | Rollback: Guard code
R7: T5 accidentally unblocked | S:Critical L:VeryLow | Control: T5 NEVER_GRANTED | Rollback: T5 invocation
R8: Evidence bus becomes executable | S:Medium L:Low | Control: FUTURE_PLAN_ONLY | Rollback: Evidence code
R9: Module adapter touches production | S:Critical L:VeryLow | Control: All adapters: production excluded | Rollback: Production import
R10: Warning enablement from lineage | S:Medium L:Low | Control: No warning enablement | Rollback: Warning enabled
R11: Merge without seal | S:Medium L:Low | Control: Post-merge seal mandatory | Rollback: Merge without seal
R12: Level 5 drift | S:Medium L:Low | Control: Level 5 remains BLOCKED | Rollback: Level 5 language
