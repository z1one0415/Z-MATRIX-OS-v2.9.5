# Runtime P1 Review Risk Register
## Status: Z_SKILLOS_CAPABILITY_INVOCATION_OS_RUNTIME_P1_REVIEW_RISK_REGISTER_READY
R1:Config S:Critical L:VeryLow M:Hardcoded False C:Config CI R:True enabled
R2:KillSwitch S:Critical L:VeryLow M:overrides_requested C:Kill switch CI R:Bypass
R3:Adapter S:Critical L:VeryLow M:FORBIDDEN_MODULES C:AST scan R:Z2 import
R4:Execution S:Critical L:VeryLow M:DENY defaults C:Router CI R:Execution call
R5:T5 S:Critical L:VeryLow M:NEVER_GRANTED C:Tier CI R:T5 invocation
R6:Evidence S:Medium L:Low M:Noop Sink C:Side-effect CI R:File write
R7:Blocking S:Critical L:VeryLow M:CONTINUE/DEGRADE C:Guard CI R:BLOCKED
R8:Production S:Critical L:VeryLow M:FORBIDDEN_MODULES C:No-production CI R:Production ref
R9:Skip S:Low L:Low M:Documented+unblock C:Unskip gate R:Blind skip
R10:DocThin S:Low L:Low M:All expanded C:Review check R:Missing fields
R11:NoSeal S:Medium L:Low M:Mandatory C:Merge gate R:Merge without seal
R12:Level5Drift S:Medium L:Low M:BLOCKED everywhere C:CI grep R:Level5 language
