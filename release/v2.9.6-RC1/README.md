# Z-MATRIX-OS v2.9.6-RC1 — Release Candidate Package

## 基本信息

| 字段 | 值 |
|------|------|
| RC 名称 | Z-MATRIX-OS v2.9.6-RC1 |
| RC gate closeout commit | `a2ad4991ba224b532edbce7e1c03cbd4c6f43195` |
| RC package base commit | `7b7741d81d84aebb291c3f5b64a78e03aeb4d86f` |
| Release notes commit | `4a78331158449a83473cf1985bd261e2418b1b13` |
| 分支 | master |
| 发布日期 | 2026-05-25 |

## 适用范围

- paper execution only
- Z9 preview chain (sample → queue → backfill → calibration policy)
- RC verification gate

## 不包含

- ❌ no real trade
- ❌ no real Z9 write
- ❌ no real market data fetch
- ❌ no auto calibration
- ❌ no broker connection

## 快速验收

```bash
# 完整 verify
./scripts/verify_rc_candidate.sh

# 或有选择地运行
python3 tests/test_rc_verification_gate.py
```

## 包内文件

| 文件 | 说明 |
|------|------|
| `README.md` | 本文件 |
| `RC_MANIFEST_v2.9.6.md` | RC 版本清单 |
| `CONTRACT_INDEX_v2.9.6.md` | 全量契约索引 |
| `RC_KNOWN_LIMITATIONS_v2.9.6.md` | 已知非阻塞保留项 |
| `RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md` | 验收报告模板 |
| `VERIFY_COMMANDS.md` | 验收命令速查 |
| `ARTIFACT_CHECKSUMS.txt` | 文件校验和 |
| `RELEASE_NOTES_v2.9.6-RC1.md` | 发布说明 |
| `OPERATOR_RUNBOOK_v2.9.6-RC1.md` | 操作手册 |
| `TAG_RECORD_v2.9.6-RC1.md` | Tag 记录 |

## 下一步

| Batch | 内容 |
|:----:|------|
| E-3 | Release Notes |
| E-4 | Operator Runbook |
| E-5 | Tag v2.9.6-RC1 |
