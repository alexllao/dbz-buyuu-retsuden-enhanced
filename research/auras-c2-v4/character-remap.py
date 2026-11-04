"""Lossless character palette-slot reservation, standalone and non-destructive.

Reads approved no-rays candidate. Relocates only A18's affected graphics,
updates her frame pointers and both palettes, expands output to4MiB. Recoome's
requested6->5 remap is rejected if alternate-colour equivalence fails.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,struct

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'no-rays/candidate.bin'
EXPECTED='87576887d9ed17478ef6cced3c3ef6d8f47b549efaa34254a73b9d545a332983'
APPEND_START=0x210000
ROM_SIZE=0x400000

def u16(data,address):return int.from_bytes(data[address:address+2],'big')
def u32(data,address):return int.from_bytes(data[address:address+4],'big')
def digest(data):return hashlib.sha256(data).hexdigest()
def unpack(data,address):
    header=int.from_bytes(data[address:address+2],'little');cursor=address+2
    assert not header&0x8000,('Not a visible native body stream',hex(address),hex(header))
    size=header+1;out=bytearray()
    while len(out)<size:
        flags=data[cursor];cursor+=1
        for bit in range(8):
            if flags>>bit&1:
                out.append(data[cursor]);cursor+=1
            else:
                token=int.from_bytes(data[cursor:cursor+2],'little');cursor+=2
                distance=token>>4;length=(token&15)+3
                assert distance>0,('Invalid backreference',hex(address),hex(cursor))
                for _ in range(length):
                    src=len(out)-distance
                    out.append(out[src] if src>=0 else 0)
            if len(out)>=size:break
    return bytes(out),{'expectedBytes':size,'actualBytes':len(out),'sourceEnd':cursor}
def literal(data):
    assert 0<len(data)<=0x8000 and len(data)%32==0
    return struct.pack('<H',len(data)-1)+b''.join(b'\xff'+data[i:i+8] for i in range(0,len(data),8))
def remap(data,old,new):
    return bytes((new if b>>4==old else b>>4)<<4 | (new if b&15==old else b&15) for b in data)
def pixels(data):
    return [v for byte in data for v in (byte>>4,byte&15)]
def palettes(data,cid):
    return {name:[u16(data,base+32*cid+2*i) for i in range(16)]
            for name,base in [('normal',0x80064),('alternate',0x801e4)]}
def frame_list(data,cid):
    gp=u32(data,0x80000+4*cid);mp=u32(data,0x80034+4*cid);frames=[]
    for fid in range(200):
        offset=u16(data,mp+2*fid)
        if offset==0xffff:return gp,mp,frames
        ptr=u32(data,gp+4*fid)
        frames.append({'pose':fid,'graphics':ptr,'pointerAddress':gp+4*fid,
                       'map':mp+2*fid+offset,'nativeDisabled':bool(data[ptr+1]&0x80)})
    raise AssertionError(('No map terminator',cid))

def build():
    source=SOURCE.read_bytes();assert digest(source)==EXPECTED
    result=bytearray(source)+bytearray(b'\xff'*(ROM_SIZE-len(source)))
    operations=[]
    def put(address,data,kind,**extra):
        data=bytes(data)
        assert address+len(data)<=len(result)
        result[address:address+len(data)]=data
        operations.append({'address':address,'data':data.hex(),'kind':kind,'bytes':len(data),**extra})
    oldpal=palettes(source,6)
    assert all(p[11]==p[4] for p in oldpal.values()),'A18 duplicate must match in normal AND alternate'
    _,_,frames=frame_list(source,6)
    newpal={name:p.copy() for name,p in oldpal.items()}
    for p in newpal.values():p[11]=0x0eee
    cursor=APPEND_START;relocated={};resources=[];frameproof=[]
    for frame in frames:
        if frame['nativeDisabled']:
            frameproof.append({**frame,'status':'Native invisible pose: header high byte negative, renderer clears map0x89FA..0x8A04'})
            continue
        address=frame['graphics'];before,meta=unpack(source,address)
        assert len(before)%32==0
        after=remap(before,11,4)
        if before!=after:
            if address not in relocated:
                if cursor&1:cursor+=1
                encoded=literal(after)
                put(cursor,encoded,'relocated_character_graphics',characterId=6,sourceAddress=address)
                relocated[address]=cursor
                resources.append({'sourceAddress':address,'destinationAddress':cursor,
                                  'decodedBytes':len(before),'encodedBytes':len(encoded),
                                  'sourceCompressedEnd':meta['sourceEnd'],
                                  'beforeDecodedSha256':digest(before),'afterDecodedSha256':digest(after),
                                  'remappedPixelCount':pixels(before).count(11)})
                cursor+=len(encoded)
            put(frame['pointerAddress'],struct.pack('>I',relocated[address]),'character_frame_pointer',characterId=6,pose=frame['pose'])
            decoded,newmeta=unpack(result,relocated[address]);assert decoded==after
        else:decoded=before
        assert 11 not in pixels(decoded),'Reserved index still appears in body graphics'
        count=u16(source,frame['map']);assert 0<count<64
        used_tiles=[]
        for sprite in range(count):
            q=frame['map']+2+6*sprite;attr=u16(source,q);size=source[q+5]
            assert ((attr>>13)&3)==0,('Unexpected nonlocal palette bank',frame['pose'],sprite)
            start=attr&0x7ff;tiles=(((size>>2)&3)+1)*((size&3)+1)
            assert (start+tiles)*32<=len(before)
            used_tiles.extend(range(start,start+tiles))
        compared=0
        for tile in used_tiles:
            bp=pixels(before[tile*32:(tile+1)*32]);ap=pixels(decoded[tile*32:(tile+1)*32])
            assert all((a==0)==(b==0) for a,b in zip(bp,ap))
            for name in oldpal:
                assert all(oldpal[name][a]==newpal[name][b] for a,b in zip(bp,ap)),(frame['pose'],name,tile)
            compared+=len(bp)
        frameproof.append({**frame,'status':'PASS normal AND alternate palette RGB-word identity; alpha and all map geometry unchanged',
                           'afterGraphics':relocated.get(address,address),'referencedTileSamples':len(used_tiles),
                           'pixelComparisonsPerPalette':compared,'sourceStreamContains11':before!=after})
    for name,base in [('normal',0x80064),('alternate',0x801e4)]:
        put(base+6*32+11*2,struct.pack('>H',0x0eee),'reserved_palette_word',characterId=6,palette=name,index=11)
    # Recoome NORMAL uses a separate frame table. His ALT retains the original
    # table and palette. Parent must integrate the conditional loader helper.
    rec=palettes(source,9)
    assert rec['normal'][6]==rec['normal'][5]
    original_rec_table,_,rec_frames=frame_list(source,9)
    cursor=(cursor+3)&~3
    rec_table_address=cursor;cursor+=4*len(rec_frames)
    rec_table=bytearray(source[original_rec_table:original_rec_table+4*len(rec_frames)])
    rec_relocated={};rec_resources=[];rec_proof=[]
    rec_newpal=rec['normal'].copy();rec_newpal[6]=0x0a6a
    for frame in rec_frames:
        if frame['nativeDisabled']:
            rec_proof.append({**frame,'status':'Native invisible marker; pointer unchanged'})
            continue
        address=frame['graphics'];before,meta=unpack(source,address);after=remap(before,6,5)
        if before!=after:
            if address not in rec_relocated:
                if cursor&1:cursor+=1
                encoded=literal(after)
                put(cursor,encoded,'relocated_normal_character_graphics',characterId=9,sourceAddress=address)
                rec_relocated[address]=cursor
                rec_resources.append({'sourceAddress':address,'destinationAddress':cursor,'decodedBytes':len(before),'encodedBytes':len(encoded)})
                cursor+=len(encoded)
            struct.pack_into('>I',rec_table,frame['pose']*4,rec_relocated[address])
            decoded,_=unpack(result,rec_relocated[address]);assert decoded==after
        else:decoded=before
        assert 6 not in pixels(decoded)
        assert all((a==0)==(b==0) and rec['normal'][a]==rec_newpal[b] for a,b in zip(pixels(before),pixels(decoded)))
        assert source[address:meta['sourceEnd']]==result[address:meta['sourceEnd']], 'ALT source changed'
        rec_proof.append({**frame,'afterNormalGraphics':rec_relocated.get(address,address),
                          'status':'PASS all decoded NORMAL pixels RGB/alpha exact; ALT source/palette/table untouched'})
    put(rec_table_address,rec_table,'conditional_normal_frame_table',characterId=9)
    put(0x80064+9*32+6*2,struct.pack('>H',0x0a6a),'reserved_normal_palette_word',characterId=9,index=6)
    assert result[0x80000+9*4:0x80000+9*4+4]==source[0x80000+9*4:0x80000+9*4+4]
    assert result[original_rec_table:original_rec_table+len(rec_table)]==source[original_rec_table:original_rec_table+len(rec_table)]
    assert result[0x801e4+9*32:0x801e4+10*32]==source[0x801e4+9*32:0x801e4+10*32]

    # Ginyu slots3/4 do not occur in any visible paired body frame.
    _,_,ginyu_frames=frame_list(source,10);ginyu_proof=[]
    for frame in ginyu_frames:
        if frame['nativeDisabled']:continue
        decoded,_=unpack(source,frame['graphics']);used=set(pixels(decoded))
        assert not used.intersection({3,4}),(frame['pose'],sorted(used))
        ginyu_proof.append({'pose':frame['pose'],'graphics':frame['graphics'],'usedIndices':sorted(used)})
    for name,base in [('normal',0x80064),('alternate',0x801e4)]:
        for index,word in [(3,0x0cac),(4,0x0a68)]:
            put(base+10*32+index*2,struct.pack('>H',word),'reserved_unused_palette_word',characterId=10,palette=name,index=index)
    assert cursor<=0x260000,hex(cursor)
    helper=f''' ; Parent integration only: replace each10-byte table fetch withJSR +2NOP:
; 0x89E4..89ED,0x10420..10429,0x11748..11751. No hooks installed here.
; D4 already holdsCID*4; A4=P1E2CE orP2E390. ReturnsselectedtableinA0.
; ClobbersCCR only, overwrittennextby0x89EE ANDI.W#FF,D1.
recoome_select_table:
    LEA ($80000).l,A0
    MOVEA.L (0,A0,D4.w),A0
    CMPI.W #$24,D4
    BNE.W @recoome_table_done
    CMPA.W #$E390,A4
    BNE.W @recoome_table_normal
    CMPI.B #9,($E7B6).w
    BEQ.W @recoome_table_done
@recoome_table_normal:
    LEA (${rec_table_address:X}).l,A0
@recoome_table_done:
    RTS
'''
    (ROOT/'character-remap.asm').write_text(helper,encoding='utf-8')
    put(0x1a4,struct.pack('>I',ROM_SIZE-1),'cartridge_rom_end')
    checksum=sum(struct.unpack('>'+str((len(result)-0x200)//2)+'H',result[0x200:]))&65535
    put(0x18e,struct.pack('>H',checksum),'sega_checksum')
    allowed={i for op in operations if op['address']<len(source) for i in range(op['address'],op['address']+op['bytes'])}
    assert all(i in allowed for i,(a,b) in enumerate(zip(source,result)) if a!=b)
    shared=[]
    for cid in range(11):
        if cid==6:continue
        _,_,others=frame_list(source,cid)
        for f in others:
            if f['graphics'] in relocated:shared.append({'characterId':cid,'pose':f['pose'],'sourceGraphics':f['graphics']})
    rec_checks={name:{'source6':f'{p[6]:04X}','target5':f'{p[5]:04X}','equal':p[6]==p[5]} for name,p in rec.items()}
    assert rec_checks['normal']['equal'] and not rec_checks['alternate']['equal']
    report={'status':'Integration fragment: A18 verified both palettes; Recoome NORMAL table prepared, ALT untouched; parent MUST install conditional graphics loader before runtime validation',
            'sourceRom':str(SOURCE),'sourceSha256':digest(source),'outputRom':str(ROOT/'character-remap.bin'),
            'outputSha256':digest(result),'outputBytes':len(result),
            'a18':{'characterId':6,'pixelIndexRemap':{'11':4},'reservedIndex':11,'newPaletteWord':'0EEE',
                   'duplicateEqualityBothPalettes':True,'frameCount':len(frames),
                   'visibleFrames':sum(not f['nativeDisabled'] for f in frames),
                   'nativeInvisibleFrames':sum(f['nativeDisabled'] for f in frames),
                   'allVisibleMappedPixelsNormalAndAlternateExact':True,
                   'relocatedResourceCount':len(resources),'resources':resources,'frames':frameproof,
                   'externalPairedCharacterReferencesToSameSourceStreams':shared,
                   'sharedSourceSafety':'Original source streams are untouched. Only A18 frame pointers are updated.'},
            'recoome':{'normalPixelRemap':{'6':5},'normalReservedPalette6':'0A6A','normalPrepared':True,'conditionalHookInstalled':False,
                       'normalTableAddress':rec_table_address,'originalTableAddress':original_rec_table,
                       'normalVisibleFrames':sum(not f['nativeDisabled'] for f in rec_frames),
                       'resources':rec_resources,'frames':rec_proof,
                       'duplicateChecks':rec_checks,
                       'normalProof':'Every decoded graphics pixel is RGB-word/alpha identical using remapped6->5 and new normalpalette6A6A. Maps unchanged.',
                       'alternateProof':'Original compressed streams, original frame table, global CID9table pointer and alternate palette are byte-identical; root helper must retain that original table for P2mirror.',
                       'paletteChoice':{'nativeCode':'0xFE98..0xFEB0','normal':'P1 always; P2 when CID differs fromP1','alternate':'P2 only when CIDP2==CIDP1','actorFlag':'No extra per-actor costume flag established; use native side+CID comparison.',
                                        'conditionalHookSites':[{'address':a,'bytes':10,'replacedBytes':source[a:a+10].hex()} for a in [0x89e4,0x10420,0x11748]],
                                        'helperAssembly':helper,
                                        'contextProof':'All three fetches useD4=CID*4, A4=E2CE(P1)/E390(P2), returnA0=frame-table, and nextANDI.WFF,D1 overwritesCCR. Helper changesA0/CCR only.',
                                        'notBodyFetches':['0xA146/0xA1BA are portrait loaders with palette4026E/403CE, not table80000body fetches']}},
            'ginyu':{'reservedIndices':{'3':'0CAC','4':'0A68'},'appliedTo':['normal','alternate'],
                     'visibleFrames':len(ginyu_proof),'noIndex3Or4InAnyVisiblePairedBodyGraphics':True,'frames':ginyu_proof,
                     'knownInitialSharedFX':'SourcesA71C andB484 use neither3nor4; broader effect consumer proof remains outside this fragment.'},
            'knownInitialFXCoverage':{'streams':[{'source':'0xA71C','destinationVRAM':'0x6C00','bytes':1024,'usedIndices':[7,8,9,10]},
                                                   {'source':'0xB484','destinationVRAM':'0x7C00','bytes':1024,'usedIndices':[6,8,9,13,15]}],
                                      'readOnlyRuntime':'A18 andRecoome standing A/B impact fixtures observed6C00 sprites withpalettebank2(stage) and3(common), not0/1. No7C00sprite consumer observed in these contact fixtures.',
                                      'limit':'Never infer player-palette ownership from VRAM buffer location. Full helper/projectile consumer coverage is not established. SourceB484 contains index6 and would be affected IF any untested renderer assigned it to normalRecoome palette.'},
            'appendRange':{'start':APPEND_START,'endExclusive':cursor},
            'unchanged':['All original compressed source graphics','Collision tables and code','Control code','All sprite maps and pose positions','Recoome global CID9graphics-table pointer and original frame table','Recoome alternate palette','Original shared effect streams atA71C/B484'],
            'patchOperations':operations,
            'applyInstructions':'Extend parent candidate withFF to4MiB, then apply address(integer)/data(hex) operations. Recompute checksum after adding any further parent patches. Addresses0x210000..appendRange.endExclusive are reserved for these streams.',
            'limitations':['Requires parent conditional Recoome loader hook: this file alone changes normalpalette6 while original globalgraphics pointer still remains, so not a standalone playable final ROM.','Static native pose-map and palette equivalence only; no new emulator run of this4MiB output yet.','Shared helper/projectile consumers outside paired pose tables are not proven exhaustively.','A18reserved11/Ginyu3,4/Recoome6 must not be assumed safe for every separate engine effect merely because body frames are covered.','Appended streams use literal-only native byte compression; no runtime atlas upload/remap hook is added.'],
            'runtimeValidated':False,'repositoryEdited':False}
    (ROOT/'character-remap.bin').write_bytes(result)
    (ROOT/'character-remap.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','sourceSha256','outputSha256','outputBytes','appendRange']},indent=2))
    print('A18 visibleframes',report['a18']['visibleFrames'],'RecoomeNORMALvisibleframes',report['recoome']['normalVisibleFrames'],'normalTable',hex(rec_table_address),'originalTable',hex(original_rec_table),'Ginyuvisibleframes',len(ginyu_proof))

if __name__=='__main__':build()
