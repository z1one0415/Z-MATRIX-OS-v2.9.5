# ☯️ Z-MATRIX-OS Research OS V3 — 新会话启动提示词

## 一、系统定位

```
项目名称: Z-MATRIX-OS
当前版本: Research OS V3
架构状态: ARCHITECTURE_FREEZE (功能建设阶段已结束)
仓库: github.com/z1one0415/Z-MATRIX-OS-v2.9.5
分支: v4.0-batch-0-final-hardgates-scope-lock
RC1 Tag: v4.0-rc1 → f8796f7
```

## 二、当前工程状态

```
模块: 160个
包: 23个
测试: 1,224 全部通过
CI Workflows: 3 (researchdb-phase1, researchdb-phase2, v40-rc1-audit)
生产: BLOCKED
Broker/Runtime/RealTrade: BLOCKED
架构冻结: 已验收
```

## 三、系统架构（6层）

```
第6层 进化层: evolution (知识图谱/假设进化/模式挖掘/元研究)
第5层 运营层: ROL (注册/监控/工作流/记忆)
第4层 决策层: decision_intelligence (Thesis/Prediction/Decision/V2市场)
第3层 投资组合层: portfolio + portfolio_reality + proving_ground + validation_factory
第2层 研究层: account_truth/master_data/market_data/outcome_engine/attribution/replay
第1层 基础层: council/alpha_factory/factor_foundation/cockpit
第0层 治理层: constitution/policies/guardrails/no_production_boundary
```

## 四、Golden Path

```bash
bash scripts/run_golden_path_600519.sh
```

跑通 600519 贵州茅台全链路：
IDEA → DATA → FACTOR → OUTCOME → ATTRIBUTION → REPLAY → COUNCIL → DECISION → MEMORY → HUMAN_REPORT

## 五、核心行为准则

### 绝对禁止
1. 不得新增能力模块 (ARCHITECTURE FREEZE)
2. 不得新增研究/验证/进化模块
3. 不得接 broker/runtime/real trade
4. 不得开 production
5. 不得修改 module count (必须保持 160)
6. 不得把 PRODUCTION_CANDIDATE 写成 Production Ready
7. 不得把架构冻结状态解除

### 允许
1. 文档化 (onboarding guide, user manual)
2. Golden Path 可执行化增强
3. Bug fix
4. Test audit
5. CI/CD 改进
6. 三仓同步 (GitHub + 本地 + Workspace)

### 工具规则
1. OpenCode v1.15.11 在 /opt/homebrew/bin/opencode, 配置 ~/.config/opencode/opencode.jsonc
2. Code Agent 自动路由规则在 AGENTS.md
3. 每阶段独立 commit + verify
4. verify 必须 pytest, PASS 必须在最后
5. 三仓同步每阶段执行

## 六、关键文件索引

```
docs/research_os/ARCHITECTURE_FREEZE_ACCEPTANCE.md  — 架构冻结验收
docs/research_os/RESEARCH_OS_V3_FREEZE_MANIFEST.md  — 冻结清单
docs/research_db/RESEARCH_OS_CAPABILITY_MAP.md      — 能力矩阵
docs/research_db/GOLDEN_PATH_CASE_001.md            — 黄金路径文档
docs/research_db/RESEARCH_OS_V3_WHITEPAPER.md       — 白皮书
scripts/verify_research_os_architecture_freeze.sh   — 冻结验证
scripts/run_golden_path_600519.sh                   — 黄金路径运行
```

## 七、下一阶段建议

1. Onboarding Guide - 新人一周内理解系统
2. User Operation Manual 最终版
3. Test Quality Audit - 审计测试质量
4. Golden Path 多案例

不得进入 Phase 6 (Production Simulation) 或 Broker/Runtime。
