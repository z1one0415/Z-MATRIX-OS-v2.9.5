# CalibrationEvent Preview Contract v1.0 — Preview Only, No Auto Apply

## Fields

calibration_event_id, calibration_version, memory_candidate_id, target_domain, proposed_change, status, auto_apply_allowed, auto_calibration_allowed, requires_human_approval, created_at

## Safety

- Preview only
- auto_apply_allowed MUST be False
- auto_calibration_allowed MUST be False
- requires_human_approval MUST be True
- No Hermes memory write
- No real Z9 write
- No real trade

## Hard Rules

- CalibrationEvent is NOT parameter change
- MemoryCandidate is NOT ApprovedHeuristic
- PromptPatchPreview is NOT prompt injection
