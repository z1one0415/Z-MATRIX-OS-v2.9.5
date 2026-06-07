# Z-SkillOS Capability Invocation OS Runtime Implementation Planning Merge Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_IMPLEMENTATION_PLANNING_MERGE_RISK_REGISTER_READY
R1:Docs→runtime S:Critical M:PLAN_ONLY C:Runtime gate R:Runtime code
R2:Registry→exec S:Medium M:FUTURE_ONLY C:Registry gate R:Executable
R3:Router→code S:Critical M:FUTURE_ONLY C:Router gate R:Router code
R4:Engine→code S:Critical M:FUTURE_ONLY C:Engine gate R:Engine code
R5:T5 bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R6:Evidence mutation S:Medium M:Immutability C:Evidence CI R:Mutation
R7:Production coupling S:Critical M:Forbidden C:No-production CI R:Production ref
R8:Adapter→code S:Critical M:Separate gate C:Adapter approval R:Adapter code
R9:No seal S:Medium M:Mandatory C:Merge gate R:Merge no seal
R10:Level 5 drift S:Medium M:BLOCKED C:CI grep R:Level 5 language
