import pytest
from skillos.capability_invocation_os.adapters.wave0.config import is_controlled_readonly_enabled, Wave0ExecutionConfig
def test_env_cannot_enable():
    assert is_controlled_readonly_enabled(Wave0ExecutionConfig()) is False
def test_requested_still_disabled():
    cfg = Wave0ExecutionConfig()
    assert is_controlled_readonly_enabled(cfg) is False
