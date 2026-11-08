from pathlib import Path
import sys
s=Path('work/barrage-five/extra.py').read_text().replace("P=Path('work/barrage-five')","P=Path('work/barrage-roster')").replace("'work/barrage-five/candidate.bin'","'work/barrage-roster/candidate.bin'")
exec(compile(s,'roster-negative','exec'),globals())
