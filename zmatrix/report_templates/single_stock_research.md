# 个股研究报告 — Single Stock Research
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**
**Ticker: {{ ticker }} | Name: {{ stock_name }}

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticker | str | ✅ | 股票代码 |
| stock_name | str | ✅ | 股票名称 |
| sector | str | ✅ | 所属板块 (SW) |
| b_score | float | ✅ | B-Matrix 得分 |
| d_score | float | ✅ | D-Matrix 得分 |
| r_score | float | ✅ | R-Matrix 得分 |
| roe | float | ✅ | 净资产收益率 |
| pe_ttm | float | ✅ | 市盈率 TTM |
| pb | float | ✅ | 市净率 |
| dividend_yield | float | | 股息率 |
| market_cap_bn | float | ✅ | 市值 (亿) |
| catalyst_chain | str | | 催化剂链 |
| thesis_status | str | | Thesis 状态 |
| evidence_layer | str | ✅ | 证据分层 (A/B/C/D) |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| financial_health_gate | {{ risk_financial_health }} | |
| valuation_risk | {{ risk_valuation }} | |
| sector_concentration | {{ risk_sector_concentration }} | |
| liquidity_risk | {{ risk_liquidity }} | |
| catalyst_decay | {{ risk_catalyst_decay }} | |
| evidence_gap | {{ risk_evidence_gap }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY RESEARCH REPORT — NO TRADING RECOMMENDATION
This report is for research purposes only. All positions are simulated.
No actual orders shall be placed based on this output.
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
