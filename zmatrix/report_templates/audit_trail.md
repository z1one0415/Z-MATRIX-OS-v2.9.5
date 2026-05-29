<!-- allowlist: forbidden-token-definition -->
# 审计追踪 — Audit Trail
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| audit_id | str | ✅ | 审计 ID |
| audit_scope | str | ✅ | 审计范围 |
| audited_pipelines | list | ✅ | 被审计管线 |
| event_count | int | ✅ | 事件数量 |
| date_range | str | ✅ | 日期范围 |
| compliance_status | str | ✅ | 合规状态 |
| safety_violations | int | ✅ | 安全违规数 |
| data_integrity_score | float | ✅ | 数据完整性得分 |
| chain_of_custody_verified | bool | ✅ | 监管链验证 |
| tamper_evidence | list | | 篡改证据 |
| forbidden_output_hits | list | | 禁止输出命中 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| safety_gate_bypass | {{ risk_bypass }} | |
| chain_of_custody_break | {{ risk_custody }} | |
| forbidden_token_leak | {{ risk_token_leak }} | |
| event_store_integrity | {{ risk_event_store }} | |
| timestamp_anomaly | {{ risk_timestamp }} | |
| audit_log_gap | {{ risk_log_gap }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY AUDIT TRAIL — NO TRADING RECOMMENDATION
This audit trail documents simulated system events. No real trades are recorded.
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
