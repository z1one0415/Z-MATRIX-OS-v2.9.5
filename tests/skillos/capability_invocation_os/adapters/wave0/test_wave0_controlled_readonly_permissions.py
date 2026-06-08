import pytest
from skillos.capability_invocation_os.adapters.wave0.permissions import validate_controlled_readonly_permission
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind
def test_all_permissions_denied():
    for kind in Wave0AdapterKind:
        for ik in ControlledInputKind:
            assert validate_controlled_readonly_permission(kind, ik, "READ") is False
