from pathlib import Path
import sys
src=Path('work/knockdown-k4/record.py').read_text().replace('range(230)','range(300)').replace("root=baseDir/'work/knockdown-k4/comparison'/which","root=baseDir/'work/knockdown-k4/comparison/long'/which")
sys.argv=['record','after'];exec(compile(src,'record-long','exec'),globals())
