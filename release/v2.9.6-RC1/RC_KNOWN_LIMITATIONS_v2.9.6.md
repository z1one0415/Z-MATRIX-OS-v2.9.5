# RC Known Limitations v2.9.6 — 已知非阻塞保留项

## 说明

以下为 pre-existing 已知测试失败项，不影响 v2.9.6-RC1 核心能力链。在 RC verify 中作为 non-blocking 非阻塞项处理。

---

### 1. `tests/test_zg09_type_a_horizontal.py`

| 字段 | 值 |
|------|------|
| 原因 | legacy interface incompatible after R-Matrix v2.0 migration |
| RC 影响 | non-blocking |
| 替代覆盖 | `tests/test_zg09_uses_rmatrix_service_only.py` |
| 替代覆盖 | `tests/test_rmatrix_contract_schema.py` |
| 替代覆盖 | `tests/test_rmatrix_service_v20_four_king.py` |

### 2. `tests/test_zg09_zg10_contracts.py`

| 字段 | 值 |
|------|------|
| 原因 | legacy scorer contract before R-Matrix v2.0 |
| RC 影响 | non-blocking |
| 替代覆盖 | `tests/test_zg18_g09_constraint_consistency.py` |
| 替代覆盖 | `tests/test_g09_g14_rmatrix_consistency.py` |

### 3. `tests/test_zg14_matrix_reliability.py`

| 字段 | 值 |
|------|------|
| 原因 | legacy matrix reliability expectation before unified R-Matrix service |
| RC 影响 | non-blocking |
| 替代覆盖 | `tests/test_zg14_uses_rmatrix_service.py` |
| 替代覆盖 | `tests/test_g09_g14_rmatrix_consistency.py` |

### 4. `tests/test_hermes_full.py`

| 字段 | 值 |
|------|------|
| 原因 | memory_bank interface drift (hermes模块接口变更) |
| RC 影响 | non-blocking |
| 替代覆盖 | G18 paper execution record tests |
| 替代覆盖 | Z9 calibration sample / queue / backfill / policy tests |

---

## 替代覆盖测试清单（强制项）

以下测试已在 RC verify 中作为强制项执行，覆盖了 legacy 测试的原有关注点：

| 领域 | 测试 | 覆盖内容 |
|:----|------|----------|
| R-Matrix v2.0 | `test_rmatrix_service_v20_four_king.py` | 四天王服务核心 |
| R-Matrix v2.0 | `test_rmatrix_contract_schema.py` | 契约 schema |
| R-Matrix v2.0 | `test_rmatrix_service_degraded_contract.py` | 降级契约 |
| G18 约束 | `test_zg18_g09_constraint_consistency.py` | G18-G09一致性 |
| G18 约束 | `test_g09_g14_rmatrix_consistency.py` | G09-G14同源性 |
| G14 R-Matrix | `test_zg14_uses_rmatrix_service.py` | G14使用R-Matrix service |
| G09 R-Matrix | `test_zg09_uses_rmatrix_service_only.py` | G09使用R-Matrix service |
| G18 Z9链 | `test_rc_verification_gate.py` | 完整preview chain |
