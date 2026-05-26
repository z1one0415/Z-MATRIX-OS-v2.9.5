# v3.0-alpha Dry-Run Rehearsal Architecture v1.0

## Goal

End-to-end dry-run rehearsal of v2.9.10~v2.9.16 modules.

## Chain

PaperLedgerEvent → OutcomeBackfillEvent → MemoryCandidatePreview → ApprovalRequest → HumanApprovalDecision → PromptPatchRequest → PromptRenderPreview → TailRiskControllerPreview → V3AlphaReadinessReport

## Not In Scope

- No real trade
- No Hermes memory write
- No Z9 write
- No prompt injection
- No runtime enable
- No broker connection
