import ctypes as C,sys,json,struct,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stage_preview import png_rgba
ROOT=Path(__file__).resolve().parent
class Variable(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
class System(C.Structure):_fields_=[('name',C.c_char_p),('version',C.c_char_p),('extensions',C.c_char_p),('need_fullpath',C.c_bool),('block_extract',C.c_bool)]
class Geometry(C.Structure):_fields_=[('base_width',C.c_uint),('base_height',C.c_uint),('max_width',C.c_uint),('max_height',C.c_uint),('aspect_ratio',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('sample_rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
POLL=C.CFUNCTYPE(None)
INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
core=C.CDLL(str(ROOT/'genesis_plus_gx_libretro.dll'))
options={};pixel_format=0;latest=None;buttons=0;unknown=set()
directory=str(ROOT).encode();rom_path=Path(sys.argv[1]).resolve();steps=json.loads(Path(sys.argv[2]).read_text())
@ENV
def env(cmd,data):
 global pixel_format
 cmd=cmd&0xffff
 if cmd in (9,30,31):C.cast(data,C.POINTER(C.c_char_p))[0]=directory;return True
 if cmd==10:pixel_format=C.cast(data,C.POINTER(C.c_int))[0];return pixel_format in (0,1,2)
 if cmd==16:
  arr=C.cast(data,C.POINTER(Variable));i=0
  while arr[i].key:
   text=arr[i].value or b''
   options[arr[i].key]=text.split(b';',1)[-1].strip().split(b'|')[0];i+=1
  return True
 if cmd==15:
  var=C.cast(data,C.POINTER(Variable));key=var[0].key
  if key in options:var[0].value=options[key];return True
  return False
 if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
 if cmd==51:return True
 if cmd in (39,52,59):C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
 if cmd==47:C.cast(data,C.POINTER(C.c_int))[0]=1;return True
 if cmd==50:C.cast(data,C.POINTER(C.c_float))[0]=60.;return True
 if cmd in (1,6,8,11,18,35,36,37,44,60):return True
 unknown.add(cmd);return False
@VIDEO
def video(data,w,h,pitch):
 global latest
 if data and data!=C.c_void_p(-1).value:latest=(w,h,pitch,C.string_at(data,pitch*h))
@AUDIO
def audio(l,r):pass
@BATCH
def batch(data,frames):return frames
@POLL
def poll():pass
@INPUT
def input_state(port,device,index,ident):
 if port!=0 or (device&0xff)!=1:return 0
 if ident==256:return buttons
 return int(bool(buttons&(1<<ident)))
for name,arg in [('retro_set_environment',env),('retro_set_video_refresh',video),('retro_set_audio_sample',audio),('retro_set_audio_sample_batch',batch),('retro_set_input_poll',poll),('retro_set_input_state',input_state)]:
 getattr(core,name).argtypes=[type(arg)];getattr(core,name)(arg)
core.retro_get_system_info.argtypes=[C.POINTER(System)];info=System();core.retro_get_system_info(C.byref(info))
core.retro_init()
rom=rom_path.read_bytes();buffer=C.create_string_buffer(rom)
game=Game(str(rom_path).encode(),C.cast(buffer,C.c_void_p),len(rom),None)
core.retro_load_game.argtypes=[C.POINTER(Game)];core.retro_load_game.restype=C.c_bool
assert core.retro_load_game(C.byref(game)),'Core rejected ROM'
core.retro_set_controller_port_device.argtypes=[C.c_uint,C.c_uint]
core.retro_set_controller_port_device(0,1);core.retro_set_controller_port_device(1,1)
core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
core.retro_get_memory_size.argtypes=[C.c_uint];core.retro_get_memory_size.restype=C.c_size_t
ram_ptr=core.retro_get_memory_data(2);ram_size=core.retro_get_memory_size(2)
ram=(C.c_uint8*ram_size).from_address(ram_ptr)
core.retro_get_system_av_info.argtypes=[C.POINTER(AV)];av=AV();core.retro_get_system_av_info(C.byref(av))
print(info.name,info.version,'RAM',ram_size,'FPS',av.timing.fps,'pixel_format',pixel_format,flush=True)
key={'B':0,'A':1,'START':3,'UP':4,'DOWN':5,'LEFT':6,'RIGHT':7,'C':8,'Y':9,'X':10,'Z':11}
log=[];total=0
def save_image(path):
 assert latest,'No video frame'
 w,h,pitch,data=latest;pix=[]
 for y in range(h):
  if pixel_format==1:
   for x in range(w):
    v=struct.unpack_from('<I',data,y*pitch+x*4)[0];pix.append(((v>>16)&255,(v>>8)&255,v&255,255))
  else:
   for x in range(w):
    v=struct.unpack_from('<H',data,y*pitch+x*2)[0]
    if pixel_format==2:pix.append((((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31,255))
    else:pix.append((((v>>10)&31)*255//31,((v>>5)&31)*255//31,(v&31)*255//31,255))
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);png_rgba(p,w,h,pix,scale=2)
 return {'width':w,'height':h,'png':str(p),'framebuffer_sha256':hashlib.sha256(data).hexdigest()}
try:
 for step in steps:
  for address,value in step.get('write_ram',{}).items():
   off=int(address,0)&0xffff
   if step.get('byte_swap',True):off^=1
   ram[off]=value
  buttons=sum(1<<key[s] for s in step.get('buttons',[]))
  for _ in range(step.get('frames',1)):
   for address,value in step.get('freeze_ram',{}).items():
    off=(int(address,0)&0xffff)^1
    ram[off]=value
   core.retro_run();total+=1
  entry={'frames_total':total,'buttons':step.get('buttons',[]),'ram_state_raw':bytes(ram[0xe6a4:0xe6a8]).hex(),'p1_raw':bytes(ram[0xe7b6:0xe7b8]).hex(),'stage_raw':bytes(ram[0xe740:0xe742]).hex(),'player1':ram[0xe7b6^1],'player2':ram[0xe8de^1],'stage':ram[0xe741^1]}
  if 'save' in step:entry.update(save_image(step['save']))
  if 'dump_ram' in step:Path(step['dump_ram']).write_bytes(bytes(ram))
  log.append(entry);print(json.dumps(entry),flush=True)
finally:
 core.retro_unload_game();core.retro_deinit()
report={'core':info.name.decode(),'core_version':info.version.decode(),'core_sha256':hashlib.sha256((ROOT/'genesis_plus_gx_libretro.dll').read_bytes()).hexdigest(),'rom_sha256':hashlib.sha256(rom).hexdigest(),'fps':av.timing.fps,'pixel_format':pixel_format,'unknown_optional_environment_commands':sorted(unknown),'steps':log}
(ROOT/'last-run.json').write_text(json.dumps(report,indent=2))
