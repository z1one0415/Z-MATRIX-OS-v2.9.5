# Agent Registry Policy

## Rules
- Every agent must be registered before use
- Agent ID must be unique
- unknown agent → REJECT
- disabled agent → REJECT
- production_allowed=true → ERROR
- allowed_scopes=["*"] → ERROR
- requires_human_review=false with risk_level>=R3 → ERROR

## Registry Fields
- agent_id, agent_name, agent_type, permission_level
- allowed_scopes, allowed_read_layers, allowed_write_layers
- allowed_commands, forbidden_commands
- max_risk_level, requires_human_review
- workspace_path, enabled, production_allowed
