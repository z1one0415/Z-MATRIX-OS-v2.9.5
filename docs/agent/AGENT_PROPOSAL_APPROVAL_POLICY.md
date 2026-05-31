# Agent Proposal-Approval Policy

## Three-Phase Write
Agent must never write directly to core system: Proposal → Approval → Execution → Verify → Audit

## Proposal States
DRAFT → SUBMITTED → APPROVED / REJECTED / DEFERRED → EXECUTED → VERIFY_FAILED → CLOSED

## Hard Rules
- Append-only | proposal_id must be unique
- No execution before approval | R3+ must have approval
- R4/R5 must have human approval | R9 forbidden to approve
- dry_run failure blocks real run | execution requires verify
