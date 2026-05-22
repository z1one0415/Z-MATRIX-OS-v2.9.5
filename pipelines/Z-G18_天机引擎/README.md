# ☯️ Z-G18 天机引擎

**当前状态**: merge-review candidate / experimental-light / not RC

## 边界声明
- 不输出 BUY/SELL/AUTO_TRADE/MARKET_ORDER
- 不直接写 Z9，只输出 prediction sample ready
- 不连接 M1/L2
- 不允许 auto_adjust_weights
- auto_adjust_allowed 恒为 False
- 当前可合入 feature review，不代表 RC

## 不变量
- INV-TG18-01 Sigmoid Shield
- INV-TG18-02 Data Lineage Cap
- INV-TG18-03 Temporal Action Gate
- INV-TG18-04 Auto-Weight Freeze
- INV-TG18-05 No Trade Action
- INV-TG18-06 Proxy Cannot Become PASS
- INV-TG18-07 Missing Lineage Is Degraded
- INV-TG18-08 Trigger Eligibility Is Not Execution

## Related gateway changes
本分支包含最小必要外溢补丁：
- Z-G01: 新增 fetch_overseas_assets() (海外资产统一入口)
- z17_loader: 导出 fetch_overseas_assets()
- Z-G02: 使用 fetch_overseas_assets() 作为隔夜资产统一入口

这些改动只用于支持 Z-G02/Z-G18 的统一数据入口，不改变任何交易动作权限。
