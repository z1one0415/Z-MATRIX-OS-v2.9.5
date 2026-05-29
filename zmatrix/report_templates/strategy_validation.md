<!-- allowlist: forbidden-token-definition -->
# 策略验证 — Strategy Validation
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| strategy_id | str | ✅ | 策略 ID |
| strategy_name | str | ✅ | 策略名称 |
| validation_window | str | ✅ | 验证窗口 |
| is_paper_mode | bool | ✅ | 纸面模式? |
| signal_count | int | ✅ | 信号数量 |
| win_rate | float | ✅ | 胜率 |
| sharpe_ratio | float | ✅ | 夏普比率 |
| max_drawdown | float | ✅ | 最大回撤 |
| annual_return | float | ✅ | 年化收益 |
| benchmark_return | float | ✅ | 基准收益 |
| alpha | float | ✅ | Alpha |
| beta | float | ✅ | Beta |
| information_ratio | float | ✅ | 信息比率 |
| turnover_rate | float | | 换手率 |
| capacity_estimate | float | | 容量估计 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| overfitting_risk | {{ risk_overfitting }} | |
| lookahead_bias | {{ risk_lookahead }} | |
| survivorship_bias | {{ risk_survivorship }} | |
| transaction_cost_impact | {{ risk_tcost }} | |
| regime_dependence | {{ risk_regime }} | |
| capacity_limit | {{ risk_capacity }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY STRATEGY VALIDATION — NO TRADING RECOMMENDATION
Strategy metrics are backtest-simulated. Real execution will differ.
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
