# Agent Registry Policy

## Rules
- Every agent must be registered before use
- unknown agent → REJECT | disabled agent → REJECT
- production_allowed=true → ERROR | allowed_scopes=["*"] → ERROR
- requires_human_review=false with risk_level>=R3 → ERROR

## Risk Levels
R0_READ | R1_ANNOTATE | R2_DRAFT | R3_WRITE_RESEARCH_DB | R4_CODE_PATCH_PROPOSAL | R5_RELEASE_PROPOSAL | R9_FORBIDDEN

## Agent Types
ORCHESTRATOR | ENGINEERING | RESEARCH | REPORT_RENDERER | FRONTEND_ASSISTANT | MAINTENANCE
