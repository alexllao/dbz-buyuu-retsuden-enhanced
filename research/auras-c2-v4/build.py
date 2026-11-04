from pathlib import Path
import json,struct,hashlib,sys
ROOT=Path('work/auras/colors-v4')
original=Path('work/rom/original.bin').read_bytes()
parent=Path('work/auras/no-rays/candidate.bin').read_bytes()
remap=json.loads((ROOT/'character-remap.json').read_text(encoding='utf-8'))
rom=bytearray((ROOT/'character-remap.bin').read_bytes())
assert hashlib.sha256(rom).hexdigest()==remap['outputSha256']
assert len(rom)==0x400000
resource=json.loads((ROOT/'resources.json').read_text(encoding='utf-8'))
labels=dict((k,int(v,16)) for k,v in (s.split('=') for s in (ROOT/'aura.labels.txt').read_text().splitlines()))
code=bytearray((ROOT/'aura.bin').read_bytes());table=labels['aura_map_table']-0x7b400
assert len(code)==table+768*4 and 0x7b400+len(code)<0x7d800
struct.pack_into('>768I',code,table,*resource['map_pointers'])
rom[0x7b400:0x7b400+len(code)]=code
for op in resource['operations']:
 data=bytes.fromhex(op['data']);at=op['address'];assert all(b==255 for b in rom[at:at+len(data)]),hex(at);rom[at:at+len(data)]=data
rom[0x9ece:0x9ed4]=bytes.fromhex('4ef9')+labels['aura_entry'].to_bytes(4,'big')
loadpatch=bytes.fromhex('4eb9')+labels['aura_load_graphics'].to_bytes(4,'big')+bytes.fromhex('4e71')*5
for at in [0x9994,0x1c2dc,0x28718]:rom[at:at+16]=loadpatch
helper=bytes.fromhex('4eb9')+labels['recoome_select_table'].to_bytes(4,'big')+bytes.fromhex('4e71')*2
for at in [0x89e4,0x10420,0x11748]:
 assert original[at:at+10].hex()=='41f90008000020704000';rom[at:at+10]=helper
fxpatch=bytes.fromhex('4eb9')+labels['aura_native_effect_load'].to_bytes(4,'big')
for at in [0x1b92c,0x28ea0]:
 assert original[at:at+6].hex()=='4eb9000015d2',hex(at);rom[at:at+6]=fxpatch
# Native collision geometry and routines remain byte-for-byte original.
for a,z in [(0x19e6ce,0x1a7866),(0x11c1e,0x12524),(0x21612,0x21672)]:assert rom[a:z]==original[a:z]
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>2096896H',rom[512:]))&65535)
(ROOT/'candidate.bin').write_bytes(rom)
record=dict(revision='c2-v4-character-colors',target_sha256=hashlib.sha256(rom).hexdigest(),target_bytes=len(rom),source_sha256=hashlib.sha256(original).hexdigest(),parent_sha256=hashlib.sha256(parent).hexdigest(),assembly_base='0x7B400',assembly_bytes=len(code),assembly_sha256=hashlib.sha256(code).hexdigest(),map_pointer_table=hex(labels['aura_map_table']),map_pointers=768,styles=resource['styles'],lightning_character_ids=[],glyph_remap_report='character-remap.json',loader_hooks=[hex(v) for v in [0x9994,0x1c2dc,0x28718]],graphics_table_hooks=[hex(v) for v in [0x89e4,0x10420,0x11748]],native_temporary_effect_hooks=[hex(v) for v in [0x1b92c,0x28ea0]],shared_region_guard='Dirty actorP1+116; defer reload/draw until E9C4 word and E73C byte both zero; native effect graphics decompression preserved',vram_physical_tiles=resource['physical_tiles'],map_pixel_identity=resource['map_pixel_identity'],status='Built; runtime validation pending')
(ROOT/'build.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k not in ['styles','vram_physical_tiles']},indent=2))
