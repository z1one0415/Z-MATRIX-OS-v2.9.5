<!-- allowlist: forbidden-token-definition -->
# 错失机会复盘 — Missed Opportunity Postmortem
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| opportunity_id | str | ✅ | 机会 ID |
| ticker | str | ✅ | 股票代码 |
| detection_date | str | ✅ | 发现日期 |
| signal_source | str | ✅ | 信号来源 |
| signal_strength | float | ✅ | 信号强度 |
| entry_price_available | float | ✅ | 可入场价格 |
| exit_price_actual | float | ✅ | 实际离场价格 |
| opportunity_return_pct | float | ✅ | 机会收益率 |
| missed_reason | str | ✅ | 错失原因 |
| decision_chain | list | ✅ | 决策链回顾 |
| detection_lag_days | int | ✅ | 发现滞后天数 |
| false_dismissal_flag | bool | ✅ | 错误驳回标志 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| pattern_repeat_risk | {{ risk_pattern }} | |
| signal_decay | {{ risk_signal_decay }} | |
| coverage_gap | {{ risk_coverage }} | |
| decision_latency | {{ risk_latency }} | |
| confirmation_bias | {{ risk_bias }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY POSTMORTEM — NO TRADING RECOMMENDATION
Opportunity analysis is retrospective only. No forward-looking trade advice.
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
