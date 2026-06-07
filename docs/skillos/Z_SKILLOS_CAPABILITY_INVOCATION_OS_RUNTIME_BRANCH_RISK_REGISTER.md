# Risk | Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_BRANCH_RISK_REGISTER_READY
R1:Skeleton→execution S:Critical M:disabled-default C:Runtime gate R:Execution code
R2:Adapter→import S:Critical M:No imports C:Adapter gate R:Z2/Z8/Z9 import
R3:Config→enabled S:Critical M:strict bool C:Config CI R:Non-bool enable
R4:T5 bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R5:Side-effects S:Medium M:NoopEvidence Sink C:Side-effect CI R:File write
R6:Production link S:Critical M:Forbidden C:No-production CI R:Production ref
R7:Warning enable S:Medium M:No warning C:Warning gate R:Warning enabled
R8:Merge no seal S:Medium M:Mandatory C:Merge gate R:Merge without seal
R9:Level 5 drift S:Medium M:BLOCKED C:CI grep R:Level 5 language
R10:Test overfit S:Low M:Behavioral test C:P1 test review R:False pass
