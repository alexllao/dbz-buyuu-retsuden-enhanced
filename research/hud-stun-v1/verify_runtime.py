from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);tag=sys.argv[3];port=1;turbo=False;out=ROOT/'work/stun-hud/verification'/f'{tag}-{cid}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'timing-setup','exec'),globals())
try:
 for index,step in enumerate(steps[:-1]):
  if index==9:
   for direction,count in [('DOWN',cid//3),('RIGHT',cid%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(step.get('frames',1)):tick([] if index==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 resources=Path('work/stun-hud/resources.bin').read_bytes();samples=[];previous=None;previousObserved=None;clockBefore=rw(0xe6a8)
 def wanted():
  result=[]
  for b in [P1,P2]:
   timer=rw(b+0x36);den=(360*rw(0xe758))>>8 if timer else rb(b+0x54);value=timer if timer else rb(b+0x51);fill=min(30,value*30//den) if den else 0;mode=2 if timer else 1 if fill>=23 else 0;result.append((mode*31+fill)*64)
  a,b=result;return b''.join(resources[a+i*16:a+i*16+16]+b''.join(resources[b+i*16+j:b+i*16+j+4] for j in [12,8,4,0]) for i in range(4))
 for f in range(1200):
  # Both auras, native jump and two directional attacks: ordinary input only.
  if f<300:k=['A','B'];other=['A','B']
  elif f<380:k=[];other=[]
  elif f<400:k=['UP'];other=['UP']
  elif f<520:k=[];other=[]
  elif f<550:k=['RIGHT'];other=['LEFT']
  elif f<556:k=['A'];other=[]
  elif 650<=f<656:k=[];other=['B']
  elif 800<=f<804:k=['LEFT'];other=[]
  elif 804<=f<808:k=['DOWN','LEFT'];other=[]
  elif 808<=f<812:k=['DOWN'];other=[]
  elif 812<=f<816:k=['DOWN','RIGHT'];other=[]
  elif 816<=f<820:k=['RIGHT'];other=[]
  elif 820<=f<824:k=['RIGHT','B'];other=[]
  else:k=[];other=[]
  expected=wanted();clockBefore=rw(0xe6a8);tick(k,other);clockAdvanced=rw(0xe6a8)!=clockBefore

  s=snap();v=s[0x12425:0x22425];v=bytes(x for i in range(0,len(v),2) for x in [v[i+1],v[i]])
  observed=v[0xaf20:0xafa0];head=v[0xac00:0xac08];n=rb(0xe452);collisions=[i for i in range(min(n,80)) if 0x579<=(rw(0xe04e+i*8+4)&0x7ff)<0x580]
  checks={'barsMatchNativeReadout':(observed in [expected,wanted(),previous] if clockAdvanced else previousObserved is None or observed==previousObserved),'nativePatternsDoNotUseHudTiles':not collisions,'nativeSatHasRoom':n<=78,'hudHeadVisible':head[:2]==bytes.fromhex('015c')}
  if not checks['barsMatchNativeReadout']:(out/f'mismatch-{f}.json').write_text(json.dumps({'observed':observed.hex(),'before':expected.hex(),'now':wanted().hex(),'previous':previous.hex() if previous else '', 'thresholds':[rb(P1+0x54),rb(P2+0x54)]}),encoding='utf8')
  if f%12==0:samples.append({'f':f,'renderAdvanced':clockAdvanced,'checks':checks,'nativeSpriteCount':n,'hudHead':head.hex(),'stun':[rb(P1+0x51),rb(P2+0x51)],'timers':[rw(P1+0x36),rw(P2+0x36)]})
  previous=expected;previousObserved=observed
 report={'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'frames':1200,'fixture':'Both human actors, native menus/positions/HP/ki/timers; actual charging/jump/attack commands only','passed':all(all(x['checks'].values()) for x in samples),'samples':samples};(out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(cid,report['passed'],[x for x in samples if not all(x['checks'].values())][:3]);assert report['passed']
finally:core.retro_unload_game();core.retro_deinit()
