# Agent Tamper Protection Policy

## Scanned Patterns
Forbidden production flags, dangerous calls, and secret patterns

## Rules
- Tamper guard violation → BLOCK | Self-elevation → BLOCK
- Secret pattern detected → REDACT + BLOCK | Workspace escape → BLOCK
