from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);tag=sys.argv[3];port=1;turbo=False;out=ROOT/'work/native-stun-fix/guard'/tag;out.mkdir(parents=True,exist_ok=True)
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
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 hits=[];trace=[];hp=rw(P2+0x24)
 for f in range(240):
  keys=['A'] if f<6 else []
  if hits and hits[0]+9<=f<hits[0]+13:keys=['B']
  if len(hits)>1 and hits[1]+9<=f<hits[1]+13:keys=['A']
  tick(keys,['RIGHT'] if hits else []);newHP=rw(P2+0x24)
  if newHP<hp:hits.append(f)
  hp=newHP;trace.append({'f':f,'keys':keys,'enemyBack':bool(hits),'enemyHP':hp,'enemyAction':rb(P2+0x5b),'program':rw(P1),'enemyProgram':rw(P2),'enemyCursor':rw(P2+6),'enemyStun':rb(P2+0x51),'enemyDizzyTimer':rw(P2+0x36)})
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'tag':tag,'hits':hits,'trace':trace},indent=2),encoding='utf8');print(tag,hits)

finally:core.retro_unload_game();core.retro_deinit()
