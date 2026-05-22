# ☯️ Z-G18 天机引擎

**当前状态**: minimal prototype / not master-ready

## 不变量
- 不输出 BUY/SELL/AUTO_TRADE/MARKET_ORDER
- 不直接写 Z9，只输出 prediction sample ready
- 不连接 M1/L2
- 不允许 auto_adjust_weights
- auto_adjust_allowed 恒为 False

## 输出
- 多周期概率 (T1/T5/T20)
- 证据覆盖 + 数据血统
- 时间一致性 + next_triggers
- Z9 prediction_sample (ready, not written)
