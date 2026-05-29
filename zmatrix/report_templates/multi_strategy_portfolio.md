<!-- allowlist: forbidden-token-definition -->
# 多策略组合 — Multi-Strategy Portfolio
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| portfolio_id | str | ✅ | 组合 ID |
| strategy_count | int | ✅ | 策略数量 |
| position_count | int | ✅ | 持仓数量 |
| total_nav | float | ✅ | 总净值 |
| leverage_ratio | float | ✅ | 杠杆率 |
| sector_exposure | dict | ✅ | 板块暴露 |
| style_exposure | dict | ✅ | 风格暴露 |
| top_10_concentration | float | ✅ | 前 10 集中度 |
| correlation_matrix_avg | float | ✅ | 平均相关性 |
| diversification_score | float | ✅ | 分散化得分 |
| rebalance_frequency | str | ✅ | 再平衡频率 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| concentration_risk | {{ risk_concentration }} | |
| leverage_risk | {{ risk_leverage }} | |
| correlation_surprise | {{ risk_correlation }} | |
| liquidity_crunch | {{ risk_liquidity }} | |
| tail_risk_exposure | {{ risk_tail }} | |
| sector_overlap | {{ risk_sector_overlap }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY PORTFOLIO REPORT — NO TRADING RECOMMENDATION
Portfolio construction is simulated. Positions are not real.
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
