# Pipeline Census v1.0

Pipeline Census 不是运行时调度器。它只是资产清点、状态标记、架构对齐工具。

状态定义：
- ACTIVE: actively used and architecture-registered
- LEGACY: old pipeline retained for compatibility
- STUB: placeholder or incomplete pipeline
- DEPRECATED: should not be used for new work
- UNKNOWN: exists but not yet classified

任何 UNKNOWN pipeline 不得自动进入 runtime。
