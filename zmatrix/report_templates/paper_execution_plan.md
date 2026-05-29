# 纸面执行计划 — Paper Execution Plan
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| plan_id | str | ✅ | 计划 ID |
| target_ticker | str | ✅ | 目标股票 |
| action_type | str | ✅ | 动作类型 (PAPER_ONLY_OBSERVE/PAPER_SIMULATE) |
| target_quantity | int | ✅ | 目标数量 |
| target_price | float | ✅ | 目标价格 |
| order_type | str | ✅ | 订单类型 |
| execution_window | str | ✅ | 执行窗口 |
| vwap_benchmark | float | | VWAP 基准 |
| slippage_estimate_bps | float | ✅ | 预估滑点 (bps) |
| cost_estimate | float | ✅ | 预估成本 |
| fill_probability | float | ✅ | 成交概率 |
| limit_board_status | str | ✅ | 涨跌停状态 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| limit_board_block | {{ risk_limit_board }} | |
| liquidity_insufficient | {{ risk_liquidity }} | |
| price_impact | {{ risk_price_impact }} | |
| execution_timing | {{ risk_timing }} | |
| counter_party_risk | {{ risk_counterparty }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY EXECUTION PLAN — NO REAL ORDERS
This execution plan is a paper simulation. No broker orders are placed.
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
