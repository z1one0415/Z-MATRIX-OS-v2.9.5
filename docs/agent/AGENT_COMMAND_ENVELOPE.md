# Agent Command Envelope Policy

## Required Fields
command_id (unique) | agent_id | command_type | requested_skill | input_refs | target_layers | requested_action | risk_level | idempotency_key | dry_run | requires_human_review | production_allowed (must be false)

## Validation
- command_id must be unique | agent_id must be registered | requested_skill must be registered
- target_layers must be valid | production_allowed must be false | R9_FORBIDDEN → direct REJECT
