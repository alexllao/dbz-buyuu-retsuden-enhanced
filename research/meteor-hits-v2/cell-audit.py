from pathlib import Path
import sys,json
s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/meteor-hits/candidate.bin'");sys.argv=['probe','after','5'];exec(compile(s,'cell-counter-audit','exec'),globals());report=[];P=Path('work/meteor-hits')
try:
 for style in ['stand','crouch']:
  for frames in [0,90,120,150,180,210,240,300,390]:
   restore(Path('work/piccolo-hits/routes/5/low-hp.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   prev=rw(P2+0x24);drops=[];rr=[];dirs=[['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']];seq=[k for k in dirs for _ in range(3)]+[dirs[-1]+['B']]*4
   for i,k in enumerate(seq+[[]]*1100):
    enemy=(['RIGHT'] if style=='stand' else ['DOWN','RIGHT']) if i<frames else [];tick(k,enemy);now=rw(P2+0x24)
    if now<prev:drops.append(dict(frame=i,damage=prev-now,hits=rb(P1+0xd20)&127))
    prev=now;rr.append(dict(frame=i,p=st(P1),e=st(P2),keys=k,keys2=enemy))
   result=dict(style=style,guardFrames=frames,maxHits=max(t['p']['hits'] for t in rr),realContacts=sum(x['damage']==6 for x in drops),blockedChip=sum(x['damage'] for x in drops if x['damage']!=6),drops=drops);assert result['maxHits']==result['realContacts'],result;report.append(result);print(style,frames,'hits',result['maxHits'],'real',result['realContacts'],'chip',result['blockedChip'],flush=True)
   if result['maxHits'] in [11,13]:(P/f'cell-{style}-{frames}.json').write_text(json.dumps(rr))
 (P/'cell-audit.json').write_text(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
