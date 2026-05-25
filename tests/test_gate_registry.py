#!/usr/bin/env python3
"""Gate Registry v1.0 — Batch F-3 contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.architecture.gate_registry import (
    GATE_REGISTRY,
    get_gate,
    get_gates_for_pipeline,
    check_gate_registry_integrity,
    check_pipeline_required_gates_registered,
)
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY


def test_gate_registry_exists_and_non_empty():
    assert isinstance(GATE_REGISTRY, dict)
    assert len(GATE_REGISTRY) >= 5, f"expected >=5 gates, got {len(GATE_REGISTRY)}"
    print(f"✅ gate registry exists: {len(GATE_REGISTRY)} gates registered")


def test_every_gate_has_required_fields():
    for gid, g in GATE_REGISTRY.items():
        assert g.get("layer") == "system_control", f"{gid}: layer"
        assert g.get("gate_type"), f"{gid}: missing gate_type"
        assert g.get("owner"), f"{gid}: missing owner"
        assert g.get("purpose"), f"{gid}: missing purpose"
        assert g.get("applies_to"), f"{gid}: missing applies_to"
        assert g.get("enforced_by"), f"{gid}: missing enforced_by"
        assert "blocking" in g, f"{gid}: missing blocking"
        assert "degradable" in g, f"{gid}: missing degradable"
        assert g.get("contract"), f"{gid}: missing contract"
        assert g.get("test"), f"{gid}: missing test"
    print(f"✅ every gate has required fields ({len(GATE_REGISTRY)} gates)")


def test_pipeline_required_gates_registered():
    missing = check_pipeline_required_gates_registered()
    assert len(missing) == 0, f"pipeline required_gates not in GATE_REGISTRY: {missing}"
    print("✅ all pipeline required_gates exist in GATE_REGISTRY")


def test_no_real_trade_gate_registered():
    g = get_gate("safety.no_real_trade")
    assert g is not None
    assert g["owner"] == "SystemCore"
    assert g["blocking"] is True
    assert "Z-G18" in g["applies_to"]
    assert "RC-release" in g["applies_to"]
    print("✅ safety.no_real_trade gate: registered, blocking, applies to Z-G18 + RC-release")


def test_z9_preview_only_gate_registered():
    g = get_gate("z9.preview_only")
    assert g is not None
    assert g["owner"] == "Z9"
    assert "Z-G18" in g["applies_to"]
    assert len(g["required_false_flags"]) >= 4
    print("✅ z9.preview_only gate: registered with false-flag checks")


def test_rc_gates_registered():
    for gid in ["rc.packaging", "rc.verification", "safety.boundary_scan"]:
        g = get_gate(gid)
        assert g is not None, f"{gid} not registered"
        assert g["blocking"] is True
    print("✅ RC gates: rc.packaging + rc.verification + safety.boundary_scan all registered")


def test_rmatrix_cycle_gate_registered():
    g = get_gate("r_matrix.cycle_valid")
    assert g is not None
    assert g["owner"] == "R-Matrix"
    assert g["degradable"] is True  # only gate allowed to degrade
    assert "Z-G09" in g["applies_to"]
    assert "Z-G14" in g["applies_to"]
    print("✅ r_matrix.cycle_valid gate: registered, degradable, applies to Z-G09 + Z-G14")


def test_gate_registry_integrity_clean():
    violations = check_gate_registry_integrity()
    assert len(violations) == 0, f"integrity violations: {violations}"
    print("✅ gate registry integrity: clean")


def test_get_gates_for_pipeline_api():
    g18_gates = get_gates_for_pipeline("Z-G18")
    g18_ids = [gid for gid, _ in g18_gates]
    assert "safety.no_real_trade" in g18_ids
    assert "z9.preview_only" in g18_ids
    assert "contract.validation" in g18_ids
    print(f"✅ Z-G18 bound to {len(g18_gates)} gates (safety + z9 + contract)")


def test_rc_release_gates():
    rc_gates = get_gates_for_pipeline("RC-release")
    rc_ids = [gid for gid, _ in rc_gates]
    assert "rc.packaging" in rc_ids
    assert "rc.verification" in rc_ids
    assert "safety.boundary_scan" in rc_ids
    assert "safety.no_real_trade" in rc_ids
    print(f"✅ RC-release bound to {len(rc_gates)} gates (packaging + verification + safety)")


def test_gate_type_diversity():
    types = {g["gate_type"] for g in GATE_REGISTRY.values()}
    expected = {"safety", "write_boundary", "contract", "release", "data_contract", "investment_control"}
    assert types == expected, f"gate types: {types} != {expected}"
    print(f"✅ gate types: {', '.join(sorted(types))}")


if __name__ == "__main__":
    test_gate_registry_exists_and_non_empty()
    test_every_gate_has_required_fields()
    test_pipeline_required_gates_registered()
    test_no_real_trade_gate_registered()
    test_z9_preview_only_gate_registered()
    test_rc_gates_registered()
    test_rmatrix_cycle_gate_registered()
    test_gate_registry_integrity_clean()
    test_get_gates_for_pipeline_api()
    test_rc_release_gates()
    test_gate_type_diversity()
    print("\n🏁 Gate Registry v1.0 — all F-3 tests PASS")
