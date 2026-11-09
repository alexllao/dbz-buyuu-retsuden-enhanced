from pathlib import Path
import hashlib,json
env={'__name__':'verify_source'};exec(compile(Path('work/namek-native-v3/build.py').read_text(),'reproduce-build','exec'),env)
original=env['P'];env['P']=original/'reproducibility';checks=[]
for slug in ['normal','aldea','porunga']:
 env['compile_variant'](slug)
 for name in ['gfx.lz','map.bin','map-header.bin','palette.bin','tiles.bin']:
  before=(original/slug/name).read_bytes();after=(env['P']/slug/name).read_bytes();assert before==after,(slug,name)
  checks.append(dict(variant=slug,file=name,bytes=len(after),sha256=hashlib.sha256(after).hexdigest(),exact=True))
(original/'reproducibility.json').write_text(json.dumps(checks,indent=2));print('All15 resource files reproduced exactly')
