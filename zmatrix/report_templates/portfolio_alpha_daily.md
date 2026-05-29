# 组合 Alpha 日报 — Portfolio Alpha Daily
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| portfolio_id | str | ✅ | 组合 ID |
| report_date | str | ✅ | 报告日期 |
| daily_pnl | float | ✅ | 日盈亏 |
| daily_return_pct | float | ✅ | 日收益率 |
| cumulative_return | float | ✅ | 累计收益 |
| benchmark_return | float | ✅ | 基准收益 |
| daily_alpha | float | ✅ | 日 Alpha |
| tracking_error | float | ✅ | 跟踪误差 |
| top_contributors | list | ✅ | 最大贡献者 |
| top_detractors | list | ✅ | 最大拖累者 |
| sector_pnl_breakdown | dict | ✅ | 板块盈亏分解 |
| net_exposure | float | ✅ | 净暴露 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| drawdown_alert | {{ risk_drawdown }} | |
| concentration_breach | {{ risk_concentration }} | |
| tracking_error_spike | {{ risk_te }} | |
| turnover_surge | {{ risk_turnover }} | |
| style_drift | {{ risk_drift }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY PERFORMANCE REPORT — NO TRADING RECOMMENDATION
Alpha metrics are paper-trading simulated. Actual results will differ.
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
