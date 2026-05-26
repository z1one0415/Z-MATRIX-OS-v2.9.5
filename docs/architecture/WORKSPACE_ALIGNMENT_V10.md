# Workspace Alignment v1.0

v2.9.10-dev 目标：不是新增投资能力，而是资产归位。

范围：
- data/ 本地数据目录
- pipeline census
- Hermes adapter inventory
- script index
- research asset policy

不做：
- 不重构 pipeline
- 不重构 Hermes
- 不导入 Obsidian 全文
- 不接真实交易
- 不做 EventStore
- 不做 Prompt Hot-Patching

Hermes boundary:
v2.9.10-dev only indexes Hermes adapters.
It must not modify hermes memory content, memory_bank.json, calibration state, or long-term memory files.
Any Hermes memory write must wait for EventStore + Approval-Required Reflection Loop.
