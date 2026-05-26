# Event Schema v1.0

## Base Event Fields

```
event_id            32-char hex (deterministic)
event_type          one of 13 EVENT_TYPES
schema_version      EVENT_STORE_V10
created_at          ISO-8601 UTC
producer_module     fully qualified module name
source_event_id     optional 32-char hex source reference
parent_event_id     optional 32-char hex parent reference
input_hash          64-char sha256 of canonical payload
output_hash         64-char sha256 of event metadata
payload             dict (event-specific)
safety              dict (DEFAULT_EVENT_SAFETY)
```

## Event Types (13)

```
ResearchEvent
CandidateReviewEvent
RoleClassificationEvent
PaperDecisionEvent
PaperLedgerEvent
OutcomeBackfillEvent
RiskEvent
HumanDiaryEvent
MistakeAttributionEvent
MemoryCandidateEvent
CalibrationEvent
HumanApprovalEvent
PromptPatchEvent
```

## Safety Defaults

All safety fields default to False except local_event_write_allowed=True.

## Safety Boundaries

- MemoryCandidateEvent/CalibrationEvent/PromptPatchEvent may enter EventStore
- They must NOT auto-write Hermes long-term memory
- They must NOT auto-inject prompts
- They must NOT auto-change strategy
