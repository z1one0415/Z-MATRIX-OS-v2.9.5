<!-- allowlist: forbidden-token-definition -->
# 账户风险周报 — Account Risk Weekly
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| account_id | str | ✅ | 账户 ID |
| report_week | str | ✅ | 报告周 |
| total_nav | float | ✅ | 总净值 |
| weekly_pnl | float | ✅ | 周盈亏 |
| var_95 | float | ✅ | VaR 95% |
| cvar_95 | float | ✅ | CVaR 95% |
| leverage | float | ✅ | 杠杆率 |
| margin_used_pct | float | ✅ | 保证金使用率 |
| max_drawdown_wtd | float | ✅ | 年内最大回撤 |
| stress_test_worst_case | float | ✅ | 压力测试最差情况 |
| liquidity_coverage | float | ✅ | 流动性覆盖率 |
| capital_curve_slope | float | ✅ | 资本曲线斜率 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| var_breach | {{ risk_var }} | |
| margin_call_risk | {{ risk_margin }} | |
| drawdown_limit_approaching | {{ risk_drawdown }} | |
| leverage_limit | {{ risk_leverage }} | |
| tail_risk_event | {{ risk_tail }} | |
| counterparty_exposure | {{ risk_counterparty }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY RISK REPORT — NO TRADING RECOMMENDATION
Risk metrics are paper-simulated. Real account risk will differ.
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
