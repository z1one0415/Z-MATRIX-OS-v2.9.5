# Z-MATRIX-OS v2.9.7-arch-RC1 — Architecture Verification Commands

## Compile

```bash
python3 -m compileall zmatrix tests scripts pipelines
```

## Registry 测试

```bash
python3 tests/test_shared_skill_registry.py        # 12/12 PASS
python3 tests/test_pipeline_registry.py             # 11/11 PASS
python3 tests/test_gate_registry.py                 # 13/13 PASS
python3 tests/test_workflow_dag.py                  # 13/13 PASS
```

## Architecture 审计

```bash
python3 tests/test_architecture_enforcement.py      # 6/6 PASS
python3 tests/test_cross_pipeline_conflict_audit.py # 6/6 PASS
```

## System Controller

```bash
python3 tests/test_system_controller_mvp.py         # 10/10 PASS
```

## Architecture Package

```bash
python3 scripts/build_architecture_package_manifest.py
python3 tests/test_architecture_package.py          # 8/8 PASS
```

## 完整验收

```bash
bash scripts/verify_architecture_candidate.sh
```
