# Skill Invocation Contract

## Input
invoke_skill(command_envelope, context_slice) → SkillResultEnvelope

## Output
{skill_id, status, output_ref, evidence_refs, quality_status, blocked_reason, human_review_required, production_allowed}

## Hard Rules
- SkillResult must be structured
- NO BUY / SELL / AUTO_EXECUTE in output
- NO READY_FOR_PRODUCTION in output
- Must not bypass ProposalLedger
