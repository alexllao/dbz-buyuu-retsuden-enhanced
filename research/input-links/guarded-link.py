from pathlib import Path
s=Path('work/control-audit/trace-link.py').read_text(encoding='utf-8')
s=s.replace("exec(compile(s,", "s=s.replace('work/basic-chains/candidate.bin','work/input-links/candidate.bin');exec(compile(s,",1)
s=s.replace('tick(k);now=', "tick(k,['RIGHT'] if len(contacts)>=3 else []);now=")
s=s.replace('work/control-audit/link-kame','work/input-links/guard-kame')
exec(compile(s,'guard-after-third-buffer','exec'),globals())
