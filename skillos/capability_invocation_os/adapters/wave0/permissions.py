"""Wave0 permissions — write/production/broker/real_trade all denied."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Permission
def check_permission(requested): return False if requested in (Wave0Permission.DENY,) else False
