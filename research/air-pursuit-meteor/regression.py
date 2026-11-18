"""Repite la auditoría de ki existente sin persecución, sobre padre y candidata."""
from pathlib import Path
import sys
variant,port=sys.argv[1:]
target='work/air-pursuit/candidate.bin' if variant=='parent' else 'work/air-pursuit-fall/candidate.bin'
s=Path('work/combo-charge-all/roster.py').read_text()
s=s.replace("setup=Path('work/combo-charge-all/runtime.py').read_text()",f"setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','{target}').replace(\"if variant=='after':\",\"if True:\")")
s=s.replace("results=[]",f"results=[]; assert hashlib.sha256(rom).hexdigest()==hashlib.sha256(Path('{target}').read_bytes()).hexdigest()",1)
out=Path('work/air-pursuit-fall/regression');out.mkdir(exist_ok=True)
s=s.replace("(S/f'roster-","(Path('work/air-pursuit-fall/regression')/f'roster-")
sys.argv=['regression',variant,port];exec(compile(s,'meteor-regression','exec'),globals())

