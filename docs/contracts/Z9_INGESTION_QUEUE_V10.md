# Z9 Ingestion Queue v1.0 — Contract Freeze

## Input
- Z9_CALIBRATION_SAMPLE v1.0

## Output
- queue_version: v1.0
- queue_type: Z9_INGESTION_QUEUE_ITEM
- idempotency: sha256(sample_id+ticker+version+record_ref)[:32], dedup=ticker_sample_id
- state: PENDING_REVIEW | WAITING_MARKET_DATA | READY_FOR_REVIEW | REJECTED
- write_policy: queue_write_allowed=False, z9_write_allowed=False
- forbidden_real_trade_checked: True

## Rules

### 状态机
- REJECTED: 当 sample_id/ticker/source_record 任一缺失
- WAITING_MARKET_DATA: 当 outcome_placeholder.review_status == "WAITING_FOR_FUTURE_MARKET_DATA"
- PENDING_REVIEW: 其余有效样本
- READY_FOR_REVIEW: 保留给 D-3/D-4 outcome workflow，表示 T+N 数据已到齐

### source_record_ref
- 必须从 sample.source_record.record_ref 显式读取
- 不允许使用可能读不到嵌套字段的泛型 _get()
- 写入到 idempotency.source_record_ref

### idempotency_key
- 基于 sample_id + ticker + sample_version + source_record.record_ref 的 sha256[:32]
- 必须随 source_record.record_ref 变化而变化
- 禁止使用伪值（如 "abc123"）

### Write Policy
- queue_write_allowed: 始终为 False（D-2 只预览队列项，不写真实队列）
- z9_write_allowed: 始终为 False（D-2 不写真实 Z9）
- 即使 ready_for_real_ingestion 未来变为 true，D-2 阶段也不允许真实 write

### 禁止交易
- 任何 action 字段（entry_intent/exit_intent/paper_action/action_cap）不得包含 BUY/SELL/ADD/CLEAR/AUTO_TRADE/MARKET_ORDER/BROKER_ORDER/REAL_TRADE

### D-2 范围
- D-2 只创建 queue preview 对象，不做任何 database write
- D-2 只验证契约合规性
- D-3 可能定义真实 outcome backfill
- D-4 可能定义参数自适应校准

## 测试
- test_z9_ingestion_queue_contract.py: 所有字段/状态/idempotency/禁止交易测试
- test_g18_output_contains_queue_preview: G18 天机引擎集成验证
