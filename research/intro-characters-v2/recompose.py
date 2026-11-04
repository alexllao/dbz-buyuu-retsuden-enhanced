"""Recompose exact native montage pixels into BG plus palette-mask sprites.
Uses only three BODY banks so native reveal/fade timing remains separate from G.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,random,struct,hashlib,sys,math
from extract import extract,render,W,H
from lz import compress as literal
from stage_preview import png_rgba
P=Path(__file__).resolve().parent

def target():
 m=json.loads((P/'target-mapping.json').read_text());changes=json.loads((P/'merge-candidates.json').read_text())['candidates']
 for c in changes:
  for ch in c['changes']:m[str(c['cid'])][ch['source_key']]=ch['to_word']
 return m,changes

def partition(words,pixels,seed=0):
 colors=sorted(set(words));assert len(colors)<=45
 # Put white in every body bank; duplicate neutral outline into two banks.
 fixed=[{0xeee},{0xeee},{0xeee}];nodes=[c for c in colors if c!=0xeee];caps=[15-len(s) for s in fixed];assert len(nodes)<=sum(caps)
 edges=defaultdict(int)
 for gy in range(28):
  for gx in range(40):
   cnt=Counter(pixels[y*320+x] for y in range(gy*8,gy*8+8) for x in range(gx*8,gx*8+8) if pixels[y*320+x] is not None)
   for a,na in cnt.items():
    for b,nb in cnt.items():
     if a<b:edges[a,b]+=min(na,nb)
 def edge(a,b):return edges.get((min(a,b),max(a,b)),0)
 weights=[[edge(a,b) for b in nodes] for a in nodes];fscore=[[sum(edge(c,x) for x in f) for f in fixed] for c in nodes];rng=random.Random(seed);best=None;bestscore=-1
 # Empty padding slots permit moves between unequal-size banks using swaps.
 while len(nodes)<sum(caps):nodes.append(-len(nodes)-1);weights.append([0]*len(nodes));[row.append(0) for row in weights[:-1]];fscore.append([0,0,0])
 n=len(nodes)
 for run in range(20):
  labels=[g for g,cap in enumerate(caps) for _ in range(cap)];rng.shuffle(labels)
  def total():return sum(fscore[i][labels[i]] for i in range(n))+sum(weights[i][j] for i in range(n) for j in range(i) if labels[i]==labels[j])
  score=total()
  for step in range(8000):
   i,j=rng.sample(range(n),2);a,b=labels[i],labels[j]
   if a==b:continue
   delta=fscore[i][b]-fscore[i][a]+fscore[j][a]-fscore[j][b]
   for k in range(n):
    if k in [i,j]:continue
    delta+=(weights[i][k]-weights[j][k])*((labels[k]==b)-(labels[k]==a))
   temp=50*(1-step/8000)+0.1
   if delta>=0 or rng.random()<math.exp(max(-50,delta/temp)):labels[i],labels[j]=b,a;score+=delta
   if score>bestscore:bestscore=score;best=labels[:]
 banks=[set(f) for f in fixed]
 for c,g in zip(nodes,best):
  if c>=0:banks[g].add(c)
 return banks,bestscore

def rect_cover(tiledata,penalty=0.35):
 pending=set(tiledata);rects=[]
 while pending:
  x,y=min(pending,key=lambda t:(t[1],t[0]));best=None
  for h in range(1,5):
   for w in range(1,5):
    covered={(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}&pending;n=len(covered)
    score=n-penalty*(w*h-n)-0.02*(w+h)
    if best is None or score>best[0]:best=(score,w,h,covered)
  _,w,h,covered=best;rects.append((x,y,w,h));pending-=covered
 return rects

def build_candidate(seed=0):
 source=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin');base=source.read_bytes();e=extract(source);m,changes=target();owners=e['pixelOwnerCIDs'];targetpix=[m[str(cid)][f'{bank}:{index}'] if cid>=0 else None for cid,bank,index in zip(owners,e['pixelBanks'],e['pixelIndices'])];colors=set(c for c in targetpix if c is not None);banks,score=partition(colors,targetpix,seed)
 palettes=[e['report']['palettes'][0]]+[[e['report']['palettes'][i+1][0]]+sorted(banks[i])+[0]*(15-len(banks[i])) for i in range(3)];indices=[{c:i for i,c in enumerate(p) if i} for p in palettes];raw=bytearray(0x6000);nexttile=1;bg=bytearray(e['rawBGMap']);bg[:]=bytes.fromhex('8000')*2048;masks=[{} for _ in range(4)];bgdedup={};pixelbg=[0]*(W*H)
 for gy in range(28):
  for gx in range(40):
   cnt=Counter(targetpix[y*W+x] for y in range(gy*8,gy*8+8) for x in range(gx*8,gx*8+8) if targetpix[y*W+x] is not None)
   if not cnt:continue
   bank=max(range(1,4),key=lambda b:sum(n for c,n in cnt.items() if c in indices[b]));tilepix=[0]*64;over={}
   for py in range(8):
    for px in range(8):
     x=gx*8+px;y=gy*8+py;c=targetpix[y*W+x]
     if c is None:continue
     b=bank if c in indices[bank] else max((b for b in range(1,4) if c in indices[b]),key=lambda b:sum(n for color,n in cnt.items() if color in indices[b]))
     if b==bank:tilepix[py*8+px]=indices[b][c];pixelbg[y*W+x]=b
     else:over.setdefault(b,[0]*64)[py*8+px]=indices[b][c]
   data=bytes(tilepix[i]*16+tilepix[i+1] for i in range(0,64,2))
   if data not in bgdedup:bgdedup[data]=nexttile;raw[nexttile*32:nexttile*32+32]=data;nexttile+=1
   attr=0x8000|bank<<13|bgdedup[data];struct.pack_into('>H',bg,(gy*64+gx)*2,attr)
   for b,p in over.items():masks[b][gx,gy]=bytes(p[i]*16+p[i+1] for i in range(0,64,2))
 bgtiles=nexttile-1;sprites=[]
 for bank in range(1,4):
  for x,y,w,h in rect_cover(masks[bank]):
   if nexttile<0x210 and nexttile+w*h>0x20a:nexttile=0x210
   tile=nexttile
   for tx in range(w):
    for ty in range(h):
     data=masks[bank].get((x+tx,y+ty),b'\0'*32);raw[nexttile*32:nexttile*32+32]=data;nexttile+=1
   sprites.append(dict(x=x*8,y=y*8,w=w,h=h,bank=bank,tile=tile))
 raw[0x20a*32:0x210*32]=e['rawTiles'][0x20a*32:0x210*32]
 assert nexttile<=768,dict(tiles=nexttile,sprites=len(sprites))
 # All fullbody art now lies in the BG map, with masks over it; old maps replaced by one complete mask map.
 newsprite=bytearray(struct.pack('>H',len(sprites)))
 for s in sprites:
  x=(s['x']-240)&4095;y=(s['y']-216)&4095;hi=(y>>8)<<4|(x>>8);attr=0x8000|s['bank']<<13|s['tile'];newsprite.extend(struct.pack('>HBBBB',attr,x&255,y&255,hi,(s['w']-1)*4+s['h']-1))
 line=[]
 for y in range(224):
  active=[s for s in sprites if s['y']<=y<s['y']+s['h']*8];count=len(active)+(9 if 104<=y<112 else 0);pixels=sum(s['w']*8 for s in active)+(144 if 104<=y<112 else 0);line.append(dict(y=y,sprites=count,pixels=pixels))
 stats=dict(bodyBGUniqueTiles=bgtiles,overlaySprites=len(sprites),totalWithNativeLineSprites=len(sprites)+9,allocatedTiles=nexttile,maxLineSprites=max(x['sprites'] for x in line),maxLinePixels=max(x['pixels'] for x in line),colorWords=len(colors),paletteOptimizationScore=score)
 # Validate full static pixels by rendering all native BG entries and new sprite overlays.
 observed=[None]*(W*H)
 for gy in range(28):
  for gx in range(40):
   a=int.from_bytes(bg[(gy*64+gx)*2:][:2],'big');bank=a>>13&3;tile=a&2047
   for py in range(8):
    for px in range(8):
     idx=raw[tile*32+py*4+px//2]>>(4 if px%2==0 else 0)&15
     if idx:observed[(gy*8+py)*W+gx*8+px]=palettes[bank][idx]
 for s in sprites:
  for py in range(s['h']*8):
   for px in range(s['w']*8):
    tile=s['tile']+(px//8)*s['h']+py//8;idx=raw[tile*32+py%8*4+px%8//2]>>(4 if px%2==0 else 0)&15;x=s['x']+px;y=s['y']+py
    if idx and x<W and y<H:observed[y*W+x]=palettes[s['bank']][idx]
 assert observed==targetpix
 candidate=bytearray(base);ops=[]
 def put(a,d,label):ops.append(dict(address=a,data=bytes(d).hex(),label=label));candidate[a:a+len(d)]=d
 put(0x3c0000,literal(raw),'Body native atlas, rebuilt losslessly in shape with approved-palette targets')
 put(0x3c7000,literal(bg),'Body BG map including all10native characters and palette masks')
 put(0x3c9000,newsprite,'Secondary-color body overlay sprites, native palette fade banks1..3 only')
 put(0x3c9400,b'\0\0','Second original body sprite map now empty; all masks in first map')
 for a,v in [(0x778be,0x3c0000),(0x778ee,0x3c7000),(0x77fd0,0x3c9000),(0x77fe8,0x3c9400)]:put(a,struct.pack('>I',v),'Intro-only resource pointer')
 for bank in range(1,4):put(0x1addb2+bank*32,struct.pack('>16H',*palettes[bank]),'Repacked body palette; bank0 approvedG unchanged')
 put(0x18e,struct.pack('>H',sum(struct.unpack('>'+str((len(candidate)-512)//2)+'H',candidate[512:]))&65535),'Checksum')
 assert candidate[0x1addb2:0x1addd2]==base[0x1addb2:0x1addd2];assert candidate[0x1a8ea2:0x1abb4c]==base[0x1a8ea2:0x1abb4c]
 (P/'candidate.bin').write_bytes(candidate);rgb=lambda v:tuple((v>>s&7)*255//7 for s in [1,5,9]);png_rgba(P/'body-remapped-static.png',W,H,[(*rgb(c),255) if c is not None else (0,0,0,0) for c in observed],scale=2)
 modified=Counter();initial=json.loads((P/'target-mapping.json').read_text())
 for cid,b,i in zip(owners,e['pixelBanks'],e['pixelIndices']):
  if cid>=0 and m[str(cid)][f'{b}:{i}']!=initial[str(cid)][f'{b}:{i}']:modified[cid]+=1
 report=dict(status='Static target pixels exact after explicit secondaryshade adaptation; native boot QA pending',sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(candidate).hexdigest(),stats=stats,operations=ops,palettes=palettes,sprites=sprites,scanlines=line,targetMapping=m,mergeCandidatesAppliedInOrder=changes,perCIDSecondaryAdaptedVisiblePixels=dict(modified),perCIDTargetRGBErrors={str(cid):0 for cid in set(owners) if cid>=0},shapeOwnershipAndTransparencyPixelExact=True,faceGBytesUnchanged=True,bodyUsesOnlyBanks123=True)
 (P/'operations.json').write_text(json.dumps(report,indent=2));print(json.dumps(stats));return report

if __name__=='__main__':build_candidate(int(sys.argv[1]) if len(sys.argv)>1 else 0)
