"""Native intro montage extraction. No ROM writes; ownership follows native units.

API: extract(source, destination=None) returns raw tiles, BG map, sprite maps,
units, groups, and per-pixel owner CID/bank/index. Source 4-bank palettes retained.
CID assignment: six non-overlapping BG character footprints; sprite-map entry
ranges identify Ginyu/Freezer and Trunks/Krillin. Shared source tiles stay shared.
"""
from pathlib import Path
import struct,json,hashlib,sys
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stage_preview import png_rgba
W,H=320,224
NAMES={0:'Goku',1:'Gohan',2:'Piccolo',3:'Vegeta',4:'Trunks',5:'Cell',6:'Android18',7:'Krillin',8:'Freezer',9:'Recoome',10:'Ginyu'}

def unpack(rom,address):
 start=address;head=int.from_bytes(rom[address:address+2],'little');address+=2
 if head&0x8000:raise ValueError('Unexpected word-mode intro resource')
 size=head+1;out=bytearray()
 while len(out)<size:
  flags=rom[address];address+=1
  for bit in range(8):
   if flags>>bit&1:out.append(rom[address]);address+=1
   else:
    token=int.from_bytes(rom[address:address+2],'little');address+=2
    for _ in range((token&15)+3):
     src=len(out)-(token>>4);out.append(out[src] if src>=0 else 0)
   if len(out)>=size:break
 return bytes(out),dict(address=start,compressedEnd=address,compressedBytes=address-start,decodedBytes=len(out))

def s12(v):return v-4096 if v&2048 else v

def bg_owner(x,bank):
 if 2<=x<=8:return 2
 if 9<=x<=12:return 3
 if 15<=x<=17:return 1
 if 22<=x<=24:return 6
 if 26<=x<=31 and bank==3:return 5
 if 31<=x<=38 and bank==2:return 9
 raise ValueError(('Unknown nonblank BG unit',x,bank))

