class RuntimeKillSwitch:
    def __init__(self): self.master_disable=True; self.registry_disable=True; self.router_disable=True; self.composition_disable=True; self.evidence_write_disable=True; self.guard_disable=True; self.adapter_disable=True; self.capability_execution_disable=True
    def disable_all(self):
        for a in vars(self): setattr(self,a,True)
    def overrides_runtime_requested(self,config):
        return self.master_disable or self.guard_disable or self.capability_execution_disable
kill_switch = RuntimeKillSwitch()
