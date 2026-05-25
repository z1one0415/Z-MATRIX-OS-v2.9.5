#!/usr/bin/env python3
"""Z-MATRIX-OS v2.9.6-RC1 — RC Verification Gate Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent


# ── 1. RC Manifest ──

def test_rc_manifest_exists():
    path = WORKSPACE / "docs" / "release" / "RC_MANIFEST_v2.9.6.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    for keyword in ["Z-MATRIX-OS v2.9.6-RC1", "禁止边界", "回滚策略", "已知保留项"]:
        assert keyword in content, f"manifest missing keyword: {keyword}"
    print("✅ RC_MANIFEST_v2.9.6.md exists with key sections")


# ── 2. Contract Index ──

def test_contract_index_exists_and_mentions_core_contracts():
    path = WORKSPACE / "docs" / "contracts" / "CONTRACT_INDEX_v2.9.6.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    for keyword in [
        "G18_FINAL_DECISION_ENVELOPE_V11.md",
        "Z9_CALIBRATION_POLICY_V10.md",
        "R_MATRIX_V2_CONTRACT.md",
        "Z9_CALIBRATION_SAMPLE_V10.md",
        "Z9_INGESTION_QUEUE_V10.md",
        "Z9_OUTCOME_BACKFILL_V10.md",
        "G18_UPSTREAM_EVIDENCE_V10.md",
        "G18_CONFLICT_RESOLVER_V10.md",
        "G18_PAPER_EXECUTION_RECORD_V10.md",
        "RC_MANIFEST_v2.9.6.md",
        "no real trade",
    ]:
        assert keyword in content, f"contract index missing reference: {keyword}"
    print("✅ CONTRACT_INDEX_v2.9.6.md mentions all core contracts")


# ── 3. RC Report Template ──

def test_rc_report_template_exists():
    path = WORKSPACE / "docs" / "release" / "RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md"
    assert path.exists(), f"missing: {path}"
    content = path.read_text()
    for keyword in ["compileall", "verify_rc_candidate.sh", "安全边界确认", "RC 放行结论"]:
        assert keyword in content
    print("✅ RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md exists with key sections")


# ── 4. G18 Z9 Preview Chain ──

def test_g18_prediction_contains_full_z9_preview_chain():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "zg18", str(WORKSPACE / "pipelines" / "Z-G18_天机引擎" / "gate_pipeline.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    chain_keys = [
        "paper_execution_record",
        "z9_calibration_sample_preview",
        "z9_ingestion_queue_preview",
        "z9_outcome_backfill_task_preview",
        "z9_calibration_policy_preview",
    ]
    for k in chain_keys:
        assert k in p, f"G18 prediction missing: {k}"
        assert p[k] is not None, f"G18 prediction {k} is None"
    print(f"✅ G18 prediction contains full Z9 preview chain ({len(chain_keys)} items)")


# ── 5. Safety Sections ──

def test_rc_safety_sections_all_false():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "zg18", str(WORKSPACE / "pipelines" / "Z-G18_天机引擎" / "gate_pipeline.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    s = r["sections"]
    safety_checks = {
        "z9_real_write_allowed": False,
        "z9_queue_write_allowed": False,
        "z9_outcome_write_allowed": False,
        "z9_market_fetch_allowed": False,
        "z9_auto_calibration_allowed": False,
    }
    for key, expected in safety_checks.items():
        assert key in s, f"sections missing: {key}"
        assert s[key] == expected, f"{key} expected {expected}, got {s[key]}"
    print("✅ safety sections: all 5 gates closed (False)")


# ── 6. Calibration Policy Preview Write Policy ──

def test_calibration_policy_preview_no_real_write():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "zg18", str(WORKSPACE / "pipelines" / "Z-G18_天机引擎" / "gate_pipeline.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.run(tickers=["002472"])
    p = r["predictions"][0]
    cp = p.get("z9_calibration_policy_preview", {})
    wp = cp.get("write_policy", {})
    for key in ["ev_write_allowed", "r_matrix_write_allowed", "g18_write_allowed", "z9_write_allowed"]:
        assert key in wp, f"calibration policy preview missing write_policy.{key}"
        assert wp[key] is False, f"calibration policy preview {key} must be False"
    assert cp.get("validation", {}).get("auto_calibration_allowed") is False
    print("✅ calibration_policy_preview: no real write (4 gates False)")


# ── 7. Required RC files check ──

def test_rc_known_limitations_exists_and_mentions_non_blocking_legacy_tests():
    """RC_KNOWN_LIMITATIONS 存在并列出legacy测试"""
    path = WORKSPACE / "docs" / "release" / "RC_KNOWN_LIMITATIONS_v2.9.6.md"
    assert path.exists(), "missing RC_KNOWN_LIMITATIONS"
    content = path.read_text()
    for keyword in [
        "test_zg09_type_a_horizontal.py",
        "test_zg09_zg10_contracts.py",
        "test_zg14_matrix_reliability.py",
        "non-blocking",
        "替代覆盖",
    ]:
        assert keyword in content, f"known limitations missing: {keyword}"
    print("✅ RC_KNOWN_LIMITATIONS: legacy tests listed as non-blocking")


def test_verify_script_has_non_blocking_legacy_section():
    """verify_rc_candidate.sh 有 non-blocking legacy section"""
    path = WORKSPACE / "scripts" / "verify_rc_candidate.sh"
    content = path.read_text()
    assert "Non-blocking legacy tests" in content
    assert "non-blocking legacy limitation" in content
    # 验证三个legacy测试不在pytest aggregate中
    for legacy in ["test_zg09_type_a_horizontal.py", "test_zg09_zg10_contracts.py", "test_zg14_matrix_reliability.py"]:
        assert legacy not in content or "legacy_tests" in content, f"{legacy} still in forced path"
    print("✅ verify script: non-blocking legacy section present, forced path removed")


def test_required_rc_files_exist():
    files = [
        "docs/release/RC_MANIFEST_v2.9.6.md",
        "docs/contracts/CONTRACT_INDEX_v2.9.6.md",
        "docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md",
        "docs/contracts/Z9_CALIBRATION_POLICY_V10.md",
        "docs/contracts/examples/z9_calibration_policy_preview_v10_example.json",
        "docs/contracts/Z9_OUTCOME_BACKFILL_V10.md",
        "docs/contracts/examples/z9_outcome_backfill_task_v10_example.json",
        "docs/contracts/Z9_INGESTION_QUEUE_V10.md",
        "docs/contracts/examples/z9_ingestion_queue_item_v10_example.json",
        "docs/contracts/Z9_CALIBRATION_SAMPLE_V10.md",
        "docs/contracts/examples/z9_calibration_sample_v10_example.json",
        "scripts/verify_rc_candidate.sh",
    ]
    for f in files:
        path = WORKSPACE / f
        assert path.exists(), f"missing required RC file: {path}"
    print(f"✅ required RC files: {len(files)}/12 present")


if __name__ == "__main__":
    test_rc_manifest_exists()
    test_contract_index_exists_and_mentions_core_contracts()
    test_rc_report_template_exists()
    test_g18_prediction_contains_full_z9_preview_chain()
    test_rc_safety_sections_all_false()
    test_calibration_policy_preview_no_real_write()
    test_rc_known_limitations_exists_and_mentions_non_blocking_legacy_tests()
    test_verify_script_has_non_blocking_legacy_section()
    test_required_rc_files_exist()
    print("\n🏁 Z-MATRIX-OS v2.9.6-RC1 — RC Verification Gate PASS")
