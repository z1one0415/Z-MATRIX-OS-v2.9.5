# Hermes Adapter Registry v1.0

Hermes Adapter Registry 只是把 hermes/ 旧模块纳入架构索引。
本阶段不改变 hermes/ 内部逻辑。

所有 Hermes Adapter 默认 preview-only / read-only / inventory-only。
任何写入长期记忆、自动校准、Prompt 注入必须等后续 EventStore / Approval Loop 完成。
