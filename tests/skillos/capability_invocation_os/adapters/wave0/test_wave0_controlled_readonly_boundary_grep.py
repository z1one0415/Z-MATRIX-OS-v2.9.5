import pytest, os
W=os.path.join(os.path.dirname(__file__),'..','..','..','..','..','skillos','capability_invocation_os','adapters','wave0')
F=['requests','urllib','httpx','socket','z2','z8','z9','v3','worldblocks','dealcompass']
def test_no_forbidden():
    if not os.path.isdir(W): pytest.skip()
    for f in os.listdir(W):
        if not f.endswith('.py') or f.startswith('__'): continue
        with open(os.path.join(W,f)) as fh:
            c=fh.read()
        for fb in F:
            if f"import {fb}" in c or f"from {fb}" in c:
                if 'FORBIDDEN' not in c.split(f"import {fb}")[0].split('\n')[-1]:
                    assert False,f"'{fb}' in {f}"
