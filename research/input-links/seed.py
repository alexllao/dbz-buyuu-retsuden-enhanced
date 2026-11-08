from pathlib import Path
import sys
s=Path('work/input-v2/test-chords.py').read_text(encoding='utf-8').split(' charged=snap();results=[]')[0]
s=s.replace("rompath='work/input-v2/candidate.bin'", "rompath='work/input-links/candidate.bin'")
s += " Path('work/input-links/charged.state').write_bytes(snap())\nfinally:core.retro_unload_game();core.retro_deinit()\n"
sys.argv=['seed','after','0'];exec(compile(s,'seed-goku-mirror','exec'),globals())
