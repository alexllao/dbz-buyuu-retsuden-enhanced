from pathlib import Path
import sys,json
port=int(sys.argv[1]);prefix=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/gravity-g2/candidate.bin'")
sys.argv=['probe','after','0'];exec(compile(prefix,'g2-test','exec'),globals())
try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=(0 if j==9 else 3) if port==1 else (3 if j==9 else 0)
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 actor=P1 if port==1 else P2;assert rb(actor+0x58)==0;seed=snap();reports=[]
 for facing in [0,1]:
  for mode in ['normal','diagonal','run','airA','airB']:
   restore(seed);ww(actor+0xa,300);other=P2 if port==1 else P1;ww(other+0xa,500 if facing==0 else 100);wb(actor+0x59,facing);wb(other+0x59,1-facing)
   fwd='RIGHT' if facing==0 else 'LEFT';seq=[['UP']]*3 if mode in ['normal','airA','airB'] else [['UP',fwd]]*3
   if mode=='run':seq=[[fwd]]*4+[[]]*4+[[fwd]]*12+seq
   if mode.startswith('air'):seq+=[[]]*10+[[mode[-1]]]*3
   rr=[]
   for k in seq+[[]]*170:
    tick(k if port==1 else [],k if port==2 else []);rr.append(dict(y=rw(actor+0x10),a=rb(actor+0x5b),program=rw(actor)))
   result=dict(port=port,facing=facing,mode=mode,height=448-min(t['y'] for t in rr),airFrames=sum(t['y']<448 for t in rr),landed=rr[-1]['y']==448 and rr[-1]['a']==0,maxYStep=max(abs(a['y']-b['y']) for a,b in zip(rr,rr[1:])))
   assert result['landed'] and result['maxYStep']<20,result
   if mode in ['normal','diagonal']:assert result['height']==61
   if mode=='run':assert result['height']==138
   reports.append(result)
 Path(f'work/gravity-g2/validation-port{port}.json').write_text(json.dumps(reports,indent=2));print('PASS',reports,flush=True)
finally:core.retro_unload_game();core.retro_deinit()
