from pathlib import Path
import sys,json
P=Path('work/jump-two');P.mkdir(exist_ok=True);variant=sys.argv[1];which=variant;rompath='work/barrage-roster/candidate.bin' if which=='before' else f'work/jump-two/{which}.bin'
s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'",f"rompath='{rompath}'");sys.argv=['probe','after','0'];exec(compile(s,'jump-probe','exec'),globals())
which=variant
try:
 report=[]
 for label,seq in [('vertical',[['UP']]*3),('diagonal',[['UP','RIGHT']]*3),('run',[['RIGHT']]*4+[[]]*4+[['RIGHT']]*12+[['UP','RIGHT']]*3),('backrun',[['LEFT']]*4+[[]]*4+[['LEFT']]*12+[['UP','LEFT']]*3)]:
  restore(Path('work/barrage-roster/seeds/0-0.state').read_bytes());ww(P1+0xa,420 if label=='backrun' else 100);ww(P2+0xa,700);ww(P1+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(20):tick()
  r=[]
  for f,k in enumerate(seq+[[]]*170):tick(k);r.append(dict(f=f,x=rw(P1+0xa),y=rw(P1+0x10),program=rw(P1),action=rb(P1+0x5b),cursor=rw(P1+6),flags=rw(P1+0x20)))
  air=[t for t in r if t['y']<448];first=next(t['f'] for t in r if t['y']<448);land=next(t['f'] for t in r[first+1:] if t['y']==448);result=dict(label=label,height=448-min(t['y'] for t in r),airFrames=land-first,takeoff=first,landing=land,airRange=abs(r[land]['x']-r[max(0,first-1)]['x']),totalRange=max(t['x'] for t in r)-min(t['x'] for t in r),run=any(t['action'] in [7,8] for t in r));report.append(result);(P/f'{which}-{label}.json').write_text(json.dumps(r))
 print(which,report,flush=True);(P/f'{which}-summary.json').write_text(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
