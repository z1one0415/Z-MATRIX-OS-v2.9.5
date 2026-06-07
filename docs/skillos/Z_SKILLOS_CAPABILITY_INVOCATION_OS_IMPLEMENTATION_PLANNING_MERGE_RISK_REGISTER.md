# Z-SkillOS Capability Invocation OS Implementation Planning Merge Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_IMPLEMENTATION_PLANNING_MERGE_RISK_REGISTER_READY
R1:Docs→runtime S:Critical M:PLAN_ONLY label C:Impl gate R:Runtime code
R2:Adapter→code S:Critical M:Separate gate C:Wave approval R:Adapter code
R3:Registry exec S:Medium M:No exec path C:Registry gate R:Executable
R4:Router runtime S:Critical M:FUTURE_PLAN_ONLY C:Router gate R:Router code
R5:Engine code S:Critical M:FUTURE_PLAN_ONLY C:Engine gate R:Engine code
R6:T5 bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R7:Evidence mutation S:Medium M:Immutability C:Evidence CI R:Mutation
R8:Production S:Critical M:Forbidden C:No-production CI R:Production ref
R9:No seal S:Medium M:Mandatory C:Merge gate R:Merge no seal
R10:Level 5 drift S:Medium M:BLOCKED C:CI grep R:Level 5 lang
