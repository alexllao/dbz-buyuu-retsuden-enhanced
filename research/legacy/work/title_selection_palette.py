from pathlib import Path
import json,struct,hashlib,subprocess,sys
from color_plan import CHAR_NAMES
OUT=Path('outputs/presentacion-seleccion-v1');OUT.mkdir(exist_ok=True)
source=Path('outputs/dbz-colores-v1/Buyuu_Retsuden_Colores_v1.bin').read_bytes();result=bytearray(source)
index=json.loads(Path('work/selection-review/palette-index.json').read_text())
edits={
 0:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,5:0x04AC,6:0x028A,8:0x006C,12:0x0640},
 1:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,5:0x04AC,6:0x028A,11:0x0826,12:0x0602},
 2:{1:0x0240,2:0x0262,3:0x0484,4:0x06C6,5:0x0602,6:0x0826},
 3:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,11:0x0420,12:0x0640},
 4:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,5:0x0CAC,6:0x0A68,8:0x0642,9:0x0864,10:0x0420},
 5:{3:0x0888,4:0x04AC,5:0x086A,6:0x0486,7:0x0262,8:0x0240,9:0x0846,11:0x04AC,12:0x0046},
 6:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,5:0x0AEE,6:0x04AC,7:0x0CEE,8:0x0CA8,9:0x0068,10:0x0CA8,11:0x0A64,12:0x0642,13:0x0862},
 7:{1:0x0ACE,2:0x08AC,3:0x046A,4:0x0246,5:0x0224,6:0x0862,7:0x0420,8:0x006C,9:0x0246},
 8:{6:0x0CAC,7:0x0C8A,8:0x0826,9:0x0602},
 9:{1:0x0ACE,2:0x08AC,3:0x046C,4:0x0248,5:0x0246,6:0x0224,8:0x026A,9:0x0048},
 10:{2:0x0CAC,3:0x0A68,4:0x0624,5:0x0246,6:0x0224,7:0x0482,8:0x0260}
}
allowed=set();records=[]
def put(offset,new,kind,cid=None):
 before=list(struct.unpack_from('>16H',source,offset))
 assert all(v&~0xEEE==0 for v in new)
 assert before[0]==new[0]
 struct.pack_into('>16H',result,offset,*new);allowed.update(range(offset,offset+32))
 records.append({'kind':kind,'character_id':cid,'offset':hex(offset),'before':[f'{v:04X}' for v in before],'after':[f'{v:04X}' for v in new]})
for entry in index:
 cid=entry['character_id'];assert len(entry['palette_offsets'])==1
 offset=entry['palette_offsets'][0]
 before=list(struct.unpack_from('>16H',source,offset));after=before.copy()
 for i,v in edits[cid].items():after[i]=v
 put(offset,after,'selection',cid)
 alt_offset=offset+11*32
 oldalt=list(struct.unpack_from('>16H',source,alt_offset))
 newalt=[after[i] if oldalt[i]==before[i] else oldalt[i] for i in range(16)]
 put(alt_offset,newalt,'selection_alternative',cid)
title_offset=0x1ADE32;title=list(struct.unpack_from('>16H',source,title_offset))
for i,v in {2:0x0642,3:0x046A,4:0x04AE,5:0x046A,6:0x0420,7:0x04A4,8:0x028A,9:0x0ACE,10:0x08AC,11:0x0862,12:0x04AC,13:0x0262}.items():title[i]=v
put(title_offset,title,'presentation')
checksum=sum(struct.unpack('>1048320H',result[512:]))&0xFFFF;struct.pack_into('>H',result,0x18E,checksum);allowed.update([0x18E,0x18F])
changed=[i for i,(a,c) in enumerate(zip(source,result)) if a!=c]
assert all(i in allowed for i in changed)
target=Path('work/rom/graphics-title-selection-preview.bin');target.write_bytes(result)
report={'status':'Visual review build, not a new delivered ROM release','base_sha256':hashlib.sha256(source).hexdigest(),'preview_sha256':hashlib.sha256(result).hexdigest(),'changed_bytes':len(changed),'checksum':f'{checksum:04X}','records':records,'notes':['Original portrait artwork and forms preserved, including base-form Vegeta and lavender-haired Trunks.','Logo colors preserved for legibility.','HUD implementation and special-attack effects are separate pending work.']}
(OUT/'paletas-y-verificacion.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for cid in range(11):
 steps_path=Path(f'work/selection-review/steps-{cid:02}.json');steps=json.loads(steps_path.read_text())
 for s in steps:s.pop('save',None);s.pop('dump_ram',None)
 steps[-1]['save']=str(OUT/f'seleccion-{cid:02}-despues.png')
 if cid==0:steps[6]['save']=str(OUT/'presentacion-despues.png')
 local=Path(f'work/selection-review/after-steps-{cid:02}.json');local.write_text(json.dumps(steps))
 proc=subprocess.run([sys.executable,'work/emulator/check_rom.py',str(target),str(local)],capture_output=True,text=True)
 assert proc.returncode==0,proc.stderr
 state=json.loads(proc.stdout.splitlines()[-1]);assert state['player1']==cid
 print(cid,CHAR_NAMES[cid],'revisado',flush=True)
print('Updated title and all selection palettes; preview captures saved.',flush=True)
