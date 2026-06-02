# Coding Discipline Autopilot v1.0

## 触发时机
每次收到工程编码任务时，在动手前执行本流程。

## Step 1: 任务分类判定

| 类别 | 条件 | 示例 |
|------|------|------|
| NEW_MODULE | 创建新.py文件 + A+规格完整 | V11 builder脚本 |
| BATCH_IMPL | 含"Vx-A/B/C"或"一次执行"指令 | V6-B/C/D |
| BATCH_TEST | 需为已完成N个模块生成全面测试 | V5 31个test |
| DOC_ONLY | 仅文档/report/verify/配置 | Closeout报告 |
| FIX_ONLY | 修改已有文件局部编辑 | 修复语法错误 |
| INFRA_ONLY | CI/gitignore/guardrail非代码 | 配置文件 |

## Step 2: 路由判定

```python
USE_OPENCODE = (
    category in (NEW_MODULE, BATCH_IMPL, BATCH_TEST)
    and task_has_complete_spec
    and not (quick_fix or single_line_edit)
)

SKIP_OPENCODE = category in (DOC_ONLY, FIX_ONLY, INFRA_ONLY)
```

## Step 3: 执行

### USE_OPENCODE = True:
```bash
# 1. 先编译检查当前状态
python -m compileall -q scripts/ zmatrix/ tests/

# 2. 调用 opencode，写入任务文件
cat > /tmp/opencode_task.md << 'TASKEOF'
<完整任务描述，含输入/输出/边界/禁止项>
TASKEOF

# 3. 执行
opencode run --task-file /tmp/opencode_task.md --model deepseek/deepseek-v4-pro

# 4. 校验
python -m compileall -q scripts/ zmatrix/ tests/
pytest tests/cases/ -q
check branch + commit
```

### SKIP_OPENCODE = True:
```bash
# 手写模式 — 直接用 write/edit 工具
# 每次 commit 前必须: compileall + pytest + branch check
```

## Step 4: 强制自检（每次commit前）

```bash
git branch --show-current        # 必须是 v4.0-batch-0-final-hardgates-scope-lock
git status --short               # 无意外文件
python -m compileall -q scripts/ zmatrix/ tests/  # 0 语法错误
pytest tests/cases/ -q           # 全部通过
```

## 执行记录

| 日期 | 任务 | 类别 | 路由 | 结果 |
|------|------|------|------|------|
| - | - | - | - | - |

## 禁止模式

```
❌ 收到 Phase/Batch 任务 → 直接 exec/write 写代码（跳过判定）
❌ 大任务用 exec inline Python 压缩式完成（应委托 opencode）
❌ 调用 opencode 后，再手动改同一批文件（信任委托，只做校验）
❌ commit 前不检查 branch
```
