<!-- allowlist: forbidden-token-definition -->
# 证据数据质量 — Evidence Data Quality
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| evidence_id | str | ✅ | 证据 ID |
| source | str | ✅ | 数据来源 |
| pit_status | str | ✅ | PIT 状态 (PIT_CLEAN/PIT_BLOCKED/PIT_DIRTY) |
| freshness_days | int | ✅ | 数据新鲜度 (天) |
| completeness_pct | float | ✅ | 完整度 (%) |
| accuracy_confidence | float | ✅ | 准确度置信 |
| outlier_count | int | | 异常值数量 |
| missing_fields | list | | 缺失字段列表 |
| quality_score | float | ✅ | 综合质量得分 |
| usable_for_production | bool | ✅ | 可用于生产? |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| data_staleness | {{ risk_staleness }} | |
| source_reliability | {{ risk_source }} | |
| pit_violation | {{ risk_pit }} | |
| outlier_contamination | {{ risk_outlier }} | |
| completeness_gap | {{ risk_completeness }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY DATA QUALITY REPORT — NO TRADING RECOMMENDATION
Data quality assessment is for model validation only.
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
