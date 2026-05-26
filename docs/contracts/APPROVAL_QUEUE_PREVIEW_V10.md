# Approval Queue Preview Contract v1.0

## Fields

queue_version, pending_count, requests, auto_process_allowed, requires_human_review

## Sorting Rules

HIGH severity first
CalibrationEvent > PromptPatch > MemoryCandidate
REQUEST_MORE_EVIDENCE stays pending

## Safety

- Preview only
- No auto processing
- No Hermes memory write
- No real Z9 write
