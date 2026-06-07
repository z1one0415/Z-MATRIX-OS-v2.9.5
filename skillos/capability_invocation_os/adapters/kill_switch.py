"""AdapterKillSwitch — all disabled by default, overrides config, no Z-MATRIX imports."""
class AdapterKillSwitch:
    def __init__(self): self.master_disable=True; self.registration_disable=True; self.execution_disable=True; self.module_adapter_disable=True; self.evidence_write_disable=True
    def disable_all(self):
        for a in vars(self): setattr(self,a,True)
    def overrides_requested(self,config): return self.master_disable or self.execution_disable or self.module_adapter_disable
kill_switch = AdapterKillSwitch()
