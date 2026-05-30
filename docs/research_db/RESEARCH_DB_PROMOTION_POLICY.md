# ResearchDB Promotion Policy

## Promotion Path

```
RAW_DATA
→ FORMAT_VALIDATED
→ SOURCE_VALIDATED
→ CROSS_SOURCE_VALIDATED
→ OUTCOME_VALIDATED
→ RESEARCH_ACCEPTED
→ PAPER_RULE_CANDIDATE
```

## Case-to-Rule Progression

| Evidence | Outcome |
|------|------|
| 1 case | LESSON_ONLY |
| 3 similar cases | RULE_CANDIDATE |
| 10 cross-ticker cases | RESEARCH_RULE |
| 20 cross-ticker + cross-regime | PAPER_RULE |
| Any case | PRODUCTION_ALLOWED=false |

## Forbidden

- RAW_DATA must not enter OUTCOME_VALIDATED directly.
- Single case must not enter RESEARCH_ACCEPTED.
- RESEARCH_ACCEPTED must not enter production.
- PAPER_RULE_CANDIDATE must not auto-promote to production.