def render(extraction,palettes=None,tiles=None,group_banks=None):
 """Render exact native draw units; optional group palette reassignment.

 Returns RGBA plus owner/bank/index arrays. This is a static reconstruction,
 never an emulator screenshot. Sprite groups keep their native one-bank ABI.
 """
 palettes=palettes if palettes is not None else extraction['report']['palettes']
 raw=tiles if tiles is not None else extraction['rawTiles'];group_banks=group_banks or {}
 units=extraction['units'];lookup={u['id']:u for u in units}
 order=[u for u in units if u['kind']=='bg']+[lookup[i] for sp in reversed(extraction['report']['spriteEntries']) for i in sp['units']]
 owners=[-1]*(W*H);banks=[0]*(W*H);indices=[0]*(W*H)
 for u in order:
  for py in range(8):
   for px in range(8):
    x=u['x']+px;y=u['y']+py
    if not(0<=x<W and 0<=y<H):continue
    sx=7-px if u['flipX'] else px;sy=7-py if u['flipY'] else py;index=raw[u['tile']*32+sy*4+sx//2]>>(4 if sx%2==0 else 0)&15
    if index:at=y*W+x;owners[at]=u['cid'];banks[at]=group_banks.get(u['paletteGroup'],u['bank']);indices[at]=index
 rgb=lambda v:tuple(((v>>s)&7)*255//7 for s in [1,5,9])
 return dict(rgba=[(*rgb(palettes[b][i]),255 if c>=0 else 0) for c,b,i in zip(owners,banks,indices)],pixelOwnerCIDs=owners,pixelBanks=banks,pixelIndices=indices)

def extract(source,destination=None):
 rom=Path(source).read_bytes();raw,resource=unpack(rom,0x1a6306);bg,bg_resource=unpack(rom,0x1ad18c)
 assert len(raw)==0x6000 and len(bg)==4096
 palettes=[list(struct.unpack_from('>16H',rom,0x1addb2+32*i)) for i in range(4)]
 units=[];sprites=[];rawmaps={};groups=[]
 for y in range(32):
  for x in range(64):
   offset=(y*64+x)*2;attr=int.from_bytes(bg[offset:offset+2],'big');tile=attr&2047
   if not tile:continue
   bank=attr>>13&3;cid=bg_owner(x,bank);key=f'bg-{x:02}-{y:02}'
   units.append(dict(id=key,kind='bg',cid=cid,x=x*8,y=y*8,tile=tile,bank=bank,attr=attr,flipX=bool(attr&0x800),flipY=bool(attr&0x1000),sourceMapOffset=offset,paletteGroup=key))
   groups.append(dict(id=key,cid=cid,kind='bg',bank=bank,units=[key]))
 for address,anchorx in [(0x1ade72,240),(0x1adeda,80)]:
  n=int.from_bytes(rom[address:address+2],'big');rawmaps[address]=rom[address:address+2+n*6]
  for entry in range(n):
   q=address+2+entry*6;attr,xb,yb,hi,size=struct.unpack_from('>HBBBB',rom,q);x=s12((hi&15)*256+xb)+anchorx;y=s12((hi>>4)*256+yb)+216;tw=(size>>2&3)+1;th=(size&3)+1
   cid=(10 if entry<10 else 8) if address==0x1ade72 else (4 if entry<5 else 7)
   key=f'sprite-{address:x}-{entry:02}';children=[]
   for tx in range(tw):
    for ty in range(th):
     uid=f'{key}-tile-{tx}-{ty}';sx=tw-1-tx if attr&0x800 else tx;sy=th-1-ty if attr&0x1000 else ty
     u=dict(id=uid,kind='sprite',cid=cid,x=x+tx*8,y=y+ty*8,tile=(attr&2047)+sx*th+sy,bank=attr>>13&3,attr=attr,flipX=bool(attr&0x800),flipY=bool(attr&0x1000),sourceEntry=entry,sourceMapAddress=address,paletteGroup=key);units.append(u);children.append(uid)
   sp=dict(id=key,cid=cid,mapAddress=address,entry=entry,sourceEntryAddress=q,x=x,y=y,widthTiles=tw,heightTiles=th,attr=attr,bank=attr>>13&3,firstTile=attr&2047,sizeByte=size,rawHex=rom[q:q+6].hex(),units=children);sprites.append(sp);groups.append(dict(id=key,cid=cid,kind='sprite',bank=attr>>13&3,units=children))
 owners=[-1]*(W*H);banks=[0]*(W*H);indices=[0]*(W*H);unit_by_id={u['id']:u for u in units}
 # Native lowest SAT entry has priority. BG first, then reverse sprite entry order.
 order=[u for u in units if u['kind']=='bg']+[unit_by_id[i] for sp in reversed(sprites) for i in sp['units']]
 for u in order:
  assert u['tile']*32+32<=len(raw)
  for py in range(8):
   for px in range(8):
    x=u['x']+px;y=u['y']+py
    if not(0<=x<W and 0<=y<H):continue
    sx=7-px if u['flipX'] else px;sy=7-py if u['flipY'] else py;off=u['tile']*32+sy*4+sx//2;index=raw[off]>>(4 if sx%2==0 else 0)&15
    if index:at=y*W+x;owners[at]=u['cid'];banks[at]=u['bank'];indices[at]=index
 used={u['tile'] for u in units};tileOwners={t:sorted({u['cid'] for u in units if u['tile']==t}) for t in sorted(used)}
 unit_lookup={u['id']:u for u in units};character_hist=defaultdict(Counter)
 for u in units:
  hist=Counter(n for value in raw[u['tile']*32:u['tile']*32+32] for n in [value>>4,value&15] if n)
  u['indexUsage']=dict(sorted(hist.items()))
  character_hist[u['cid']].update({f"{u['bank']}:{i}":n for i,n in hist.items()})
 for group in groups:
  hist=Counter()
  for uid in group['units']:hist.update(unit_lookup[uid]['indexUsage'])
  group['indexUsage']=dict(sorted(hist.items()))
 report=dict(source=str(Path(source).resolve()),sourceSha256=hashlib.sha256(rom).hexdigest(),status='Read-only extraction; fullbody colors await comparison against approved battle palettes. Only big-face G approved.',width=W,height=H,tileResource=resource,bgResource=bg_resource,palettes=palettes,units=units,spriteEntries=sprites,paletteGroups=groups,usedTiles=sorted(used),sourceTileOwners=tileOwners,stats=dict(bgTileUnits=sum(u['kind']=='bg' for u in units),spriteEntries=len(sprites),spriteTileUnits=sum(u['kind']=='sprite' for u in units),uniqueReferencedTiles=len(used),highestReferencedTile=max(used),tileCapacity=768,unreferencedTiles=768-len(used),repackableFreeTilesExcludingTransparentZero=767-len(used),transparentTileZeroReserved=True,nativeDecorativeLineTiles=list(range(0x20a,0x210)),repackableFreeTilesExcludingZeroAndDecorativeLine=761-len(used),sharedTilesBetweenCharacters=sum(len(cids)>1 for cids in tileOwners.values())),relocation=dict(graphicsPointerOperand='0x778BE',bgMapPointerOperand='0x778EE',spriteMapPointerOperands={'0x1ADE72':'0x77FD0','0x1ADEDA':'0x77FE8'},graphicsVRAM='0x0000..0x5FFF',faceGraphicsVRAM='0x6000..0xBFFF fixed',bodyBGMapVRAM='0xC000..0xCFFF',faceBGMapVRAM='0xE000..0xEFFF fixed',spriteSATVRAM='0xDC00',introPaletteBanks='0x1ADDB2..0x1ADE31',bank0Face='0x1ADDB2..0x1ADDD1 fixed approved G',groupConstraint='Each BG8x8 unit and each whole native sprite entry carries one palette-bank attribute. Splitting/rebuilding sprite entries permits smaller groups but changes SAT usage.'),ownershipRules=dict(bg='CID2 columns2..8; CID3 9..12; CID1 15..17; CID6 22..24; CID5 bank3 columns26..31; CID9 bank2 columns31..38',sprites='1ADE72 entries0..9 CID10,10..16 CID8;1ADEDA entries0..4 CID4,5..7 CID7',meaning='Owner labels refer to actual native draw units, not rectangle cropping or guessed visible-pixel boundaries. Sprite portions can overlap neighbouring characters.'))
 report['characterIndexUsage']={str(cid):dict(sorted(hist.items())) for cid,hist in character_hist.items()}
 result=dict(rawTiles=raw,rawBGMap=bg,rawSpriteMaps=rawmaps,units=units,groups=groups,pixelOwnerCIDs=owners,pixelBanks=banks,pixelIndices=indices,report=report)
 if destination:
  out=Path(destination);out.mkdir(parents=True,exist_ok=True)
  (out/'body-tiles.bin').write_bytes(raw);(out/'body-bg-map.bin').write_bytes(bg)
  for a,d in rawmaps.items():(out/f'sprite-map-{a:x}.bin').write_bytes(d)
  (out/'pixel-owner-cid-plus-one.bin').write_bytes(bytes(c+1 for c in owners));(out/'pixel-bank.bin').write_bytes(bytes(banks));(out/'pixel-index.bin').write_bytes(bytes(indices));(out/'extraction.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
  rgb=lambda v:tuple(((v>>s)&7)*255//7 for s in [1,5,9]);rgba=[(*rgb(palettes[b][i]),255 if cid>=0 else 0) for cid,b,i in zip(owners,banks,indices)];png_rgba(out/'fullbody-native.png',W,H,rgba,scale=2)
 return result

if __name__=='__main__':
 source=sys.argv[1] if len(sys.argv)>1 else 'outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin';dest=sys.argv[2] if len(sys.argv)>2 else 'work/intro-characters/extracted';r=extract(source,dest);print(json.dumps(r['report']['stats']))
