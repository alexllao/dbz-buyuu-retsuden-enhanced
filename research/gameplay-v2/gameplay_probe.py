from pathlib import Path
import ctypes as C,json,sys,struct,hashlib,subprocess

BASE=Path(__file__).resolve().parent.parent
cli=list(sys.argv)
selected_rom=Path(cli[cli.index('--rom')+1]) if '--rom' in cli else BASE/'work/rom/original.bin'
selected_out=Path(cli[cli.index('--out')+1]) if '--out' in cli else None
selected_character=int(cli[cli.index('--character')+1]) if '--character' in cli else 0
boot_turbo='--turbo' in sys.argv
native_boot='--native' in sys.argv or boot_turbo
WORK=BASE/'work/gameplay'/('turbo-boot' if boot_turbo else 'normal-boot' if native_boot else 'speed-fixture');WORK.mkdir(parents=True,exist_ok=True)
if selected_out is not None:WORK=selected_out;WORK.mkdir(parents=True,exist_ok=True)
# Reuse the existing local emulator setup; no additional analysis service or network.
sys.argv=['probe',str(selected_rom),str(BASE/'work/auras/controlled.json')]
src=(BASE/'work/emulator/check_rom.py').read_text(encoding='utf-8').split('try:\n for step in steps:')[0]
src=src.replace('ROOT=Path(__file__).resolve().parent',"ROOT=Path(r'"+str(BASE/'work/emulator')+"')")
src=src.replace('latest=None;buttons=0;', 'latest=None;buttons=0;buttons2=0;')
src=src.replace('if port!=0 or (device&0xff)!=1:return 0','if port>1 or (device&0xff)!=1:return 0\n pad_buttons=buttons if port==0 else buttons2')
src=src.replace('if ident==256:return buttons','if ident==256:return pad_buttons').replace('bool(buttons&(1<<ident))','bool(pad_buttons&(1<<ident))')
exec(compile(src,'local-emulator-setup','exec'),globals())

P1=0xe75e;P2=0xe886
def rb(a):return ram[(a&0xffff)^1]
def wb(a,v):ram[(a&0xffff)^1]=v&255
def rw(a):return rb(a)*256+rb(a+1)
def ww(a,v):wb(a,v>>8);wb(a+1,v)
def tick(keys=(),keys2=()):
 global buttons,buttons2,total
 buttons=sum(1<<key[k] for k in keys)
 buttons2=sum(1<<key[k] for k in keys2)
 core.retro_run();total+=1
def state():
 w,h,pitch,data=latest
 roi=b''.join(data[y*pitch:y*pitch+140*2] for y in range(70,min(h,224)))
 return {'x':rw(P1+0xa),'y':rw(P1+0x10),'action':rb(P1+0x5b),'held':rb(P1+0x1b),'pressed':rb(P1+0x1d),'pad':rb(0xe666),'speed':rw(0xe756),'anim3a':rw(P1+0x3a),'field36':rw(P1+0x36),'field38':rw(P1+0x38),'p1_screen_roi_sha256':hashlib.sha256(roi).hexdigest(),'native_player_hex':bytes(rb(P1+i) for i in range(0x128)).hex()}
core.retro_serialize_size.restype=C.c_size_t
core.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_serialize.restype=C.c_bool
core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool
def snap():
 buf=C.create_string_buffer(core.retro_serialize_size());assert core.retro_serialize(buf,len(buf));return buf.raw
def restore(data):
 buf=C.create_string_buffer(data);assert core.retro_unserialize(buf,len(data))
