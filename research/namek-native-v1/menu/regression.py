from pathlib import Path
import sys,json,hashlib
s=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');sys.argv=['probe','--rom','work/namek-native/integrated.bin'];exec(compile(s,'regression-runtime','exec'),globals())
O=Path('work/namek-menu');checks=[]
def press(k,n=3,k2=(),idle=120):
 for _ in range(n):tick(k,k2)
 for _ in range(idle):tick()
def cur():return dict(state=rw(0xe6a4),phase=rw(0xe750),stage=rb(0xe741),variant=rb(0xf7c0),hp=[rw(P1+0x24),rw(P2+0x24)],mode=rw(0xe9e8))
def bootMenu(mode=0):
 core.retro_reset()
 for entry in steps[:7]:
  for _ in range(entry.get('frames',1)):tick(entry.get('buttons',[]))
 for _ in range(mode):press(['RIGHT'],idle=20)
 press(['C'],idle=20)
 for f in range(2400):
  if rw(0xe6a4)==0x20 and rw(0xe750)==3:break
  tick(['C'] if f%120<3 else [],['C'] if mode==1 and f%120<3 else [])
 assert rw(0xe6a4)==0x20 and rw(0xe750)==3
try:
 bootMenu(1);press(['DOWN'],idle=20);cycle=[cur()]
 for i in range(12):press(['A']);cycle.append(cur())
 expected=[(i,0) for i in range(9)]+[(6,1),(6,2),(6,3),(0,0)]
 assert [(t['stage'],t['variant']) for t in cycle]==expected,cycle
 checks.append(dict(name='all12_forward_and_wrap',passed=True,states=cycle));print('CYCLE PASS',flush=True)
 for i in range(6):press(['A'])
 assert (rb(0xe741),rb(0xf7c0))==(6,0);save_image(O/'original-namek-selected.png')
 # Exact original graphics in the native background allocation.
 sys.path.insert(0,'work');import extract_sprite
 native,_=extract_sprite.unpack(0x1863ac);ss=snap();v=ss[0x12425:0x12425+0x5c00];actual=b''.join(v[i:i+2][::-1] for i in range(0,len(v),2));assert actual==bytes(native[:0x5c00])
 checks.append(dict(name='original_namek_graphics_preserved',passed=True,stage=6,variant=0,vramSha256=hashlib.sha256(actual).hexdigest()));print('ORIGINAL NAMEK PASS',flush=True)
 restore((O/'mode2-playing.state').read_bytes());ko=None;transitions=[];last=None
 for f in range(30000):
  tick();now=(rw(0xe6a4),rw(0xe750),rb(0xe741),rb(0xf7c0))
  if now!=last:transitions.append(dict(f=f,state=list(now)));last=now
  if min(rw(P1+0x24),rw(P2+0x24))==0 and ko is None:ko=f
  if ko is not None and f-ko>1500:break
 save_image(O/'cpu-post-match.png');(O/'cpu-post-match.state').write_bytes(snap());post=cur();checks.append(dict(name='native_cpu_match_until_post_ko',passed=ko is not None,koFrame=ko,end=post,transitions=transitions[-40:],fixtureWrites=[]));print('CPU POST',ko,post,flush=True)
 before=snap();press(['C']);after=cur();save_image(O/'cpu-after-confirm.png');checks.append(dict(name='cpu_postmatch_confirm',state=after,variantRetained=after['stage']==6 and after['variant']==3));print('CPU CONFIRM',after,flush=True)
 for f in range(2400):
  if rw(0xe6a4)==0x20 and rw(0xe750)==3:break
  tick(['C'] if f%120<3 else [])
 rematch=cur();assert rematch['stage']==6 and rematch['variant']==3 and rematch['state']==0x20,rematch
 checks.append(dict(name='cpu_rematch_retains_selected_variant',passed=True,result=rematch,fixtureWrites=[]));save_image(O/'cpu-rematch-parameters.png');print('REMATCH PASS',rematch,flush=True)
 # Deliberately inject only a stale latch into a fresh story character screen.
 core.retro_reset()
 for entry in steps[:5]:
  for _ in range(entry.get('frames',1)):tick(entry.get('buttons',[]))
 press(['C'],idle=180);assert rw(0xe6a4)==0x24,cur();wb(0xf7c0,3)
 for f in range(1800):
  tick(['C'] if f%120<3 else [])
  if rb(0xf7c0)==0 and rb(0xe741)!=0:break
 after=cur();assert after['variant']==0,after
 save_image(O/'story-after-stale-latch.png');checks.append(dict(name='story_clears_stale_variant',passed=True,fixtureWrites=[dict(address='F7C0',value=3,when='fresh story character screen before confirming')],result=after));print('STORY PASS',after,flush=True)
 (O/'regression.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),checks=checks),indent=2))
finally:core.retro_unload_game();core.retro_deinit()
