"""Wave0 kill switch — all disabled by default, overrides config."""
class Wave0KillSwitch:
    def __init__(self): self.master=True; self.github=True; self.docgen=True; self.docs=True; self.report=True; self.evidence=True
    def disable_all(self):
        for a in vars(self): setattr(self,a,True)
    def overrides(self,c): return self.master or self.github or self.docgen or self.docs or self.report
ks = Wave0KillSwitch()
