# Skill Invocation Contract

## Input
invoke_skill(command_envelope, context_slice)

## Output Structure
```json
{
  "skill_id": "...",
  "status": "DRAFT_CREATED | ...",
  "output_ref": "...",
  "evidence_refs": [],
  "quality_status": "PARTIAL | ...",
  "blocked_reason": null,
  "human_review_required": true,
  "production_allowed": false
}
```

## Hard Rules
- SkillResult must be structured
- NO BUY / SELL / AUTO_EXECUTE in output
- NO READY_FOR_PRODUCTION in output
- Must not bypass ProposalLedger
