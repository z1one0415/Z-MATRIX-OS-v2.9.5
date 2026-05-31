# Expert Domain Contract

## Reviewer Skill Output
reviewer_id | target_ref | verdict | confidence | risk_flags | missing_evidence | reason_short

## Verdict Enum
PASS | WATCH | BLOCK | DATA_INSUFFICIENT | CONFLICTED | NEEDS_HUMAN_REVIEW

## Hard Rules
- Reviewer Skill must not output trade actions
- Reviewer Skill must not write to ResearchDB
- Reviewer Skill only generates review conclusions
- production_allowed must be false
