#!/usr/bin/env python3
"""Validate package consistency, links, catalog and reproducible HTML. No network."""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import urlparse
from build_html import build, validate_catalog

root=Path(__file__).resolve().parent.parent
catalog_path=root/'references/controls.json'
catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
validate_catalog(catalog)
assert re.fullmatch(r'\d+\.\d+\.\d+', catalog['version'])
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', catalog['checked'])
controls=catalog['controls']
sources=catalog['sources']
assert len(controls)==len({c['id'] for c in controls})
assert len(sources)==len({s['id'] for s in sources})
for c in controls:
    assert re.fullmatch(r'[A-Z]+-\d{2}',c['id']), c['id']
    assert set(c)=={'id','domain','title','priority','applicability','verify','pass','evidence','sourceIds'},c['id']
    for k in ['domain','title','applicability','verify','pass','evidence']:
        assert isinstance(c[k],str) and c[k].strip(), (c['id'],k)
for s in sources:
    u=urlparse(s['url'])
    assert u.scheme=='https' and u.netloc and not u.username and not u.password,s['id']
    assert s['checked']==catalog['checked'],s['id']

# Relative Markdown links must point to bundled files; web sources are not fetched.
links=0
for p in root.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if '://' in link or link.startswith('#'): continue
        target=(p.parent/link.split('#',1)[0]).resolve()
        assert target.is_relative_to(root.resolve()), (p,link,'outside package')
        assert target.is_file(),(p,link,'missing')
        links+=1

html=(root/'assets/security-audit.html').read_bytes()
with tempfile.TemporaryDirectory(prefix='security-audit-build-') as folder:
    rebuilt=Path(folder)/'audit.html'
    with contextlib.redirect_stdout(io.StringIO()): build(catalog_path,rebuilt)
    assert rebuilt.read_bytes()==html,'HTML is stale; rebuild it'
text=html.decode('utf-8')
assert '__CATALOG__' not in text and '__SCRIPT__' not in text
assert 'innerHTML' not in text and 'document.write' not in text
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=[\"\']https?://',text,re.I),'external executable/style dependency'
assert 'connect-src \'none\'' in text
for forbidden in ['.env','.pem','.p12','.key']:
    assert not list(root.rglob('*'+forbidden)), 'Potential secret file in package'
print(json.dumps({'result':'PASS','controls':len(controls),'source_records':len(sources),'local_links':links,'html_bytes':len(html),'html_sha256':hashlib.sha256(html).hexdigest(),'checks':['catalog schema and references','bundled Markdown links','deterministic HTML rebuild','offline rendering dependency checks','unsafe DOM sink absence','secret-file extension exclusion']},indent=2))
