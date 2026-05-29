<!-- allowlist: forbidden-token-definition -->
# 执行路由竞争 — Execution Route Competition
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| route_id | str | ✅ | 路由 ID |
| ticker | str | ✅ | 股票代码 |
| competing_routes | list | ✅ | 竞争路由列表 |
| best_route | str | ✅ | 最优路由 |
| route_scores | dict | ✅ | 各路由得分 |
| latency_ms | float | ✅ | 延迟 (ms) |
| fill_rate | float | ✅ | 成交率 |
| cost_bps | float | ✅ | 成本 (bps) |
| reject_rate | float | | 拒单率 |
| route_stability | float | ✅ | 路由稳定性 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| route_concentration | {{ risk_route_conc }} | |
| latency_spike | {{ risk_latency }} | |
| fill_degradation | {{ risk_fill }} | |
| exchange_outage | {{ risk_outage }} | |
| cost_anomaly | {{ risk_cost_anomaly }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY ROUTE ANALYSIS — NO TRADING RECOMMENDATION
Route competition results are simulated. No real orders are routed.
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
