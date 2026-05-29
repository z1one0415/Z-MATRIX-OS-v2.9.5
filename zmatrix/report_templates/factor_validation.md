# 因子验证 — Factor Validation
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| factor_id | str | ✅ | 因子 ID |
| factor_name | str | ✅ | 因子名称 |
| factor_category | str | ✅ | 因子类别 |
| ic_mean | float | ✅ | IC 均值 |
| ic_ir | float | ✅ | IC_IR |
| rank_ic | float | ✅ | Rank IC |
| turnover | float | | 因子换手率 |
| horizon_ready | bool | ✅ | 样本量充足? |
| sample_count | int | ✅ | 样本数量 |
| stability_score | float | ✅ | 稳定性得分 |
| robustness_score | float | ✅ | 鲁棒性得分 |
| promotion_eligible | bool | ✅ | 可晋升? |
| production_allowed | bool | ✅ | 可用于生产? |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| data_mining_bias | {{ risk_data_mining }} | |
| horizon_insufficient | {{ risk_horizon }} | |
| factor_decay | {{ risk_decay }} | |
| collinearity | {{ risk_collinearity }} | |
| regime_instability | {{ risk_instability }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY FACTOR VALIDATION — NO TRADING RECOMMENDATION
Factor metrics are research artifacts. Real trading requires additional gates.
```

## Audit Trail
| Item | Value |
|------|-------|
| template_version | V4.0-C3 |
| render_timestamp | {{ timestamp }} |
| pipeline_id | {{ pipeline_id }} |
| run_id | {{ run_id }} |
| input_hash | {{ input_hash }} |
| output_hash | {{ output_hash }} |
| audit_event_id | {{ audit_event_id }} |
| safety_gate_passed | {{ safety_gate_passed }} |
