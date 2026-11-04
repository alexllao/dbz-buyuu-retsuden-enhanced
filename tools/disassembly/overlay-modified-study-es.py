"""Mapa de estudio de una revisión modificada, con sus blobs ASM documentados."""
from pathlib import Path
import argparse,csv,re,json,hashlib,importlib.util,sys

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--original',required=True);ap.add_argument('--modified',required=True);ap.add_argument('--listing',required=True);ap.add_argument('--blob-listing',action='append',default=[]);ap.add_argument('--title-operations');ap.add_argument('--capstone-dir',required=True);ap.add_argument('--out',required=True);args=ap.parse_args()
    sys.path.insert(0,args.capstone_dir);from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
    dis=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
    spec=importlib.util.spec_from_file_location('spanish_study',Path(__file__).with_name('generate-study-es.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    base=Path(args.original).read_bytes();rom=Path(args.modified).read_bytes();instructions={};dropped=0;overlays=[]
    for row in csv.DictReader(Path(args.listing).open(encoding='utf-8'),delimiter='\t'):
        a=int(row['address'],16);data=bytes.fromhex(row['hex']);assert base[a:a+len(data)]==data
        if rom[a:a+len(data)]!=data:dropped+=1;continue
        xs=list(dis.disasm(data,a,count=1))
        if len(xs)==1 and xs[0].size==len(data):instructions[a]=(len(data),xs[0].mnemonic+' '+xs[0].op_str)
    pattern=re.compile(r'^([0-9a-fA-F]{8}):\s+([0-9a-fA-F]+)\s+(.+)$')
    macros={'40e7','46df','4e71','4e75'}
    for listing in args.blob_listing:
        records=[]
        for line in Path(listing).read_text(encoding='utf-8').splitlines():
            m=pattern.match(line)
            if m:records.append((int(m[1],16),bytes.fromhex(m[2]),m[3]))
        assert records,listing
        lo=records[0][0];hi=max(a+len(d) for a,d,_ in records)
        for a in list(instructions):
            if lo<=a<hi:del instructions[a]
        count=0
        for a,data,text in records:
            if rom[a:a+len(data)]!=data:
                # Filled pointer/resource tables can differ from their assembled placeholders.
                assert text.startswith('.hex '),(listing,hex(a),'instruction bytes differ');continue
            if text.startswith('.hex ') and not (data.hex() in macros or (len(data)==4 and data[:2].hex() in ['48e7','4cdf'])):continue
            decoded=list(dis.disasm(data,a));assert sum(x.size for x in decoded)==len(data),(listing,hex(a))
            for x in decoded:instructions[x.address]=(x.size,x.mnemonic+' '+x.op_str);count+=1
        overlays.append({'source':str(listing),'start':lo,'endExclusive':hi,'instructionCount':count})
    hook_ranges=[(0x8f58,8),(0x8dcc,6),(0x209dc,8),(0x20a46,6),(0x89e4,10),(0x10420,10),(0x11748,10),(0x9994,6),(0x1c2dc,6),(0x28718,6),(0x1b92c,6),(0x28ea0,6),(0x77bd0,6),(0x78094,6)]
    for a,n in hook_ranges:
        if base[a:a+n]==rom[a:a+n]:continue
        xs=list(dis.disasm(rom[a:a+n],a));assert sum(x.size for x in xs)==n,(hex(a),n)
        for old in list(instructions):
            if old<a+n and old+instructions[old][0]>a:del instructions[old]
        for x in xs:instructions[x.address]=(x.size,x.mnemonic+' '+x.op_str)
        overlays.append({'source':'Gancho documentado de la revisión','start':a,'endExclusive':a+n,'instructionCount':len(xs)})
    if args.title_operations:
        ops=json.loads(Path(args.title_operations).read_text(encoding='utf-8'))['patchOperations'];op=next(x for x in ops if x['address']==0x3f0500);a=op['address'];data=bytes.fromhex(op['data']);assert rom[a:a+len(data)]==data
        xs=list(dis.disasm(data,a));assert sum(x.size for x in xs)==len(data)
        for x in xs:instructions[x.address]=(x.size,x.mnemonic+' '+x.op_str)
        overlays.append({'source':args.title_operations,'start':a,'endExclusive':a+len(data),'instructionCount':len(xs)})
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);lines=['; MAPA ASM DE ESTUDIO DE LA REVISIÓN MODIFICADA','; No es el fuente original ni un proyecto de recompilación validado.','; Se conservan clasificaciones originales con bytes idénticos y se añaden blobs/gancho documentados.','; Datos/tablas y zonas no clasificadas se dejan como INCBIN; no se barren como instrucciones.','; SHA-256 modificado: '+hashlib.sha256(rom).hexdigest(),'; INCBIN requiere una copia local propia de modificada.bin.','        org $000000',''];cursor=0;code=0;gaps=0
    for a in sorted(instructions):
        n,text=instructions[a];assert a>=cursor,(hex(a),hex(cursor))
        if a>cursor:lines.extend([f'zona_no_clasificada_{cursor:06X}:',f'        incbin "modificada.bin",${cursor:06X},${a-cursor:X} ; Datos o código pendiente de clasificar.','']);gaps+=1
        lines.append(f'        {text:<48} ; ${a:06X} [{rom[a:a+n].hex()}] {module.operation(text)}');cursor=a+n;code+=n
    if cursor<len(rom):lines+= [f'zona_no_clasificada_{cursor:06X}:',f'        incbin "modificada.bin",${cursor:06X},${len(rom)-cursor:X} ; Región no clasificada.'];gaps+=1
    (out/'ROM_modificada_mapa_completo.asm').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    report={'modifiedSource':str(args.modified),'sha256':hashlib.sha256(rom).hexdigest(),'bytes':len(rom),'classifiedInstructions':len(instructions),'classifiedInstructionBytes':code,'unclassifiedBytes':len(rom)-code,'unclassifiedRegions':gaps,'originalInstructionsExcludedBecauseBytesChanged':dropped,'overlays':overlays,'completeAddressCoverage':True,'allGameCodeIdentified':False,'recompilationValidated':False,'limits':['Mapa de estudio ligado al hash indicado, no a futuras revisiones.','Los recursos nuevos permanecen como datos INCBIN.','No se ha demostrado la recompilación exacta del listado.']}
    (out/'INFORME_ROM_MODIFICADA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['sha256','bytes','classifiedInstructions','classifiedInstructionBytes','completeAddressCoverage']}))
if __name__=='__main__':main()