def trial(baseline,label,schedule,speed=None):
 restore(baseline)
 if speed is not None:
  ww(0xe756,speed)
  ww(0xe758,0x10000//speed)
 initial=state();trace=[]
 for keys in schedule:
  tick(keys);trace.append(state())
 save_image(WORK/(label+'.png'))
 return {'label':label,'initial':initial,'frames':trace}
try:
 for index,step in enumerate(steps[:-1]):
  if index==9 and selected_character:
   for direction,count in [('DOWN',selected_character//3),('RIGHT',selected_character%3)]:
    for press in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=step.get('buttons',[])
  if boot_turbo and index<2:keys=list(set(keys+['A','B']))
  for _ in range(step.get('frames',1)):tick(keys)
 # Controlled test fixture: human input for both fighters, port two stays unpressed.
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 save_image(WORK/'baseline.png')
 baseline=snap();(WORK/'baseline.state').write_bytes(baseline)
 assert rb(P1+0x58)==selected_character,(selected_character,rb(P1+0x58))
 print('BASE',json.dumps(state()),flush=True)
 schedules={
 'idle':[[]]*90,
 'right-30-release':[ ['RIGHT'] for _ in range(30)]+[[]]*60,
 'left-30-release':[ ['LEFT'] for _ in range(30)]+[[]]*60,
 'punch-tap':[['A']]*2+[[]]*88,
 'kick-tap':[['B']]*2+[[]]*88,
 'jump-tap':[['UP']]*2+[[]]*88,
 'charge-release':[['A','B']]*30+[[]]*60,
 'punch-then-right':[['A']]*2+[['RIGHT']]*88,
 'right-then-left':[['RIGHT']]*20+[['LEFT']]*40+[[]]*30,
 'punch-double-early':[['A']]*2+[[]]*2+[['A']]*2+[[]]*84,
 }
 for n in (1,5,10,15,20,25,35,40):schedules[f'right-{n:02}-stop']=[['RIGHT']]*n+[[]]*(90-n)
 for gap in (8,12,16,18,19,20,21,22):schedules[f'punch-repress-{gap:02}']=[['A']]*2+[[]]*(gap-2)+[['A']]*2+[[]]*(88-gap)
 schedules['punch-brief-direction']=[['A']]*2+[[]]*2+[['RIGHT']]*4+[[]]*82
 for phase in (0,1):schedules[f'one-frame-punch-phase-{phase}']=[[]]*phase+[['A']]+[[]]*(89-phase)
 schedules['punch-held']=[['A']]*90
 if '--quick' in cli:
  wanted=['idle','right-01-stop','right-05-stop','right-then-left','punch-tap','kick-tap','jump-tap','charge-release','punch-held']
  schedules={k:schedules[k] for k in wanted}
 results=[]
 for speed in ((None,) if native_boot else (0x100,0x140)):
  for label,schedule in schedules.items():
   results.append(trial(baseline,f'{"native" if speed is None else format(speed,"03x")}-{label}',schedule,speed))
 if '--quick' in cli:
  for attack,button in [('punch','A'),('kick','B')]:
   found=next(r for r in results if r['label']==f'native-{attack}-tap')
   end=next(i+1 for i,s in enumerate(found['frames']) if i>0 and s['action']==0 and found['frames'][i-1]['action']!=0)
   gap=max(3,end-4)
   results.append(trial(baseline,f'native-{attack}-late-dynamic',[[button]]*2+[[]]*(gap-2)+[[button]]*3+[[]]*(87-gap)))
 report={'rom_sha256':hashlib.sha256(rom).hexdigest(),'core':info.name.decode(),'core_version':info.version.decode(),'fps':av.timing.fps,'fixture':'Original ROM; both control-type bytes forced to human (P1+BE and P2+BE = 0); second port unpressed; save-state restored before each trial. Native speed pairs E756/E758 = 0x100/0x100 and 0x140/0xCC, matching inverse calculation at ROM 0x207E6. Boot turbo verification separate.','initial_speed':rw(0xfe0c),'results':results}
 report['native_boot']=native_boot;report['turbo_boot']=boot_turbo;report['native_speed_pair']=[rw(0xe756),rw(0xe758)]
 if native_boot:report['fixture']='Original ROM, native boot speed retained. Turbo enabled by A+B held during boot and first Start. Controlled test fixture changes only human/CPU control bytes to keep opponent idle; snapshots restored for each trial.'
 (WORK/'traces.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 for r in results:
  firstx=next((i+1 for i,s in enumerate(r['frames']) if s['x']!=r['initial']['x']),None)
  changes=[(i+1,s['action']) for i,s in enumerate(r['frames']) if s['action']!=(r['initial']['action'] if i==0 else r['frames'][i-1]['action'])]
  print(r['label'],'firstx',firstx,'dx30',r['frames'][29]['x']-r['initial']['x'],'actions',changes[:15],flush=True)
 if native_boot and '--quick' not in cli and '--no-video' not in cli:
  clips=[('right-30-release',schedules['right-30-release']),('right-then-left',schedules['right-then-left']),('punch-then-right',schedules['punch-then-right']),('punch-double-early',schedules['punch-double-early']),('jump-tap',schedules['jump-tap']),('charge-release',schedules['charge-release'])]
  encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf','scale=640:448:flags=neighbor','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(WORK/'gameplay.mp4')],stdin=subprocess.PIPE)
  for label,schedule in clips:
   restore(baseline)
   for keys in schedule+[[]]*30:
    tick(keys);w,h,pitch,data=latest
    encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  encoder.stdin.close();assert encoder.wait()==0
  (WORK/'video-sequence.json').write_text(json.dumps({'fps':av.timing.fps,'frames_per_scene':120,'scenes':[x[0] for x in clips]},indent=2),encoding='utf-8')
finally:
 core.retro_unload_game();core.retro_deinit()
