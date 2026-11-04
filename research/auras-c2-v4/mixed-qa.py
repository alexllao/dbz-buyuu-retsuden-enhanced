from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path('work').resolve()))
import extract_sprite as native
cfg=sys.argv[1:];p1cid=int(cfg[0]) if cfg else 0;p2cid=int(cfg[1]) if len(cfg)>1 else 2
qa_rom=Path('work/auras/colors-v4/candidate.bin');rom_bytes=qa_rom.read_bytes()
out=Path('work/auras/colors-v4/runtime-qa-extra')/f'pair-{p1cid:02}-{p2cid:02}';out.mkdir(parents=True,exist_ok=True)
sys.argv=['probe','--native','--rom',str(qa_rom),'--out',str(out)]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'v4-extra-runtime-setup','exec'),globals())

def unpack_at(a):
 head=int.from_bytes(rom_bytes[a:a+2],'little');a+=2;assert head<0x8000
 size=head+1;data=bytearray()
 while len(data)<size:
  flags=rom_bytes[a];a+=1
  for bit in range(8):
   if flags>>bit&1:data.append(rom_bytes[a]);a+=1
   else:
    token=int.from_bytes(rom_bytes[a:a+2],'little');a+=2;n=(token&15)+3;dist=token>>4
    for _ in range(n):data.append(data[len(data)-dist] if len(data)-dist>=0 else 0)
   if len(data)>=size:break
 return bytes(data[:size])

def ptr(a):return int.from_bytes(rom_bytes[a:a+4],'big')

qa_p2index=11 if p1cid==p2cid==9 else p2cid
expected=[(0xa260,unpack_at(ptr(0x280000+p1cid*8))),(0xa820,unpack_at(ptr(0x280004+p1cid*8))),(0xa960,unpack_at(ptr(0x280100+qa_p2index*12))),(0x5c00,unpack_at(ptr(0x280104+qa_p2index*12))),(0xae80,unpack_at(ptr(0x280108+qa_p2index*12))),(0xaec0,unpack_at(0x280300))]
expected_fx=native.unpack(0x1b942)[0]
expected_a260_fx=native.unpack(0x2a3a0)[0]
baseline_old=Path('work/auras/v3/vram-probe/baseline.state').read_bytes()
old_common=baseline_old[0x22425+54*2:0x22425+64*2]

def ast(b):return {'cid':rb(b+0x58),'program':rw(b),'action':rb(b+0x5b),'pose':rb(b+4),'hp':rw(b+0x24),'aura':rb(b+0xbd),'phase':rb(b+0x111),'worldY':rw(b+0x10)}
def rec(frame):
 s=snap();v=s[0x12425:0x22425];regs=s[0x22525:0x22545]
 def block(a,n):return b''.join(v[i:i+2][::-1] for i in range(a,a+n,2))
 matches={hex(a):block(a,len(data))==data for a,data in expected}
 n=min(80,rb(0xe452));sprites=[];aa=[]
 for i in range(n):
  q=0xe04e+8*i;size=rb(q+2);attr=rw(q+4);ti=attr&2047
  sprites.append(((rw(q)&511)-128,((size&3)+1)*8,(((size>>2)&3)+1)*8))
  if 0x513<=ti<=0x55f and ti!=0x540 or 0x2e0<=ti<=0x2ff or 0x574<=ti<=0x578:aa.append((ti,(attr>>13)&3))
 line=max(sum(y<=z<y+h for y,h,w in sprites) for z in range(224));pixels=max(sum(w for y,h,w in sprites if y<=z<y+h) for z in range(224))
 return {'frame':frame,'counter':rw(0xe6a8),'E9C4':rw(0xe9c4),'E73C':rb(0xe73c),'E9CE':rb(0xe9ce),'dirty':rb(0xe874),'p1':ast(P1),'p2':ast(P2),'VRAM_matches':matches,'native_5c_fx_exact':block(0x5c00,1024)==expected_fx,'native_A260_fx_exact':block(0xa260,1440)==expected_a260_fx,'tile540_tail_intact':v[0xa804:0xa820]==baseline_old[0x12425+0xa804:0x12425+0xa820],'commonCRAM_unchanged':s[0x22425+54*2:0x22425+64*2]==old_common,'VDP_R11_R13':[regs[11],regs[13]],'sprites':n,'max_scanline_sprites':line,'max_scanline_pixels':pixels,'aura_tiles_and_banks':aa,'dust_sprites':sum(0x576<=ti<=0x578 for ti,bank in aa),'aura_sprites':len(aa)}

