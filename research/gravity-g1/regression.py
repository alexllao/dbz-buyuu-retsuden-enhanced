from pathlib import Path
import sys,json
prefix=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/gravity-probe/gravity-g1.bin'")
sys.argv=['probe','after','0'];exec(compile(prefix,'gravity-check','exec'),globals())
report=[]
try:
 for cid in range(11):
  for actor in [P1,P2]:
   for mode in ['air-A','air-B','vertical','run','single','opposite','expired']:
    restore(Path(f'work/gravity-probe/seed-{cid}.state').read_bytes());ww(actor+0xa,200 if actor==P1 else 500)
    fwd='RIGHT' if actor==P1 else 'LEFT';back='LEFT' if fwd=='RIGHT' else 'RIGHT'
    seq={'air-A':[['UP']]*3+[[]]*10+[['A']]*3,'air-B':[['UP']]*3+[[]]*10+[['B']]*3,'vertical':[['UP']]*3,'run':[[fwd]]*4+[[]]*4+[[fwd]]*12+[['UP',fwd]]*3,'single':[[fwd]]*30,'opposite':[[fwd]]*4+[[]]*4+[[back]]*10,'expired':[[fwd]]*4+[[]]*40+[[fwd]]*10}[mode]
    rr=[]
    for k in seq+[[]]*180:
     tick(k if actor==P1 else [],k if actor==P2 else []);rr.append(dict(y=rw(actor+0x10),p=rw(actor),a=rb(actor+0x5b)))
    landed=rr[-1]['y']==448 and rr[-1]['a']==0
    assert landed,(cid,actor,mode,rr[-1])
    ran=any(t['a'] in [7,8] for t in rr)
    if mode=='run':assert ran
    if mode in ['single','opposite','expired']:assert not ran,(cid,actor,mode)
    report.append(dict(seedCid=cid,actorCid=rb(actor+0x58),actor=hex(actor),mode=mode,landed=landed,ran=ran,maxYStep=max(abs(a['y']-b['y']) for a,b in zip(rr,rr[1:]))))
 Path('work/gravity-probe/regression.json').write_text(json.dumps(report,indent=2));print('PASS',len(report),'cases', 'largest Y step',max(t['maxYStep'] for t in report),flush=True)
finally:core.retro_unload_game();core.retro_deinit()
