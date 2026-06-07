# Runtime P0 Merge Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_DISABLED_DEFAULT_P0_MERGE_RISK_REGISTER_READY
R1:Skeleton→enabled S:Critical M:disabled-default C:Config gate R:Enablement
R2:Merge→execution S:Critical M:Merge review only C:Execution gate R:Execution
R3:Adapter→impl S:Critical M:Mapping only C:Adapter gate R:Adapter code
R4:Imports→later S:Critical M:Forbidden now C:AST scan R:ZMATRIX import
R5:Evidence→files S:Medium M:NoopSink C:Side-effect CI R:File write
R6:Router→execution S:Critical M:DENY C:Router CI R:Execution
R7:T5→bypass S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R8:Test→overtrust S:Low M:Behavioral test C:P1 proof R:False pass
R9:No seal S:Medium M:Mandatory C:Merge gate R:Merge no seal
R10:Level5→drift S:Medium M:BLOCKED C:CI grep R:Level5 language
