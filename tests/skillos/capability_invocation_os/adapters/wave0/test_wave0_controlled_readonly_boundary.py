import pytest
from skillos.capability_invocation_os.adapters.wave0.boundary import assert_no_controlled_readonly_side_effects, assert_no_real_adapter_call, assert_no_network, assert_no_file_write, assert_no_zmatrix, assert_no_production
def test_all_pass():
    assert all(p.passed for p in assert_no_controlled_readonly_side_effects())
    assert all(p.passed for p in assert_no_real_adapter_call())
    assert all(p.passed for p in assert_no_network())
    assert all(p.passed for p in assert_no_file_write())
    assert all(p.passed for p in assert_no_zmatrix())
    assert all(p.passed for p in assert_no_production())
def test_never_raises():
    try:
        assert_no_controlled_readonly_side_effects(); assert_no_real_adapter_call(); assert_no_network()
        assert_no_file_write(); assert_no_zmatrix(); assert_no_production()
    except: pytest.fail("Boundary raised")
