from pathlib import Path
import sys,json
src=Path('work/knockdown-k4/record.py').read_text()
src=src.replace("rompath='work/knockdown-k4/candidate.bin'", "rompath='work/rom/original.bin'")
src=src.replace("if False:","if True:").replace("work/knockdown-k2/seeds/", "work/knockdown-k4/original-seeds/")
src=src.replace('range(230)','range(300)')
sys.argv=['record','original'];exec(compile(src,'record-original','exec'),globals())
