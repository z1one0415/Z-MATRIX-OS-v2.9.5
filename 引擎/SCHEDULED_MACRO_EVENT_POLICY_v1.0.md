# Scheduled Macro Event Policy v1.0

## Policy
- Scheduled events (FOMC, CPI, NFP, PMI, central_bank) ≠ blackswans
- Reduce interpretation weight, NOT global stop
- Event day: no new entry interpretation
- Post-48h: full evaluation resumes
- Blackswans: hard veto maintained

## Phase Rules
- pre_2d: reduce interpretation strength, no veto
- pre_1d: reduce interpretation strength, no veto
- event_day: no new entry, existing holding review allowed
- post_48h: full evaluation resumes
- blackswans: hard veto, paper_track_allowed=false, score_cap<=60

## Event Types
Scheduled: FOMC, CPI, NFP, PMI, central_bank_decision, policy_announcement
Blackswans: war, sanctions, default, trading_halt, policy_shock
