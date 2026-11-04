"""Genera un mapa ASM de estudio; nunca afirma recuperar el fuente original."""
from pathlib import Path
import argparse,csv,json,hashlib,re,shutil

def operation(assembly):
    op=assembly.strip().split()[0].lower().split('.')[0]
    if op in ['move','movea','moveq','movem','movep']:return 'Transfiere valores entre los operandos; el sufijo indica el tamaño.'
    if op=='lea':return 'Calcula una dirección y la deja en un registro de direcciones.'
    if op=='pea':return 'Apila una dirección efectiva.'
    if op in ['jsr','bsr']:return 'Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.'
    if op=='jmp':return 'Salta a otra dirección sin apilar un retorno nuevo.'
    if op=='rts':return 'Regresa usando la dirección de retorno de la pila.'
    if op=='rte':return 'Regresa de una excepción y restaura el estado del procesador.'
    if op in ['cmp','cmpa','cmpi','cmpm','tst']:return 'Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.'
    if op.startswith('db'):return 'Decrementa un contador y aplica la condición del bucle.'
    if op.startswith('b') and op not in ['bset','bclr','bchg','btst']:return 'Bifurcación según la condición indicada por el mnemónico.'
    if op=='bset':return 'Establece el bit indicado.'
    if op=='bclr':return 'Borra el bit indicado.'
    if op=='bchg':return 'Invierte el bit indicado.'
    if op=='btst':return 'Comprueba el bit indicado y actualiza la condición de cero.'
    if op.startswith(('add','sub')):return 'Operación aritmética de suma o resta sobre los operandos.'
    if op in ['muls','mulu','divs','divu']:return 'Multiplicación o división; el mnemónico distingue signo y tamaño.'
    if op in ['and','andi','or','ori','eor','eori','not']:return 'Operación lógica o máscara de bits.'
    if op in ['clr','neg','negx','ext','swap']:return 'Transforma el operando: borrar, negar, extender signo o intercambiar mitades.'
    if op.startswith(('asl','asr','lsl','lsr','rol','ror','roxl','roxr')):return 'Desplaza o rota bits según la operación indicada.'
    if op=='nop':return 'Instrucción sin efecto lógico previsto.'
    if op in ['link','unlk']:return 'Prepara o deshace un marco de pila.'
    if op in ['reset','stop','trap','trapv','illegal']:return 'Operación de control o excepción del procesador; requiere interpretar su contexto.'
    if op.startswith('s'):return 'Escribe o comprueba una condición; consultar el mnemónico y los operandos.'
    return 'Operación 68000; significado concreto del juego pendiente de identificar.'

