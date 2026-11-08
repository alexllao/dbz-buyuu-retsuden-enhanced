from pathlib import Path
import sys
name=sys.argv[1];port2=len(sys.argv)>2
s=Path('work/basic-chains',name+'.py').read_text(encoding='utf-8')
anchor="exec(compile(s,"
s=s.replace(anchor,"s=s.replace('work/basic-chains/candidate.bin','work/input-links/candidate.bin').replace(\"P=Path('work/basic-chains')\",\"P=Path('work/input-links')\");exec(compile(s,",1)
sys.argv=['regression','after']+(['port2'] if port2 else [])
exec(compile(s,'new-buffer-basic-regression','exec'),globals())
