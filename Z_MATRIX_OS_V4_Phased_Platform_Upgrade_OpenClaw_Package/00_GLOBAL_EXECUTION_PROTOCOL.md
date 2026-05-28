# 00｜V4.0 Research OS → Research Platform 全局执行协议

## 1. 启动定位

本包用于启动：

```text
V4.0-0 Platform Hardgate — Research OS Governance Upgrade
```

不是策略增强，不是实盘系统，不是自动交易系统，不是 Agent 扩张。

目标：

```text
把 v3.5.20 冻结后的 Research OS
升级为可持续扩展、可测试、可治理、可分层演进的 Research Platform。
```

## 2. 分阶段路线

```text
V4.0-0：Platform Hardgate
V4.0-1：Data Governance
V4.0-2：Factor Registry
V4.0-3：Research Experiment OS
V4.0-4：B-Matrix Current Snapshot Workbench
V4.0-5：D-Matrix Data Source Plan
```

## 3. 全局硬边界

所有阶段必须保持：

```text
real_trade_allowed=False
broker_order_allowed=False
runtime_enabled=False
auto_buy_allowed=False
auto_sell_allowed=False
production_strategy_modified=False
classifier_production_modified=False
production_allowed=False
```

禁止：

```text
1. 不接 broker。
2. 不开真实 runtime。
3. 不生成真实交易指令。
4. 不修改 classifier 生产链。
5. 不新增 alpha 策略逻辑。
6. 不提升任何因子/策略到 production。
7. 不推翻 v3.5.20 冻结结论。
8. 不用文件名替代 evidence/status 验证。
9. 不让 LLM 输出主观连续分数。
```

## 4. v3.5.20 冻结基座

V4.0 所有阶段必须承认：

```text
R-Matrix historical replay: RESEARCH_READY
B-Matrix current snapshot: RESEARCH_READY
B-Matrix historical PIT: BLOCKED
D-Matrix: BLOCKED
production: BLOCKED
real_trade: BLOCKED
broker_runtime: BLOCKED
classifier_production_chain: FROZEN
```

## 5. 每阶段统一完成报告

```text
# V4.0-X 完成报告

## 1. Phase 目标
## 2. 已完成内容
## 3. 新增/修改文件
## 4. 测试命令与结果
## 5. Verify 脚本结果
## 6. Acceptance Matrix 更新项
## 7. 安全边界确认
- real_trade_allowed=False
- broker_order_allowed=False
- runtime_enabled=False
- auto_buy_allowed=False
- auto_sell_allowed=False
- production_strategy_modified=False
- classifier_production_modified=False

## 8. v3.5.20 冻结基座确认
- baseline_rewritten=False
- classifier_production_chain_modified=False
- production_chain_modified=False

## 9. Commit SHA
## 10. Known Limitations
## 11. 下一阶段是否允许启动
```

## 6. 全局 verify

最终必须具备：

```text
scripts/verify_v400_phase0_platform_hardgate.sh
scripts/verify_v400_phase1_data_governance.sh
scripts/verify_v400_phase2_factor_registry.sh
scripts/verify_v400_phase3_experiment_os.sh
scripts/verify_v400_phase4_b_matrix_workbench.sh
scripts/verify_v400_phase5_d_matrix_plan.sh
scripts/verify_v400_all_phases.sh
```

每阶段必须：

```bash
python -m compileall governance workbenches plans tests scripts
pytest -q tests/governance/
bash scripts/verify_v400_phaseX_*.sh
git add .
git commit -m "v4.0-X: <phase name>"
git push
git rev-parse HEAD
```
