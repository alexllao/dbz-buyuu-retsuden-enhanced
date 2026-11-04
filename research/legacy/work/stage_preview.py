from pathlib import Path
import sys,struct,zlib,binascii,json
sys.path.insert(0,str(Path(__file__).parent))
from extract_sprite import b,u16,u32,unpack,rgb,frame
def png_rgba(path,W,H,pixels,scale=1):
 raw=bytearray()
 for y in range(H*scale):
  raw.append(0)
  for x in range(W*scale):raw.extend(pixels[(y//scale)*W+x//scale])
 def chunk(k,d):return struct.pack('>I',len(d))+k+d+struct.pack('>I',binascii.crc32(k+d)&0xffffffff)
 Path(path).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W*scale,H*scale,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
def stage_palette(stage):
 # Confirmed 0x90E4: D1=0x16 (22 colors), not decimal 16.
 return [0]*32+[u16(0x19E51E+48*stage+2*i) for i in range(22)]+[u16(0x9102+2*i) for i in range(10)]
def render_stage(stage,pal=None):
 graphics=u32(0x1769CA+4*stage);tiles,meta=unpack(graphics)
 ptr=0x18C168+2*stage;entry=ptr+u16(ptr);maps=[]
 while u32(entry)!=0xffffffff:
  maps.append(u32(entry));entry+=4
  assert len(maps)<12
 assert maps
 widths=[u16(m)*8 for m in maps]
 W=sum(widths);H=512
 if pal is None:pal=stage_palette(stage)
 pixels=[]
 for y in range(H):
  for m,strip_width in zip(maps,widths):
   for x in range(strip_width):
    attr=u16(m+2+2*((y//8)*(strip_width//8)+x//8))
    tile=attr&0x7ff;sx=x%8;sy=y%8
    if attr&0x800:sx=7-sx
    if attr&0x1000:sy=7-sy
    off=tile*32+sy*4+sx//2
    if off>=len(tiles):raise ValueError((stage,tile,len(tiles)))
    idx=(tiles[off]>>(4 if sx%2==0 else 0))&15
    color=pal[((attr>>13)&3)*16+idx]
    pixels.append((*rgb(color),255))
 meta.update({'stage_id':stage,'graphics_offset':hex(graphics),'map_offsets':[hex(m) for m in maps],'strip_widths':widths,'width':W,'height':H,'palette_offset':hex(0x19E51E+48*stage),'note':'All map strips in the stage list, static rendering; scrolling, dynamic layers and animation not emulated.'})
 return W,H,pixels,meta
if __name__=='__main__':
 out=Path('work/stages');out.mkdir(exist_ok=True)
 W,H,pix,meta=render_stage(0)
 png_rgba(out/'stage-00-original.png',W,H,pix)
 (out/'stage-00.json').write_text(json.dumps(meta,indent=2))
 print(meta)
