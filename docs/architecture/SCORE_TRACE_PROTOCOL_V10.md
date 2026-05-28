# ZC00 SCORE TRACE PROTOCOL V10

## Schema
```json
{
  "trace_version": "SCORE_TRACE_V10",
  "factor_id": "b_roe",
  "input_facts": {"roe": 15.2, "industry_p25": 8, "industry_p75": 22},
  "normalized_value": 0.514,
  "formula": "min(100, max(0, (v-p25)/(p75-p25)*100))",
  "intermediate_values": {"v": 15.2, "p25": 8, "p75": 22},
  "final_score": 51.4,
  "timestamp": "2026-05-29T03:20:00Z"
}
```

## Requirements
- Every factor score must produce a ScoreTrace
- ScoreTrace must be serializable to JSON
- ScoreTrace must contain ALL intermediate values
- Missing input facts must be recorded as None with reason
