from pathlib import Path
import sys
variant=sys.argv[1];rompath='work/barrage-roster/candidate.bin' if variant=='before' else 'work/throw-links/candidate.bin';s=Path('work/meteor-hits/roster.py').read_text().replace("rompath='work/meteor-hits/candidate.bin'",f"rompath='{rompath}'").replace("P=Path('work/meteor-hits')",f"P=Path('work/throw-links/meteors/{variant}');P.mkdir(parents=True,exist_ok=True)")
exec(compile(s,'throw-meteor-regression','exec'),globals())
