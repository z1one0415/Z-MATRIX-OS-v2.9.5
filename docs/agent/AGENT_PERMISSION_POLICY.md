# Agent Permission Policy

## Risk Levels
- R0_READ: read-only access
- R1_ANNOTATE: annotation writes
- R2_DRAFT: draft creation
- R3_WRITE_RESEARCH_DB: ResearchDB writes (requires human review)
- R4_CODE_PATCH_PROPOSAL: code patch proposal (requires human approval)
- R5_RELEASE_PROPOSAL: release proposal (requires human approval)
- R9_FORBIDDEN: always blocked

## Permission Rules
- VIEW_ONLY agent calling R3 → REJECT
- R3+ requires human review
- R4/R5 requires human approval
- R9 always blocked
