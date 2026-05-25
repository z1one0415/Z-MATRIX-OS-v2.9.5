# Z-MATRIX-OS v2.9.6-RC1 — Operator Runbook

## 1. 适用对象

- **Developer**: 需了解 Z-MATRIX-OS 的 A→D 批次架构
- **Reviewer**: 需要验证 RC 验收门是否通过
- **Operator**: 运行 G18 paper preview chain 并解读输出
- **不适用**: 实盘交易员直接根据 Z9 preview 下单

## 2. 环境前置

| 要求 | 说明 |
|------|------|
| Python | 3.10+ (已知 3.14.4 兼容) |
| Repo root | 确保所有 `pipelines/` 和 `zmatrix/` 在 sys.path 中 |
| Broker 账户 | ❌ 不需要 |
| Z9 write 后端 | ❌ 不需要 |
| 行情 API | ❌ 不需要（G18 使用 proxy 数据） |
| 网络 | 可选，用于 G09 信号加载（无网络降级为 WATCH） |

## 3. 快速验收流程

```bash
# 1. 编译全部模块
python3 -m compileall pipelines tests zmatrix hermes scripts

# 2. RC 验收门
python3 tests/test_rc_verification_gate.py
# 预期: 9/9 PASS

# 3. 发布包完整性
python3 tests/test_rc_packaging.py
# 预期: 10/10 PASS

# 4. 完整 verify 脚本
./scripts/verify_rc_candidate.sh
```

## 4. 运行 G18 Paper Preview Chain

### 方式一：CLI

```bash
python3 pipelines/Z-G18_天机引擎/gate_pipeline.py \
  --tickers 002472,601899,588000 \
  --mode daily
```

### 方式二：Python import

```python
import importlib.util

spec = importlib.util.spec_from_file_location(
    "zg18",
    "pipelines/Z-G18_天机引擎/gate_pipeline.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

result = mod.run(tickers=["002472"])
pred = result["predictions"][0]

# 查看全部 preview chain
for key in [
    "paper_execution_record",
    "z9_calibration_sample_preview",
    "z9_ingestion_queue_preview",
    "z9_outcome_backfill_task_preview",
    "z9_calibration_policy_preview",
]:
    print(f"{key}: {'✅' if pred.get(key) else '❌'}")

# 查看 safety gates
for key in [
    "z9_real_write_allowed",
    "z9_queue_write_allowed",
    "z9_outcome_write_allowed",
    "z9_market_fetch_allowed",
    "z9_auto_calibration_allowed",
]:
    print(f"{key}: {result['sections'].get(key)}")
```

## 5. 输出解释

### G18 prediction 输出字段

| 字段 | 说明 | 典型值 |
|------|------|--------|
| `ticker` | 股票代码 | "002472" |
| `probability` | 概率评分 | 0.72 |
| `action_proposal` | 动作建议 | "WAIT" / "WATCH" |
| `final_decision` | G18 最终裁决 | dict（含 blocking_reasons） |
| `upstream_evidence` | 6 源证据聚合 | dict（含 evidence_available） |
| `conflict_resolution` | 冲突裁决 | dict（含 has_conflict） |
| `paper_execution_record` | 纸面执行记录 | dict（C-4） |
| `z9_calibration_sample_preview` | Z9 校准样本预览 | dict（D-1） |
| `z9_ingestion_queue_preview` | Z9 队列项目预览 | dict（D-2） |
| `z9_outcome_backfill_task_preview` | Z9 回填任务预览 | dict（D-3） |
| `z9_calibration_policy_preview` | Z9 校准策略预览 | dict（D-4） |

### Sections safety gates

| 闸门 | 预期值 | 含义 |
|:----:|:------:|------|
| `z9_real_write_allowed` | `False` | 禁止真实 Z9 写 |
| `z9_queue_write_allowed` | `False` | 禁止真实队列写 |
| `z9_outcome_write_allowed` | `False` | 禁止 outcome 回填写 |
| `z9_market_fetch_allowed` | `False` | 禁止真实行情拉取 |
| `z9_auto_calibration_allowed` | `False` | 禁止自动调参 |
| `z9_real_write_allowed` 等 | `False` | 所有写入开关关闭 |

## 6. 安全边界确认

| 操作 | 状态 |
|:----|:----:|
| Real trade (BUY/SELL/ADD/CLEAR) | ❌ 禁止 (assert_no_real_trade) |
| Broker order (MARKET_ORDER/BROKER_ORDER) | ❌ 禁止 |
| Real Z9 write | ❌ 禁止 (z9_write_allowed=False) |
| Queue write | ❌ 禁止 (queue_write_allowed=False) |
| Real market data fetch | ❌ 禁止 (real_fetch_allowed=False) |
| Auto calibration | ❌ 禁止 (auto_calibration_allowed=False) |
| 所有校准输出 | preview only |

## 7. 常见失败与处理

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| `compileall` 失败 | Python 版本不兼容 | 检查 Python >= 3.10 |
| pytest 失败 | test_hermes_full.py import error | 已知 non-blocking，忽略 |
| legacy test 警告 | R-Matrix 旧接口测试 | 已知 non-blocking，不影响核心管线 |
| working tree dirty | 未提交修改 | `git status` 检查后 `git stash` |
| checksum mismatch | release 包被修改 | 重新运行 `python3 scripts/build_rc_package_manifest.py` |
| missing release artifact | 文件被误删 | 从 git 恢复: `git checkout -- <path>` |
| G18 output missing preview key | 某个 D-batch 未加载 | 检查 import 是否正确 |
| safety gate unexpectedly True | z9_xxx_allowed 标记错误 | 立即停止，联系开发者 |
| G09 信号未加载 | 本地路径缺少 G09 数据文件 | non-blocking，自动降级为 WATCH |

## 8. 回滚流程

```bash
# 1. 查看最近提交
git log --oneline -n 10

# 2. 回滚到指定 commit
git revert <commit-hash>

# 3. 验证回滚后状态
python3 -m compileall pipelines tests zmatrix hermes scripts
python3 tests/test_rc_verification_gate.py
./scripts/verify_rc_candidate.sh
```

### 回滚须知

- Z9 不写真实数据，回滚不涉及数据迁移
- G18 无持久化配置变更
- 回滚后如果 safety gate 标记出现异常（变为 True），立即停止操作并联系开发者

## 9. 不允许操作

| 操作 | 理由 |
|:----|:----:|
| ❌ 把 `paper_action` 当实盘动作执行 | C-4 仅纸面记录，不连接券商 |
| ❌ 手动改 `z9_write_allowed` 为 `True` | D-1 契约冻结，不允许真实写 |
| ❌ 把 `BUY/SELL` 写入 action field | 会被 `assert_no_real_trade` 拦截而崩溃 |
| ❌ 接券商接口到 Z9 preview chain | D-3/D-4 仅为契约预览 |
| ❌ 绕过 `verify_rc_candidate.sh` | 跳过验收门可能导致不一致状态 |
| ❌ 手动修改 `ARTIFACT_CHECKSUMS.txt` | 应运行 `build_rc_package_manifest.py` 自动更新 |
| ❌ 删除 `release/` 目录文件后不重新生成 | 包完整性依赖 checksum |
