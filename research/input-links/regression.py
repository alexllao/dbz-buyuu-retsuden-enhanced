from pathlib import Path
import sys
name=sys.argv[1]
s=Path('work/control-audit/run.py').read_text(encoding='utf-8')
s=s.replace("source=source.replace(\"rompath='work/input-v2/candidate.bin'\", \"rompath='work/basic-chains/candidate.bin'\")", "source=source.replace(\"rompath='work/input-v2/candidate.bin'\", \"rompath='work/input-links/candidate.bin'\")")
s=s.replace("root=Path('work/control-audit')", "root=Path('work/input-links')")
exec(compile(s,'input-link-regression','exec'),globals())
