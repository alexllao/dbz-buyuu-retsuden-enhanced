from pathlib import Path
import sys
src=Path('work/throw-links/audit.py').read_text().replace("P=Path('work/throw-links')","P=Path('work/throw-links/after')").replace("'work/barrage-roster/candidate.bin'","'work/throw-links/candidate.bin'").replace("seedPath=P/f'seeds/{cid}.state'","seedPath=Path(f'work/throw-links/seeds/{cid}.state')")
src=src.replace('for delay in [0,12,24,36,48,64,80,100,120]:','for delay in ([0,12,24,36,48,64,68,72,76,80,100,120] if cid==0 else [0,12,24,36,48,64,80,100,120]):')
exec(compile(src,'throw-audit-after','exec'),globals())
