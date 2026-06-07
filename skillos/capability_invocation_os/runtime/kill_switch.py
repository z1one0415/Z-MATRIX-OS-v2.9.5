"""Kill switch — all components disabled by default."""
class KillSwitch:
    def __init__(self):
        self.master_disable = True
        self.registry_disable = True
        self.router_disable = True
        self.composition_disable = True
        self.evidence_write_disable = True
        self.guard_disable = True
        self.adapter_disable = True

    def disable_all(self):
        for attr in vars(self):
            setattr(self, attr, True)

kill_switch = KillSwitch()
