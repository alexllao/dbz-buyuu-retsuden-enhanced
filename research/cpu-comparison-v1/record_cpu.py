from pathlib import Path
import sys,json,hashlib,subprocess,time,collections
cfg=sys.argv[1:];rom_arg=cfg[0];p1id=int(cfg[1]);p2id=int(cfg[2]);out=Path(cfg[3]);seconds=float(cfg[4]) if len(cfg)>4 else 35
assert 0<seconds<=35
out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(Path('work').resolve()));sys.path.insert(0,str(Path('work/cpu-soak').resolve()))
from menu_ai_setup import boot_versus
sys.argv=['probe','--native','--rom',rom_arg,'--out',str(out)]
header=Path('work/gameplay_probe.py').read_text(encoding='utf-8').split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'cpu-native-setup','exec'),globals())
original_hash='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557'
new_hash='100b546f0555b014ac8cd01ddd7d12af97b8acf8011a006e2933afcc3a42983b'
romhash=hashlib.sha256(rom).hexdigest();assert romhash in [original_hash,new_hash]
is_mod=romhash==new_hash
resources=json.loads(Path('work/auras/colors-v4/resources.json').read_text(encoding='utf-8')) if is_mod else None
cache={}
def unpack_at(a):
 if a in cache:return cache[a]
 size=int.from_bytes(rom[a:a+2],'little')+1;a+=2;data=bytearray()
 while len(data)<size:
  flags=rom[a];a+=1
  for bit in range(8):
   if flags>>bit&1:data.append(rom[a]);a+=1
   else:
    token=int.from_bytes(rom[a:a+2],'little');a+=2;n=(token&15)+3;dist=token>>4
    for _ in range(n):data.append(data[len(data)-dist] if len(data)-dist>=0 else 0)
   if len(data)>=size:break
 return bytes(data[:size])
def expected_regions(cid1,cid2):
 key=(cid1,cid2)
 if key not in cache:
  if max(key)>10:return []
  j=11 if cid1==cid2==9 else cid2
  def ptr(a):return int.from_bytes(rom[a:a+4],'big')
  cache[key]=[(0xa260,unpack_at(ptr(0x280000+cid1*8))),(0xa820,unpack_at(ptr(0x280004+cid1*8))),(0xa960,unpack_at(ptr(0x280100+j*12))),(0x5c00,unpack_at(ptr(0x280104+j*12))),(0xae80,unpack_at(ptr(0x280108+j*12))),(0xaec0,unpack_at(0x280300))]
 return cache[key]
def actor(b):
 return dict(cid=rb(b+0x58),hp=rw(b+0x24),power=rw(b+0x28),x=rw(b+0xa),y=rw(b+0x10),action=rb(b+0x5b),program=rw(b),pose=rb(b+4),control=rb(b+0xbe),held=rw(b+0x1a),pressed=rw(b+0x1c),ai=[rb(b+i) for i in [0xbf,0xc0,0xc1,0xc2,0xc3,0xc4]],ai_cursor=rw(b+0x44),aura=rb(b+0xbd),phase=rb(b+0x111) if is_mod else None)
def frame_state(f):
 return dict(frame=f,tick=rw(0xe6a8),state=rw(0xe6a4),scene=rb(0xe73c),effect=rw(0xe9c4),effect_kind=rb(0xe9ce),dirty=rb(0xe874) if is_mod else None,stage=rb(0xe741),gates=[rb(0xe742),rb(0xe744)],p1=actor(P1),p2=actor(P2))
def detail(row):
 state=snap();v=state[0x12425:0x22425]
 def block(a,n):return b''.join(v[i:i+2][::-1] for i in range(a,a+n,2))
 n=rb(0xe452);sprites=[];auraSprites=0
 for i in range(min(n,80)):
  a=0xe04e+i*8;size=rb(a+2);tile=rw(a+4)&2047
  sprites.append(((rw(a)&511)-128,((size&3)+1)*8,(((size>>2)&3)+1)*8))
  if is_mod and tile in resources['physical_tiles']:auraSprites+=1
  if not is_mod and 0x513<=tile<0x540:auraSprites+=1
 lines=[sum(y<=z<y+h for y,h,w in sprites) for z in range(224)]
 pixels=[sum(w for y,h,w in sprites if y<=z<y+h) for z in range(224)]
 row.update(sprites=n,scanline_sprites=max(lines,default=0),scanline_pixels=max(pixels,default=0),aura_sprites=auraSprites,framebuffer_sha256=hashlib.sha256(latest[3]).hexdigest())
 if is_mod:
  matches={hex(a):block(a,len(data))==data for a,data in expected_regions(row['p1']['cid'],row['p2']['cid'])}
  # A temporary effect may legitimately own these tiles; judge only Ki draws
  # in a normal scene with resident resources and a sustained/retiring aura.
  judge=bool(row['dirty']==0 and row['scene']==0 and row['effect']==0 and auraSprites and (row['p1']['phase'] or row['p2']['phase']))
  row.update(atlas_matches=matches,atlas_judged=judge,atlas_fault=bool(judge and not all(matches.values())))
 return row
