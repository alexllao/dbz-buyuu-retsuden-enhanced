from pathlib import Path
import sys
sys.argv=['audit','normal']
s=Path('work/namek-native-r9/record.py').read_text()
insert='''
original_tick=tick
expected_graphics=(T/'normal/tiles.bin').read_bytes()[:0x5c00]
swapped=bytearray(len(expected_graphics));swapped[0::2]=expected_graphics[1::2];swapped[1::2]=expected_graphics[0::2]
expected_graphics=bytes(swapped);audit_count=0;audit_bad=[]
def tick(*args,**kwargs):
 global audit_count
 result=original_tick(*args,**kwargs);audit_count+=1
 actual=snap()[0x12425:0x12425+0x5c00]
 if actual!=expected_graphics:
  bad=[i for i,(a,b) in enumerate(zip(actual,expected_graphics)) if a!=b]
  if len(audit_bad)<5:save_image(T/f'audit-bad-{audit_count}.png')
  audit_bad.append(dict(frame=audit_count,chapter=chapter,firstByte=min(bad),lastByte=max(bad),bytes=len(bad)))
 return result
'''
s=s.replace('\ntry:\n begin(0,',insert+'\ntry:\n begin(0,',1)
s=s.replace('finally:\n',"finally:\n (T/'live-vram-audit.json').write_text(json.dumps(dict(frames=audit_count,mismatches=audit_bad),indent=2))\n",1)
exec(compile(s,'r9-continuous-graphics-audit','exec'),globals())
