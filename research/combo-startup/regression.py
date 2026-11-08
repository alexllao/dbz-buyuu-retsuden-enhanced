from pathlib import Path
s=Path('work/control-audit/run.py').read_text(encoding='utf-8').replace('work/basic-chains/candidate.bin','work/combo-startup/candidate.bin').replace("root=Path('work/control-audit')","root=Path('work/combo-startup')")
exec(compile(s,'combo-startup-input-regression','exec'),globals())
