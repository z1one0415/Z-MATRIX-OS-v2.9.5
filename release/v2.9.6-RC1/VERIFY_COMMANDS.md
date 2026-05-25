# Z-MATRIX-OS v2.9.6-RC1 — Verification Commands

## 预备

```bash
cd <repo-root>
```

## 编译

```bash
python3 -m compileall pipelines tests zmatrix hermes scripts
```

## RC Gate 测试

```bash
python3 tests/test_rc_verification_gate.py
# 预期: 9/9 PASS
```

## Z9 后验链路 Contract 测试

```bash
python3 tests/test_z9_calibration_policy_contract.py  # 24/24 PASS
python3 tests/test_z9_outcome_backfill_contract.py    # 18/18 PASS
python3 tests/test_z9_ingestion_queue_contract.py     # 12/12 PASS
python3 tests/test_z9_calibration_sample_contract.py  # 6/6 PASS
python3 tests/test_g18_paper_execution_record.py      # 8/8 PASS
```

## RC Packaging 测试

```bash
python3 tests/test_rc_packaging.py
# 预期: 5/5 PASS
```

## 完整 Verify 脚本

```bash
./scripts/verify_rc_candidate.sh
```

## Git 检查

```bash
git diff --check
git status --short    # 预期: clean
```

## 安全边界检查 (独立)

安全边界在 `verify_rc_candidate.sh` 中自动执行（AST scanner）。
如需独立运行：

```bash
python3 -c "
import ast, sys, os
from pathlib import Path
# ... (详见 scripts/verify_rc_candidate.sh 的 Safety boundary scan 段)
"
```