def spanish_copy(source,dest,purpose):
    original=source.read_text(encoding='utf-8');lines=[]
    lines += ['; COPIA DIDÁCTICA ANOTADA EN CASTELLANO', '; '+purpose,
              '; Las instrucciones/directivas conservan la fuente del parche.',
              '; Los comentarios de operación no prueban por sí solos el significado del juego.', '']
    macros={'48e7fffe':'Guarda los registros del llamador.', '40e7':'Guarda el registro de estado en la pila.',
            '46df':'Restaura el registro de estado desde la pila.', '4cdf7fff':'Restaura los registros guardados.'}
    for raw in original.splitlines():
        code=raw.split(';',1)[0].rstrip()
        if not code.strip():continue
        if code.strip().endswith(':'):
            name=code.strip()[:-1]
            purpose_line={'actor_input':'Entrada por actor: control humano, cola de pulsaciones y acción previa.',
                          'animation_recovery':'Recorte de la recuperación final de golpes básicos en las condiciones admitidas.',
                          'animation_settle':'Transición visual final; otra acción cancela esta transición.',
                          'entry':'Entrada del gancho; conserva registros y vuelve a la ruta nativa.',
                          'actor':'Comprueba condiciones del comando nuevo para un actor humano.',
                          'pre_input':'Consume C mientras está retenida la maniobra, antes del historial nativo.',
                          'consume':'Enmascara el botón de vuelo en los campos de entrada del actor.',
                          'save_history':'Guarda temporalmente el historial para no modificarlo si el comando falla.',
                          'restore_history':'Restaura el historial original tras consultar el reconocedor nativo.'}.get(name)
            if purpose_line:lines += ['', '; '+purpose_line]
            lines.append(code);continue
        if code.lstrip().startswith('.hex '):
            token=code.strip()[5:].replace(' ','').lower();comment=macros.get(token,'Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.')
        else:comment=operation(code)
        lines.append(code+' ; '+comment)
    # Ignoring comments, the copied patch must keep exactly the original input tokens.
    tokenize=lambda s:[l.split(';',1)[0].strip() for l in s.splitlines() if l.split(';',1)[0].strip()]
    assert tokenize(original)==tokenize('\n'.join(lines)),source
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--rom',required=True);ap.add_argument('--listing',required=True);ap.add_argument('--functions',required=True);ap.add_argument('--out',required=True);ap.add_argument('--known',default=str(Path(__file__).with_name('known-regions-es.json')));ap.add_argument('--capstone-dir');ap.add_argument('--patch-repo');args=ap.parse_args()
    rom=Path(args.rom).read_bytes();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);known=json.loads(Path(args.known).read_text(encoding='utf-8'));digest=hashlib.sha256(rom).hexdigest();assert digest==known['romSha256'],'La base no coincide con la ROM original auditada.'
    labels={int(k,16):v for k,v in known['labels'].items()};functions=list(csv.DictReader(Path(args.functions).open(encoding='utf-8'),delimiter='\t'));funs={int(x['address'],16):x for x in functions};rows=list(csv.DictReader(Path(args.listing).open(encoding='utf-8'),delimiter='\t'));instructions={}
    capstone=None
    if args.capstone_dir:
        import sys;sys.path.insert(0,args.capstone_dir)
        from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
        capstone=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
    for row in rows:
        a=int(row['address'],16);data=bytes.fromhex(row['hex']);assert rom[a:a+len(data)]==data
        asm=row['assembly'];provenance='Clasificación existente de Ghidra; no equivale a ejecución observada.'
        if capstone:
            decoded=list(capstone.disasm(data,a,count=1))
            if len(decoded)==1 and decoded[0].size==len(data):asm=decoded[0].mnemonic+' '+decoded[0].op_str
        instructions[a]=(len(data),asm,provenance)
    audited=[]
    if capstone:
        for region in known['regions']:
            lo=int(region['start'],16);hi=int(region['endExclusive'],16);decoded=list(capstone.disasm(rom[lo:hi],lo));assert sum(x.size for x in decoded)==hi-lo,region
            for a in list(instructions):
                if lo<=a<hi or a<lo<a+instructions[a][0]:del instructions[a]
            for x in decoded:instructions[x.address]=(x.size,x.mnemonic+' '+x.op_str,'Tramo de código auditado, delimitado explícitamente; ver índice de regiones.')
            audited.append(region)
    # Existing Ghidra classifications remain hypotheses. Unknown bytes are not decoded.
    ordered=sorted(instructions);cursor=0;codebytes=0;opaque=0;gaps=[];asm=[]
    asm += ['; DRAGON BALL Z BUYUU RETSUDEN - MAPA ASM DE ESTUDIO EN CASTELLANO',
            '; NO ES EL CÓDIGO FUENTE ORIGINAL. NO ES UN PROYECTO DE RECOMPILACIÓN VALIDADO.',
            '; El mapa cubre todas las direcciones: instrucciones clasificadas + regiones INCBIN.',
            '; INCBIN puede contener datos, gráficos, relleno o código todavía no identificado.',
            '; No se ha convertido cada byte de la ROM en una instrucción 68000.',
            '; Los comentarios automáticos describen operaciones, no inventan funciones del juego.',
            '; SHA-256 de la base: '+digest,
            '; Necesitas tu propio original.bin; no se distribuye con este listado.',
            '; Jugador 1: RAM $FFE75E; jugador 2: $FFE886; estructura nativa $128 bytes.',
            '; No reutilizar libremente $118..$11F del actor: son temporizadores nativos.',
            '','        org $000000','']
    def gap(lo,hi):
        nonlocal opaque
        if hi<=lo:return
        opaque+=hi-lo;gaps.append({'start':lo,'endExclusive':hi,'bytes':hi-lo})
        asm.extend([f'zona_no_clasificada_{lo:06X}:',f'        incbin "original.bin",${lo:06X},${hi-lo:X} ; {hi-lo} bytes sin clasificar como instrucciones en este mapa.',''])
    for a in ordered:
        n,text,provenance=instructions[a]
        assert a>=cursor,(hex(a),hex(cursor));gap(cursor,a)
        if a in labels:
            asm.extend(['; IDENTIFICADO: '+labels[a]['description'],labels[a]['name']+':'])
        elif a in funs:asm.extend(['; Función delimitada por Ghidra; papel concreto pendiente.',f'rutina_{a:06X}:'])
        asm.append(f'        {text:<48} ; ${a:06X} [{rom[a:a+n].hex()}] {operation(text)}')
        cursor=a+n;codebytes+=n
    gap(cursor,len(rom));assert codebytes+opaque==len(rom)
    (out/'ROM_original_mapa_completo.asm').write_text('\n'.join(asm)+'\n',encoding='utf-8')
    index=['# Índice de rutinas y límites de conocimiento','','Este índice acompaña el mapa por direcciones. Los nombres didácticos no proceden del estudio original del juego.','','## Tramos auditados','']
    for region in audited:index.append(f'- `{region["start"]}..{region["endExclusive"]}` (final excluido), **{region["name"]}**: {region["description"]} Fuente: `{region["source"]}`.')
    index+=['','## Funciones de la base Ghidra','','Dirección | Nombre de Ghidra | Bytes del cuerpo | Descripción','--- | --- | ---: | ---']
    for f in functions:
        a=int(f['address'],16);note=labels.get(a,{}).get('description','Papel del juego pendiente; límites inferidos por análisis estático.')
        index.append(f'`${a:06X}` | `{f["name"]}` | {f["bodyBytes"]} | {note}')
    (out/'INDICE_RUTINAS.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    (out/'regiones_sin_clasificar.json').write_text(json.dumps(gaps,indent=2)+'\n')
    shutil.copyfile(args.known,out/'regiones_identificadas.json');shutil.copyfile(args.functions,out/'funciones_ghidra.tsv')
    vectors=[{'numero':i,'offset':f'0x{i*4:06X}','valor':f'0x{int.from_bytes(rom[i*4:i*4+4],"big"):08X}','interpretacion':'Pila inicial' if i==0 else 'Dirección de reset' if i==1 else 'Vector de excepción; significado específico pendiente en este índice'} for i in range(64)]
    (out/'VECTORES_Y_CABECERA.json').write_text(json.dumps({'vectores':vectors,'sistema':rom[0x100:0x110].decode('ascii',errors='replace'),'tituloDomestico':rom[0x120:0x150].decode('ascii',errors='replace').strip(),'tituloInternacional':rom[0x150:0x180].decode('ascii',errors='replace').strip(),'nota':'Datos leídos del artefacto original; no son instrucciones.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    analysis_files=[]
    for name in ['seeds.tsv','relative-dispatch-tables.tsv']:
        source=Path(args.listing).parent/name
        if source.exists():
            target=out/'analisis'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target);analysis_files.append({'name':name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    # A small reviewable code-only extract is suitable for the repository.
    extract=['; EXTRACTOS NATIVOS AUDITADOS, COMENTADOS EN CASTELLANO','; No es todo el juego. Los tramos se delimitan por evidencia independiente.','']
    for region in audited:
        lo=int(region['start'],16);hi=int(region['endExclusive'],16);extract+=['', '; '+region['description'],f'; Fuente: {region["source"]}',f'        org ${lo:06X}',region['name']+':']
        for a in ordered:
            if lo<=a<hi:
                n,text,_=instructions[a];extract.append(f'        {text:<48} ; ${a:06X} [{rom[a:a+n].hex()}] {operation(text)}')
    (out/'rutinas_nativas_comentadas.asm').write_text('\n'.join(extract)+'\n',encoding='utf-8')
    patches=[]
    if args.patch_repo:
        repo=Path(args.patch_repo)
        for source,name,purpose in [(repo/'src/gameplay/v3/controls.asm','controles_v3_comentados.asm','Controles propios: cola de pulsaciones, recuperación y transición visual.'),(repo/'src/gameplay/v3/side.asm','cambio_lado_comentado.asm','Nuevo comando humano FBF+C; reutiliza el movimiento nativo sin golpe.'),(repo/'src/auras/c2-v4/aura.asm','auras_v4_comentadas.asm','Código propio de auras v4; atlas por jugador, paleta y restauración tras efectos.')]:
            dest=out/'parches_comentados'/name;spanish_copy(source,dest,purpose);patches.append({'source':str(source),'output':str(dest),'codeTokensPreserved':True})
        title=repo/'src/title/g/patch-operations.json'
        if capstone and title.exists():
            ops=json.loads(title.read_text(encoding='utf-8'))['patchOperations'];op=next(x for x in ops if x['address']==0x3f0500);data=bytes.fromhex(op['data']);items=list(capstone.disasm(data,op['address']));assert sum(x.size for x in items)==len(data)
            target=out/'parches_comentados/credito_titulo_comentado.asm';text=['; Ayuda propia del título: carga los glifos añadidos y reproduce la inicialización desplazada.','; El mapa y los dibujos de las letras son datos separados, no instrucciones.','; Este extracto corresponde a los bytes del registro consultado, no al fuente del juego.','        org $3F0500','cargar_credito_titulo:']
            for x in items:text.append(f'        {x.mnemonic+" "+x.op_str:<48} ; ${x.address:06X} [{x.bytes.hex()}] {operation(x.mnemonic+" "+x.op_str)}')
            target.write_text('\n'.join(text)+'\n',encoding='utf-8')
    report={'originalSha256':digest,'romBytes':len(rom),'ghidraInstructions':len(rows),'ghidraFunctions':len(functions),'studyInstructions':len(instructions),'classifiedInstructionBytes':codebytes,'unclassifiedBytes':opaque,'unclassifiedRegions':len(gaps),'completeAddressCoverage':True,'allGameCodeIdentified':False,'recompilationValidated':False,'newLinearDisassemblyOfOpaqueData':False,'patchCopies':patches,'analysisFiles':analysis_files,'tooling':'Ghidra12.1.4 instruction listing; optional Capstone5.0.6 for exactly delimited audited ranges; Python standard library for export','limits':['La cobertura completa se refiere a direcciones, no a que todo el código haya sido descubierto.','Una clasificación de Ghidra no prueba que cada instrucción se ejecute ni que no haya datos intercalados.','No se recuperan nombres, variables o comentarios originales del desarrollador.','Los comentarios automáticos de operación no sustituyen la interpretación manual del juego.','INCBIN mantiene opacos los bytes no clasificados; no se publica la ROM original.','Los bytes no clasificados pueden ser código o datos: su porcentaje de la ROM no mide el porcentaje de lógica recuperada.','El dialecto impreso mezcla una notación de estudio y directivas comunes: no se promete que un ensamblador concreto lo acepte o reproduzca el binario.']}
    (out/'INFORME_COBERTURA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['romBytes','ghidraInstructions','ghidraFunctions','studyInstructions','classifiedInstructionBytes','unclassifiedBytes','completeAddressCoverage','allGameCodeIdentified']}))
if __name__=='__main__':main()
