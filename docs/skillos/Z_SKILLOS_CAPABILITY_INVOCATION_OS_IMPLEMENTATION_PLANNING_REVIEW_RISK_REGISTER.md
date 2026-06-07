# Z-SkillOS Capability Invocation OS Implementation Planning Review Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_IMPLEMENTATION_PLANNING_REVIEW_RISK_REGISTER_READY
R1:Planning→runtime S:Critical L:Medium M:All docs PLAN_ONLY C:Implementation gate R:Code without gate
R2:Adapter→code S:Critical L:Medium M:Separate adapter gate C:Wave-level approval R:Adapter code
R3:Registry executable S:Medium L:Low M:No execution path C:Registry gate R:Executable registry
R4:Router runtime S:Critical L:Low M:FUTURE_PLAN_ONLY C:Router gate R:Router code
R5:Engine code S:Critical L:Low M:FUTURE_PLAN_ONLY C:Engine gate R:Engine code
R6:Guard code S:Critical L:Low M:FUTURE_PLAN_ONLY C:Guard gate R:Guard code
R7:T5 unblocked S:Critical L:VeryLow M:NEVER_GRANTED C:Tier model CI R:T5 invocation
R8:Evidence writable S:Medium L:Low M:Immutability rule C:Evidence CI R:Evidence mutation
R9:Production coupling S:Critical L:VeryLow M:All docs forbid C:No-production CI R:Production ref
R10:Warning lineage S:Medium L:Low M:No warning enablement C:Warning gate R:Warning enabled
R11:Merge no seal S:Medium L:Low M:Seal mandatory C:Merge gate closure R:Merge without seal
R12:Level 5 drift S:Medium L:Low M:Level 5 BLOCKED C:CI grep R:Level 5 language
