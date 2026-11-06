from pathlib import Path
import sys,json
variant=sys.argv[1];cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
prefix=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/gravity-g2/candidate.bin'")
sys.argv=['probe','after',str(cid)];exec(compile(prefix,'gravity-test','exec'),globals())
try:
 seed=Path(f'work/gravity-probe/seed-{cid}.state').read_bytes();report=[]
 for label,seq in [('vertical',[['UP']]*3),('forward',[['UP','RIGHT']]*3),('running',[['RIGHT']]*4+[[]]*4+[['RIGHT']]*12+[['UP','RIGHT']]*3),('backrun',[['LEFT']]*4+[[]]*4+[['LEFT']]*12+[['UP','LEFT']]*3)]:
  restore(seed);rr=[]
  for i,k in enumerate(seq+[[]]*190):
   tick(k);rr.append(dict(f=i,x=rw(P1+0xa),y=rw(P1+0x10),program=rw(P1),action=rb(P1+0x5b),cursor=rw(P1+6),flags=rw(P1+0x20),ttl=rb(0xf742)))
  jumps=[t for t in rr if t['y']<448]
  summary=dict(label=label,height=448-min(t['y'] for t in rr),airFrames=len(jumps),run=any(t['action'] in [7,8] for t in rr),flags=sorted(set(t['flags'] for t in jumps)),programs=sorted(set(t['program'] for t in rr)),range=max(t['x'] for t in rr)-min(t['x'] for t in rr));report.append(summary)
  Path(f'work/gravity-g2/{variant}-{cid}-{label}.json').write_text(json.dumps(rr))
 print(variant,cid,report,flush=True);Path(f'work/gravity-g2/{variant}-{cid}-summary.json').write_text(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
