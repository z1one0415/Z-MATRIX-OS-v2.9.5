# Agent Token Budget Policy

## Per-Command Limits
max_input_tokens per command | max_context_items per skill | Default limit <= 100

## Enforcement
estimate_tokens(text) → int | enforce_token_budget(payload, budget) → dict | Over budget → NEED_NARROWER_QUERY

## Purpose
Prevent token explosion. Force agents to request targeted, minimal context slices.
