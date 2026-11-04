"""Comprueba la cobertura por bytes de un mapa de estudio, sin ensamblar mnemónicos."""
from pathlib import Path
import argparse,re,hashlib,json
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--asm',required=True);ap.add_argument('--rom',required=True);ap.add_argument('--out');args=ap.parse_args()
rom=Path(args.rom).read_bytes();cursor=0;result=bytearray();instructions=0;opaque=0
for line in Path(args.asm).read_text(encoding='utf-8').splitlines():
    inc=re.search(r'\bincbin\s+"[^"]+",\$([0-9a-fA-F]+),\$([0-9a-fA-F]+)',line)
    code=re.search(r';\s*\$([0-9a-fA-F]+)\s+\[([0-9a-fA-F]+)\]',line)
    if inc:
        a,n=int(inc[1],16),int(inc[2],16);assert a==cursor,(hex(a),hex(cursor));data=rom[a:a+n];assert len(data)==n;opaque+=n
    elif code:
        a=int(code[1],16);data=bytes.fromhex(code[2]);n=len(data);assert a==cursor,(hex(a),hex(cursor));assert data==rom[a:a+n],hex(a);instructions+=1
    else:continue
    result.extend(data);cursor+=n
assert cursor==len(rom) and bytes(result)==rom
report={'asm':str(args.asm),'romSha256':hashlib.sha256(rom).hexdigest(),'bytes':len(rom),'addressCoverageAndOpcodeBytesVerified':True,'instructionLines':instructions,'opaqueBytes':opaque,'assemblyOfMnemonicsValidated':False,'note':'La igualdad usa los bytes de referencia del comentario y la ROM propia para INCBIN. No demuestra que un ensamblador acepte el dialecto o emita las mismas instrucciones.'}
if args.out:Path(args.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
