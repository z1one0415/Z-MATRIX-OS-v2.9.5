import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledReadonlyDecision
def test_no_envelope():
    d=ControlledReadonlyDecision()
    assert not hasattr(d,'result_envelope'); assert not hasattr(d,'caller_visible_message'); assert not hasattr(d,'execute')
