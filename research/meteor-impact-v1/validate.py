from pathlib import Path
import sys,json
s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/meteor-impact/candidate.bin'")
sys.argv=['probe','after','0'];exec(compile(s,'impact-verify','exec'),globals());P=Path('work/meteor-impact');report=[];damage=[35,34,43,49,40,78,33,32,32,36]
try:
 for cid in range(10):
  folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full';state='low-hp.state' if cid in [3,5] else 'charged.state'
  for face in [0,1]:
   for mode in ['hit','guard','whiff']:
    restore(Path(f'work/{folder}/routes/{cid}/{state}').read_bytes());distance=200 if mode=='whiff' else 32;ww(P1+0xa,300+distance if face else 300);ww(P2+0xa,300 if face else 300+distance);wb(P1+0x59,face);wb(P2+0x59,1-face);f='LEFT' if face else 'RIGHT';b='RIGHT' if face else 'LEFT'
    for _ in range(8):tick([],[f] if mode=='guard' else [])
    hp=rw(P2+0x24);hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]];hcb=[[f],['DOWN',f],['DOWN'],['DOWN',b],[b]];dirs=hcf*2 if cid==0 else [['DOWN'],['DOWN',f],[f],[b]] if cid==5 else hcb+[[f]] if cid in [1,3,4,7,9] else hcf+[[b]];btn=['A','B'] if cid==0 else ['B'];rr=[]
    for k in [k for k in dirs for _ in range(3)]+[dirs[-1]+btn]*4+[[]]*1100:
     tick(k,[f] if mode=='guard' else []);rr.append(dict(y=rw(P1+0x10),events=rw(0xf768),dx=rw(0xf766),p=rw(P1),e=rw(P2),hp=rw(P2+0x24),paused=rb(0xe744)))
    result=dict(cid=cid,facing=face,mode=mode,events=rw(0xf768),damage=hp-rw(P2+0x24),hit=max(t['events'] for t in rr)>0,end=[rw(P1),rw(P2)],dxEnd=rw(0xf766));assert result['dxEnd']==0,result
    if mode=='hit':assert result['damage']==damage[cid] and result['hit'],result
    if result['damage']==0:assert result['events']==0,result
    report.append(result)
 print('PASS',len(report),'cases','zero damage',sum(t['damage']==0 for t in report),flush=True);(P/'validation-cases.json').write_text(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
