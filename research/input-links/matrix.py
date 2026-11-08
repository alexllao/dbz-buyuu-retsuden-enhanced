from pathlib import Path
import json,sys
audit_variant=sys.argv[1];p=Path('work/input-links')
s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];sys.argv=['probe','after']
rompath='work/basic-chains/candidate.bin' if audit_variant=='before' else 'work/input-links/candidate.bin'
s=s.replace('work/basic-chains/candidate.bin',rompath);exec(compile(s,'link-matrix-header','exec'),globals());results=[]
try:
 for port in [0,1]:
  actor,enemy=(P1,P2) if port==0 else (P2,P1)
  for side in [0,1]:
   for speed in [2,3,4,5,6]:
    for delay in [0,3,6]:
     for kind,button,repeats,expected in [('kame',['A'],1,0xc04),('super',['A'],2,0xc05),('meteor',['A','B'],2,0x83e)]:
      restore(p.joinpath('charged.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(actor+0xa,300 if side==0 else 332);ww(enemy+0xa,332 if side==0 else 300);wb(actor+0x59,side);wb(enemy+0x59,1-side)
      for _ in range(8):tick()
      rows=[];hits=[];hp=rw(enemy+0x24)
      def step(k=()):
       global hp
       tick(k if port==0 else [],k if port==1 else []);now=rw(enemy+0x24)
       if now<hp:hits.append(len(rows))
       hp=now;rows.append(dict(f=len(rows),program=rw(actor),enemyAction=rb(enemy+0x5b),hp=now,hits=rb(actor+0xd20)&127,token=rb(actor+0xb9),queueTTL=rb((0xf720 if port==0 else 0xf730)+14)))
      for f in range(120):
       k=['A'] if f<3 else []
       for i,t in enumerate(hits[:2]):
        if t+3<=f<t+6:k=[['A','B'][i]]
       step(k)
       if len(hits)>=3:break
      for _ in range(delay):step()
      dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]*repeats
      if side:dirs=[[{'LEFT':'RIGHT','RIGHT':'LEFT'}.get(v,v) for v in k] for k in dirs]
      for k in [k for k in dirs for _ in range(speed)]+[dirs[-1]+button]*3:step(k)
      for _ in range(380):step()
      result=dict(port=port,side=side,speed=speed,delay=delay,kind=kind,started=any(t['program']==expected for t in rows),programs=sorted(set(t['program'] for t in rows)),damage=200-hp,maxHits=max(t['hits'] for t in rows),queueSeen=any(t['queueTTL'] for t in rows));results.append(result)
      if side==0 and port==0 and kind=='kame' and delay==3 and speed==4:p.joinpath(f'{audit_variant}-critical-trace.json').write_text(json.dumps(rows))
   print(audit_variant,port,side,'started',sum(t['started'] for t in results if t['port']==port and t['side']==side),'of',sum(t['port']==port and t['side']==side for t in results),flush=True)
 p.joinpath(f'{audit_variant}-matrix.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()
