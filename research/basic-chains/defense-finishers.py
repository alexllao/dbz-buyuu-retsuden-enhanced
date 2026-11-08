from pathlib import Path
import sys,json
variant=sys.argv[1];s=Path('work/basic-chains/finishers.py').read_text();s=s.replace("for speed in [2,3,4]:","for speed in [3]:").replace('tick(k);now=rw(P2+0x24)',"tick(k,['RIGHT'] if len(contacts)>=3 else []);now=rw(P2+0x24)")
s=s.replace("f'{variant}-finisher-{kind}-{speed}.json'","f'{variant}-guard-finisher-{kind}-{speed}.json'").replace("f'{variant}-finishers.json'","f'{variant}-guard-finishers.json'")
exec(compile(s,'chain-guard-remate','exec'),globals())
