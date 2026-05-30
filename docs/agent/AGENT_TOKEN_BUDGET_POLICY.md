# Agent Token Budget Policy

## Per-Command Limits
- max_input_tokens per command
- max_context_items per skill
- Default limit <= 100 per query

## Enforcement
- estimate_tokens(text) → int
- enforce_token_budget(payload, budget) → dict
- Over budget → NEED_NARROWER_QUERY
- Full scan forbidden by default

## Purpose
Prevent token explosion from agents requesting full-context scans.
Force agents to request targeted, minimal context slices.
