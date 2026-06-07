# Runtime P0 Review Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_DISABLED_DEFAULT_P0_REVIEW_RISK_REGISTER_READY
R1:Config→enabled S:Critical M:strict bool C:Config CI R:Non-bool enable
R2:Env→enable S:High M:env_override_detected C:Env CI R:Env enable
R3:Non-bool→enable S:Critical M:is True C:Guard CI R:Non-bool
R4:Registry→import S:Critical M:No imports C:Static analysis R:Dynamic import
R5:Router→execution S:Critical M:DENY default C:Router CI R:Execution
R6:Composition→chain S:Critical M:DENY multi C:Composition CI R:Chain exec
R7:Evidence→files S:Medium M:NoopSink C:Side-effect CI R:File write
R8:Guard→blocking S:Critical M:CONTINUE C:Guard CI R:BLOCKED action
R9:T5→granted S:Critical M:NEVER_GRANTED C:Tier CI R:T5 invocation
R10:Adapter→impl S:Critical M:Mapping only C:Adapter gate R:Adapter code
R11:ZMATRIX→imports S:Critical M:Forbidden C:AST scan R:Z2/Z8/Z9 import
R12:Production→link S:Critical M:Forbidden C:No-production CI R:Production ref
R13:Envelope→mutation S:Critical M:No mutation C:Envelope CI R:Mutation
R14:Level5→drift S:Medium M:BLOCKED C:CI grep R:Level5 language