encoder=None
try:
 boot=boot_versus(globals(),p1id,p2id)
 initial=frame_state(-1);save_image(out/'Inicio.png')
 (out/'baseline.state').write_bytes(snap())
 w,h,pitch,data=latest
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size',f'{w}x{h}','-framerate',str(av.timing.fps),'-i','pipe:0','-vf','scale=640:448:flags=neighbor','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'CPU.mp4')],stdin=subprocess.PIPE)
 rows=[];events=[];maxFrames=int(seconds*av.timing.fps);ko=None;freezeStart=None;freezeMax=0;frozen=0;lastHash=None;lastTick=None;failure=None;start=time.monotonic();photos=0
 prev=initial
 for i in range(maxFrames):
  tick() # Empty host pads. Only native CPU scripts choose combat inputs.
  row=frame_state(i);w,h,pitch,data=latest
  encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  fbhash=hashlib.sha256(data).hexdigest()
  stable=fbhash==lastHash and row['tick']==lastTick and row['state']==0xc and row['scene']==row['effect']==0 and all(row[p]['hp']>0 for p in ['p1','p2'])
  frozen=frozen+1 if stable else 0;freezeMax=max(freezeMax,frozen);lastHash=fbhash;lastTick=row['tick']
  reasons=[]
  for p in ['p1','p2']:
   if row[p]['hp']<prev[p]['hp']:reasons.append(p+'-damage')
   if row[p]['cid']!=prev[p]['cid']:reasons.append(p+'-character-change')
  if (row['scene'],row['effect'],row['effect_kind'],row['dirty'])!=(prev['scene'],prev['effect'],prev['effect_kind'],prev['dirty']):reasons.append('effect-scene-transition')
  if i%6==0 or reasons:
   detail(row);rows.append(row)
   if row.get('atlas_fault') and photos<6:
    save_image(out/f'Atlas-aviso-{i:05}.png');photos+=1
  if reasons:events.append(dict(frame=i,reasons=reasons,p1hp=row['p1']['hp'],p2hp=row['p2']['hp'],scene=row['scene'],effect=row['effect'],effect_kind=row['effect_kind'],dirty=row['dirty']))
  if i in [int(av.timing.fps*t) for t in [7,14,21,28]]:save_image(out/f'CPU-{i:05}.png')
  if ko is None and any(row[p]['hp']==0 for p in ['p1','p2']):ko=i
  prev=row
  if frozen>=round(av.timing.fps*5):failure='Suspected freeze: identical framebuffer and game counter for five seconds outside effects';break
  if ko is not None and i-ko>=round(av.timing.fps*2):break
 encoder.stdin.close();assert encoder.wait()==0;encoder=None
 save_image(out/'Final.png');(out/'final.state').write_bytes(snap())
 report=dict(source_rom_sha256=romhash,variant='enhanced-v4' if is_mod else 'untouched-original',pair=[p1id,p2id],fps=av.timing.fps,frames=i+1,gameplay_seconds=(i+1)/av.timing.fps,requested_cap_seconds=seconds,wall_seconds=time.monotonic()-start,core='Genesis Plus GX v1.7.4 f27655b',boot=boot,initial=initial,final=frame_state(i),native_ko_frame=ko,freeze_suspect=failure,max_identical_counter_and_framebuffer_frames=freezeMax,host_combat_buttons=[],fixture_writes='P1/P2 actor+BE only, as documented by menu helper; no HP, RNG, position, actor-ID, animation or cinematic state forcing.',samples=rows,events=events,video_sha256=hashlib.sha256((out/'CPU.mp4').read_bytes()).hexdigest())
 (out/'Informe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(variant=report['variant'],pair=report['pair'],seconds=report['gameplay_seconds'],HP=[report['final'][p]['hp'] for p in ['p1','p2']],events=len(events),aura_samples=sum(r['aura_sprites']>0 for r in rows),atlas_faults=sum(r.get('atlas_fault',False) for r in rows),failure=failure)),flush=True)
finally:
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()
