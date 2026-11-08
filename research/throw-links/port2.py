from pathlib import Path
import sys,json
s=Path('work/throw-links/audit.py').read_text().split('try:\n for cid in requested:')[0].replace("P=Path('work/throw-links')","P=Path('work/throw-links/port2')").replace("'work/barrage-roster/candidate.bin'","'work/throw-links/candidate.bin'");sys.argv=['audit','0'];exec(compile(s,'throw-p2','exec'),globals());P1,P2=P2,P1;raw_tick=tick
def tick(a=(),b=()):raw_tick(b,a)
try:
 reports=[]
 for cid in range(11):
  seed=Path(f'work/throw-links/seeds-p2/{cid}.state').read_bytes();best=json.loads(Path(f'work/throw-links/after/report-{cid}.json').read_text())['earliestUsefulDelay'];cases=[run_case(cid,seed,0,throwOnly=True)]
  for delay in sorted(set([0,best,120])):
   for guard in [False,True]:cases.append(run_case(cid,seed,delay,guard=guard))
  d=dict(cid=cid,cases=cases);reports.append(d);(P/f'report-{cid}.json').write_text(json.dumps(d,indent=2));print('P2',cid,[(x['delay'],x['guard'],x['totalDamage'],x['maxHits']) for x in cases],flush=True)
 (P/'summary.json').write_text(json.dumps(reports,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