try:
 for index,step in enumerate(steps[:-1]):
  if index==9 and p1cid:
   for direction,count in [('DOWN',p1cid//3),('RIGHT',p1cid%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  if index==11 and p2cid!=1:
   for direction,count in [('DOWN',p2cid//3),('RIGHT',p2cid%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
   for _ in range(step.get('frames',1)):tick()
   continue
  for _ in range(step.get('frames',1)):tick(step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 assert (rb(P1+0x58),rb(P2+0x58))==(p1cid,p2cid),(rb(P1+0x58),rb(P2+0x58))
 baseline=snap();cases={}
 def run(label,schedule):
  restore(baseline);rows=[]
  for i,(k1,k2) in enumerate(schedule):tick(k1,k2);rows.append(rec(i))
  cases[label]=rows
 run('P2-charge-release',[([],['A','B'] if 10<=i<100 else []) for i in range(180)])
 run('both-different-colors',[(['A','B'] if 10<=i<100 else [],['A','B'] if 10<=i<110 else []) for i in range(190)])
 run('two-consecutive',[(['A','B'] if 10<=i<80 or 140<=i<210 else [],[]) for i in range(290)])
 restore(baseline)
 for _ in range(65):tick(['A','B'])
 ww(P1+0x10,0xa0);wb(P1+0x1e,rb(P1+0x1e)|16)
 rows=[]
 for i in range(55):tick(['A','B']);rows.append(rec(i))
 cases['forced-air-map-selection']=rows
 restore(baseline);ww(P1,0x15c);ww(P1+6,1);wb(P1+0x5b,0xd)
 ww(0xe9c4,3);wb(0xe9ce,0);wb(0xe73c,0x41);wb(0xe737,0x40);ww(0xe732,0)
 rows=[rec(-1)]
 for i in range(60):tick();rows.append(rec(i))
 cases['synthetic-native-A260-FX']=rows
 restore(baseline);ww(P1,0x15c);ww(P1+6,1);wb(P1+0x5b,0xd)
 ww(0xe9c4,3);wb(0xe9ce,0x43);wb(0xe73c,0x41);wb(0xe737,0x40);ww(0xe732,0)
 rows=[rec(-1)]
 for i in range(180):tick();rows.append(rec(i))
 cases['synthetic-native-FX43']=rows
 # No natural ending is assumed. Explicitly test safe-state restoration separately.
 ww(0xe9c4,0);wb(0xe73c,0);wb(0xe737,0);wb(0xe9ce,0)
 for b in [P1,P2]:ww(b,0);ww(b+6,0);wb(b+0x5b,0);wb(b+0xbd,0)
 rows=[rec(-1)]
 for i in range(30):tick();rows.append(rec(i))
 cases['forced-normal-transition-test']=rows
 report={'rom':str(qa_rom),'sha256':hashlib.sha256(rom_bytes).hexdigest(),'pair':[p1cid,p2cid],'expected_segments':[{'VRAM':hex(a),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()} for a,data in expected],'cases':cases,'scope':'Human-control native boot. SyntheticFX43 changes actorprogram and cinematicRAM state, notCPU-PC. Forcednormaltransition clears scene flags and actorprograms explicitly and is not a claim of a natural completed special. Air case forces altitude/plane only.'}
 (out/'report.json').write_text(json.dumps(report,indent=2))
 print('REPORT',str(out/'report.json'),report['sha256'],flush=True)
 for k,rs in cases.items():print(k,'dirty',sorted(set(x['dirty'] for x in rs)),'maxsprites',max(x['sprites'] for x in rs),'modes',sorted(set((x['E9C4'],x['E73C']) for x in rs)),'allAtlasSamples',sum(all(x['VRAM_matches'].values()) for x in rs),'of',len(rs),flush=True)
finally:
 core.retro_unload_game();core.retro_deinit()
