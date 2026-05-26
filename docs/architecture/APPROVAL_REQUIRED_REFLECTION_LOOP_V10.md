# Approval-Required Reflection Loop Architecture v1.0

## Goal

Integrate Hermes Memory Kernel preview output with human approval queue.

## Chain

```
MemoryCandidatePreview
→ ApprovalRequest (PENDING_REVIEW)
→ HumanApprovalDecision (APPROVE/REJECT/QUARANTINE/REQUEST_MORE_EVIDENCE)
→ HumanApprovalEvent → EventStore
```

## Not In Scope

- No Hermes long-term memory write
- No memory_bank.json write
- No auto calibration
- No auto prompt injection
- No real trade
- No B/R/D / Z8 / G18 / Account Constitution modification

## Architecture

Approval Loop is the safety gate for v3.0 self-evolution.
MemoryCandidate / CalibrationEvent / PromptPatch only enter the
"write candidate" zone after human approval — in a future version.
This version does NOT execute writes.

## Event Chain

```
MemoryCandidatePreview / CalibrationEventPreview / PromptPatchPreview
→ ApprovalRequest (PENDING_REVIEW)
→ ApprovalRequestEvent (EventStore)
→ HumanApprovalDecision (APPROVE/REJECT/QUARANTINE/REQUEST_MORE_EVIDENCE)
→ HumanApprovalEvent (EventStore)
→ EventStore

ApprovalRequestEvent is NOT approval.
HumanApprovalEvent is NOT automatic execution.
```
