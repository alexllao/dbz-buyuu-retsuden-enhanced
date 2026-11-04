from pathlib import Path
import shutil,json
old=Path('work/intro-characters');p=Path('work/intro-body-refined');p.mkdir(parents=True,exist_ok=True)
for f in ['extract.py','lz.py','recompose.py']:
 shutil.copyfile(old/f,p/f)
m=json.loads((old/'target-mapping.json').read_text());changes=[]
# Keep all original gray ramps rather than flattening trousers and armor.
# Consolidate tiny near-black/trim colors instead, across the body-only banks.
for before,after,why in [(0x0006,0x0000,'Freezer near-black outline'),(0x0024,0x0000,'Recoome darkest outline'),(0x0200,0x0000,'Recoome blue-black outline'),(0x0664,0x0666,'A18 secondary neutral gray'),(0x0248,0x0246,'Recoome small warm trim'),(0x0224,0x0246,'Trunks small boot shadow'),(0x0468,0x0246,'Vegeta small armor trim')]:
 for cid,values in m.items():
  for k,v in values.items():
   if v==before:values[k]=after;changes.append(dict(cid=cid,key=k,before=before,after=after,reason=why))
# Recoome used two almost equally dark shades for skin. Share the human
# three-tone skin ramp already used by the other selected battle palettes.
for key,value in {'2:3':0x0aee,'2:4':0x08ac,'2:5':0x046a}.items():
 changes.append(dict(cid='9',key=key,before=m['9'][key],after=value,reason='Readable shared human three-tone skin ramp'));m['9'][key]=value
colors=set(v for d in m.values() for v in d.values());assert len(colors)==43,len(colors)
(p/'target-mapping.json').write_text(json.dumps(m,indent=2)+'\n');(p/'merge-candidates.json').write_text('{"candidates": []}\n')
(p/'refinement.json').write_text(json.dumps({'uniqueColors':len(colors),'changes':changes,'restored':'Unmerged original material plan gray ramps, rather than v6.2 white/black collapses','pending':'Native palette packing and user visual review'},indent=2)+'\n')
print('Prepared',len(colors),'colors; armor/trouser ramps retained')
