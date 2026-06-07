# Z-SkillOS Capability Invocation OS Runtime Implementation Planning Review Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_IMPLEMENTATION_PLANNING_REVIEW_RISK_REGISTER_READY
R1:Planning→runtime S:Critical M:PLAN_ONLY C:Runtime gate R:Code without gate
R2:Registry→executable S:Critical M:FUTURE_ONLY C:Registry gate R:Executable
R3:Router→runtime S:Critical M:FUTURE_ONLY C:Router gate R:Router code
R4:Engine→code S:Critical M:FUTURE_ONLY C:Engine gate R:Engine code
R5:Guard→code S:Critical M:FUTURE_ONLY C:Guard gate R:Guard code
R6:T5 bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R7:Evidence mutation S:Medium M:Immutability C:Evidence CI R:Mutation
R8:Production coupling S:Critical M:Forbidden C:No-production CI R:Production ref
R9:Adapter→code S:Critical M:Separate gate C:Adapter approval R:Adapter code
R10:Warning lineage S:Medium M:No warning C:Warning gate R:Warning enabled
R11:Merge no seal S:Medium M:Mandatory C:Merge gate R:Merge no seal
R12:Level 5 drift S:Medium M:BLOCKED C:CI grep R:Level 5 language
