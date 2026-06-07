# Risk | Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_P1_BRANCH_RISK_REGISTER_READY
R1:P1→enablement S:Critical M:disabled-default C:Config gate R:Enablement
R2:Adapter→code S:Critical M:No imports C:Adapter gate R:Adapter code
R3:Execution→call S:Critical M:DENY default C:Execution gate R:Execution
R4:T5 bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R5:Side-effects S:Medium M:Noop/InMemory Sink C:Side-effect CI R:File write
R6:Production link S:Critical M:Forbidden C:No-production CI R:Production ref
R7:Test→overtrust S:Low M:Behavioral P1 tests C:P1 proof review R:False pass
R8:No seal S:Medium M:Mandatory C:Merge gate R:Merge without seal
R9:Level 5 drift S:Medium M:BLOCKED C:CI grep R:Level 5 language
