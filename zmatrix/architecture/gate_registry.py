#!/usr/bin/env python3
"""
☯️ Gate Registry v1.0 — Z-MATRIX-OS 三层架构第三层组件 (Batch F-3)

Gate Registry 是系统控制层的 gate 注册表。
所有安全边界、contract validation、preview-only、RC verification 闸门必须注册于此。

原则:
  1. gate 是系统控制层组件，不得实现业务判断
  2. pipeline.required_gates 必须全部存在于 GATE_REGISTRY
  3. blocking gate 不可降级通过
"""
from __future__ import annotations

from typing import Any

GATE_REGISTRY: dict[str, dict[str, Any]] = {
    "safety.no_real_trade": {
        "layer": "system_control",
        "gate_type": "safety",
        "purpose": "Block real trade / broker order / market order capabilities",
        "owner": "SystemCore",
        "applies_to": ["Z-G18", "Z-G09", "Z-G14", "RC-release"],
        "enforced_by": "zmatrix.action.action_contracts.assert_no_real_trade",
        "blocking": True,
        "degradable": False,
        "forbidden_tokens": [
            "BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE",
        ],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
    },
    "z9.preview_only": {
        "layer": "system_control",
        "gate_type": "write_boundary",
        "purpose": "Ensure all Z9 outputs remain preview-only and no real write occurs",
        "owner": "Z9",
        "applies_to": ["Z-G18"],
        "enforced_by": "tests/test_z9_calibration_policy_contract.py",
        "blocking": True,
        "degradable": False,
        "required_false_flags": [
            "z9_real_write_allowed", "z9_queue_write_allowed",
            "z9_outcome_write_allowed", "z9_market_fetch_allowed",
            "z9_auto_calibration_allowed",
        ],
        "contract": "docs/contracts/Z9_CALIBRATION_POLICY_V10.md",
        "test": "tests/test_z9_calibration_policy_contract.py",
    },
    "contract.validation": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure architecture contracts and runtime payload contracts are structurally valid",
        "owner": "SystemCore",
        "applies_to": ["Z-G18", "RC-release"],
        "enforced_by": "tests/*_contract*.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/GATE_REGISTRY_V10.md",
        "test": "tests/test_gate_registry.py",
    },
    "rc.packaging": {
        "layer": "system_control",
        "gate_type": "release",
        "purpose": "Ensure RC release package files and checksums are complete",
        "owner": "RC",
        "applies_to": ["RC-release"],
        "enforced_by": "tests/test_rc_packaging.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_MANIFEST_v2.9.6.md",
        "test": "tests/test_rc_packaging.py",
    },
    "rc.verification": {
        "layer": "system_control",
        "gate_type": "release",
        "purpose": "Run RC verification gate and safety boundary scan",
        "owner": "RC",
        "applies_to": ["RC-release"],
        "enforced_by": "scripts/verify_rc_candidate.sh",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md",
        "test": "tests/test_rc_verification_gate.py",
    },
    "r_matrix.cycle_valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "purpose": "Ensure R-Matrix cycle output is contract-valid before downstream use",
        "owner": "R-Matrix",
        "applies_to": ["Z-G09", "Z-G14"],
        "enforced_by": "tests/test_rmatrix_contract_schema.py",
        "blocking": True,
        "degradable": True,
        "contract": "docs/contracts/R_MATRIX_V2_CONTRACT.md",
        "test": "tests/test_rmatrix_contract_schema.py",
    },
    "safety.boundary_scan": {
        "layer": "system_control",
        "gate_type": "safety",
        "purpose": "Scan executable surfaces for real trade / real write boundary leaks",
        "owner": "SystemCore",
        "applies_to": ["RC-release"],
        "enforced_by": "scripts/verify_rc_candidate.sh",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_MANIFEST_v2.9.6.md",
        "test": "tests/test_rc_verification_gate.py",
    },
}


def get_gate(gate_id: str) -> dict | None:
    return GATE_REGISTRY.get(gate_id)


def get_gates_for_pipeline(pipeline_id: str) -> list[tuple[str, dict]]:
    return [(gid, g) for gid, g in GATE_REGISTRY.items()
            if pipeline_id in g.get("applies_to", [])]


def check_gate_registry_integrity() -> list[str]:
    violations = []
    for gid, gate in GATE_REGISTRY.items():
        if gate.get("layer") != "system_control":
            violations.append(f"{gid}: layer != system_control")
        if not gate.get("gate_type"):
            violations.append(f"{gid}: missing gate_type")
        if not gate.get("owner"):
            violations.append(f"{gid}: missing owner")
        if not gate.get("applies_to"):
            violations.append(f"{gid}: missing applies_to")
        if not gate.get("enforced_by"):
            violations.append(f"{gid}: missing enforced_by")
        if not gate.get("contract"):
            violations.append(f"{gid}: missing contract")
        if not gate.get("test"):
            violations.append(f"{gid}: missing test")
    return violations


def check_pipeline_required_gates_registered() -> list[str]:
    """检查 PIPELINE_REGISTRY.required_gates 是否全部存在于 GATE_REGISTRY"""
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY

    missing = []
    for pid, p in PIPELINE_REGISTRY.items():
        for g in p.get("required_gates", []):
            if g not in GATE_REGISTRY:
                missing.append(f"{pid} -> {g}")
    return missing
