from pathlib import Path
import struct,zlib,binascii,json
ROM=Path(__file__).parent/'rom/original.bin'
b=ROM.read_bytes()
def u16(a):return int.from_bytes(b[a:a+2],'big')
def u32(a):return int.from_bytes(b[a:a+4],'big')
def unpack(a):
    head=int.from_bytes(b[a:a+2],'little');a+=2
    if head&0x8000: raise ValueError('word mode not implemented')
    size=head+1;out=bytearray()
    while len(out)<size:
        flags=b[a];a+=1
        for bit in range(8):
            if flags>>bit&1:
                out.append(b[a]);a+=1
            else:
                token=int.from_bytes(b[a:a+2],'little');a+=2
                length=(token&15)+3;dist=token>>4
                for _ in range(length):
                    src=len(out)-dist
                    if src>=len(out):raise ValueError('invalid backreference')
                    out.append(out[src] if src>=0 else 0)
            if len(out)>=size:break
    return out,{'size':size,'actual_size':len(out),'source_end':hex(a)}
def frame(cid=0,fid=0):
    gp=u32(u32(0x80000+4*cid)+4*fid)
    tiles,meta=unpack(gp)
    mt=u32(0x80034+4*cid)+2*fid;mp=mt+u16(mt)
    n=u16(mp);sprites=[]
    assert 0<n<64
    for i in range(n):
        q=mp+2+6*i;attr=u16(q);hi=b[q+4]
        x=((hi&15)<<8)|b[q+2];y=((hi>>4)<<8)|b[q+3]
        if x&0x800:x-=4096
        if y&0x800:y-=4096
        size=b[q+5];w=((size>>2)&3)+1;h=(size&3)+1
        sprites.append((x,y,w,h,attr))
    x0=min(s[0] for s in sprites);y0=min(s[1] for s in sprites)
    x1=max(s[0]+s[2]*8 for s in sprites);y1=max(s[1]+s[3]*8 for s in sprites)
    W=x1-x0;H=y1-y0;pixels=[0]*(W*H)
    for x,y,w,h,attr in reversed(sprites):
        start=attr&0x7ff
        for px in range(w*8):
            for py in range(h*8):
                sx=w*8-1-px if attr&0x800 else px
                sy=h*8-1-py if attr&0x1000 else py
                ti=start+(sx//8)*h+sy//8;off=ti*32+(sy%8)*4+(sx%8)//2
                assert off<len(tiles),(cid,fid,off,len(tiles))
                v=(tiles[off]>>(4 if sx%2==0 else 0))&15
                if v:pixels[(y-y0+py)*W+x-x0+px]=v
    meta.update({'character_id':cid,'frame_id':fid,'graphics_offset':hex(gp),'mapping_offset':hex(mp),'sprites':sprites,'width':W,'height':H})
    return W,H,pixels,meta
def palette(cid):return [u16(0x80064+32*cid+2*i) for i in range(16)]
def rgb(v):return tuple(((v>>s)&7)*255//7 for s in (1,5,9))
def png(path,W,H,pixels,pal,scale=4):
    raw=bytearray()
    for y in range(H*scale):
        raw.append(0)
        for x in range(W*scale):
            idx=pixels[(y//scale)*W+x//scale]
            raw.extend((*rgb(pal[idx]),255 if idx else 0))
    def chunk(k,d):return struct.pack('>I',len(d))+k+d+struct.pack('>I',binascii.crc32(k+d)&0xffffffff)
    Path(path).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W*scale,H*scale,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
if __name__=='__main__':
    out=Path('work/sprites');out.mkdir(exist_ok=True)
    for cid in range(12):
        try:
            W,H,pix,meta=frame(cid,0)
            png(out/f'char-{cid:02}.png',W,H,pix,palette(cid))
            (out/f'char-{cid:02}.json').write_text(json.dumps(meta,indent=2))
            print(cid,W,H,meta['graphics_offset'])
        except Exception as e:print(cid,type(e).__name__,str(e))
