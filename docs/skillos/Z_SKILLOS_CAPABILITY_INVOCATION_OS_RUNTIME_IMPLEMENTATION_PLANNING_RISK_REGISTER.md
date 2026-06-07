# Risk | Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_IMPLEMENTATION_PLANNING_RISK_REGISTER_READY
R1:Planning→runtime S:Critical L:Medium M:PLAN_ONLY C:Runtime gate R:Code without gate
R2:Registry→executable S:Critical L:Medium M:FUTURE_PLAN_ONLY C:Registry gate R:Executable code
R3:Router→runtime S:Critical L:Low M:FUTURE_PLAN_ONLY C:Router gate R:Router code
R4:Engine→code S:Critical L:Low M:FUTURE_PLAN_ONLY C:Engine gate R:Engine code
R5:Guard→code S:Critical L:Low M:FUTURE_PLAN_ONLY C:Guard gate R:Guard code
R6:T5 unblocked S:Critical L:VeryLow M:NEVER_GRANTED C:Tier CI R:T5 invocation
R7:Evidence writable S:Medium L:Low M:Immutability C:Evidence CI R:Mutation
R8:Production coupling S:Critical L:VeryLow M:Forbidden C:No-production CI R:Production ref
R9:Adapter→code S:Critical L:Low M:Separate gate C:Adapter approval R:Adapter code
R10:Warning lineage S:Medium L:Low M:No warning C:Warning gate R:Warning enabled
R11:Merge no seal S:Medium L:Low M:Mandatory C:Merge gate R:Merge without seal
R12:Level 5 drift S:Medium L:Low M:BLOCKED C:CI grep R:Level 5 language
