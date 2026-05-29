# 研究理事会审查 — Research Council Review
**Template: V4.0-HARDENING-C3 | Generated: {{ timestamp }}**

---

## Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| review_id | str | ✅ | 审查 ID |
| target_ticker | str | ✅ | 目标股票 |
| reviewers_panel | list | ✅ | 审查委员列表 (12 人) |
| reviewer_count | int | ✅ | 参与审查人数 |
| approval_count | int | ✅ | 通过人数 |
| reject_count | int | ✅ | 拒绝人数 |
| abstain_count | int | ✅ | 弃权人数 |
| consensus_score | float | ✅ | 共识得分 |
| dissenting_opinions | list | | 不同意见汇总 |
| final_verdict | str | ✅ | 最终裁定 (APPROVED/REJECTED/DEFERRED) |
| review_chain_of_custody | str | ✅ | 审查链 |

## Risk Assessment
| Risk Flag | Status | Detail |
|-----------|--------|--------|
| reviewer_quorum_met | {{ risk_quorum }} | |
| consensus_threshold | {{ risk_consensus }} | |
| conflict_of_interest | {{ risk_conflict }} | |
| data_sufficiency | {{ risk_data_sufficiency }} | |
| model_version_consistency | {{ risk_model_version }} | |

## Safety Declaration
```
real_trade_allowed: False
broker_order_allowed: False
production_allowed: False
human_review_required: True
⚠️ PAPER-ONLY REVIEW — NO TRADING AUTHORIZATION
This council review is a simulation. No real trading decisions are authorized.
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
