from pathlib import Path
import sys
s=Path('work/barrage-roster/test.py').read_text().replace("'work/barrage-roster/candidate.bin'","'work/jump-two/candidate.bin'").replace("P=Path('work/barrage-roster')/","P=Path('work/jump-two')/")
sys.argv=['test','after','quick'];exec(compile(s,'jump-barrage-check','exec'),globals())
