"""Wave0 Config — all enabled returns False. Strict True only requested."""
class Wave0Config:
    def __init__(self,s=None):
        self._wave0=False; self._github=False; self._docgen=False; self._docs=False; self._report=False
        if isinstance(s,dict):
            for a,k in [("_wave0","WAVE0_READONLY_ADAPTERS_ENABLED"),("_github","WAVE0_GITHUB_READONLY_ENABLED"),("_docgen","WAVE0_DOCUMENT_GENERATION_ENABLED"),("_docs","WAVE0_LOCAL_DOCS_INSPECTION_ENABLED"),("_report","WAVE0_REPORT_READING_ENABLED")]:
                v=s.get(k,False); setattr(self,a,v if isinstance(v,bool) and v is True else False)
def load(s=None): return Wave0Config(s) if isinstance(s,dict) else Wave0Config()
def is_wave0_enabled(c): return False
def is_github_readonly_enabled(c): return False
def is_document_generation_enabled(c): return False
def is_local_docs_inspection_enabled(c): return False
def is_report_reading_enabled(c): return False
def env_override(): return False
