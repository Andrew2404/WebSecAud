#!/usr/bin/env python3
"""Create a private draft covering every catalog control. This is not a runner."""
import json
from pathlib import Path
import sys
from validate_ledger import ROOT, fresh_record, validate

def generate():
    draft=json.loads((ROOT/'templates/test-plan-ledger.json').read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'references/controls.json').read_text(encoding='utf-8'))
    draft['scope']['catalogVersion']=catalog['version']
    draft['tests']=[fresh_record(c) for c in catalog['controls']]
    assert validate(draft)['valid']
    return draft

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/new_ledger.py private-audits/test-plan.json')
    destination=Path(sys.argv[1]); destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('x',encoding='utf-8') as out: json.dump(generate(),out,indent=2);out.write('\n')
    print('Created draft ledger. All cases are Planned/Unreviewed; caps are zero and active testing is blocked. No requests sent.')
