# Agent Frontend Action Queue Policy

## Action Types
OPEN_CASE | FOCUS_TICKER | SHOW_EVENT_WINDOW | SHOW_FACTOR_REPORT
SHOW_HYPOTHESIS | SHOW_ANALYSIS_ZONE | ASK_HUMAN_REVIEW
SHOW_AGENT_PROPOSAL | SHOW_VERIFY_RESULT | SHOW_DATA_QUALITY_WARNING
REQUEST_USER_DECISION

## Hard Rules
- Action Queue only controls frontend display
- Must not mutate ResearchDB
- Must not trigger trades
- Must not auto-approve
- Destructive pop allowed after read
