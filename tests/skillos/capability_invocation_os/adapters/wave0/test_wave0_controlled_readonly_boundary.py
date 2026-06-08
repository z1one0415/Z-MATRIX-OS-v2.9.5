import pytest
from skillos.capability_invocation_os.adapters.wave0.boundary import (
    assert_no_controlled_readonly_side_effects,
    assert_no_real_adapter_call, assert_no_network,
    assert_no_file_write, assert_no_zmatrix, assert_no_production,
)

def test_all_boundary_proofs_pass():
    proofs = assert_no_controlled_readonly_side_effects()
    assert all(p.passed for p in proofs)
    proofs = assert_no_real_adapter_call()
    assert all(p.passed for p in proofs)
    proofs = assert_no_network()
    assert all(p.passed for p in proofs)
    proofs = assert_no_file_write()
    assert all(p.passed for p in proofs)
    proofs = assert_no_zmatrix()
    assert all(p.passed for p in proofs)
    proofs = assert_no_production()
    assert all(p.passed for p in proofs)

def test_boundary_never_raises():
    try:
        assert_no_controlled_readonly_side_effects()
        assert_no_real_adapter_call()
        assert_no_network()
        assert_no_zmatrix()
        assert_no_production()
    except Exception as e:
        pytest.fail(f"Boundary raised: {e}")
