from pathlib import Path
s=Path('work/control-audit/trace-link.py').read_text(encoding='utf-8')
s=s.replace("exec(compile(s,", "s=s.replace('work/basic-chains/candidate.bin','work/input-links/candidate.bin');exec(compile(s,",1)
s=s.replace('work/control-audit/link-kame','work/input-links/link-kame')
exec(compile(s,'trace-new-buffer','exec'),globals())
