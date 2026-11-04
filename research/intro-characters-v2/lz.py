"""Native byte-LZ greedy encoder; bounded dictionary search, exact round-trip."""
import struct
from collections import defaultdict,deque

def compress(data):
 data=bytes(data);assert 0<len(data)<=0x8000
 out=bytearray(struct.pack('<H',len(data)-1));positions=defaultdict(lambda:deque(maxlen=80));i=0
 while i<len(data):
  flags_at=len(out);out.append(0);flags=0
  for bit in range(8):
   if i>=len(data):break
   best=0;dist=0;key=data[i:i+3]
   if len(key)==3:
    for pos in reversed(positions[key]):
     d=i-pos
     if d>4095:break
     n=3
     while n<18 and i+n<len(data) and data[pos+n]==data[i+n]:n+=1
     if n>best:best=n;dist=d
     if n==18:break
   length=best if best>=3 else 1
   if length==1:flags|=1<<bit;out.append(data[i])
   else:out.extend(struct.pack('<H',(dist<<4)|(length-3)))
   for pos in range(i,i+length):
    if pos+3<=len(data):positions[data[pos:pos+3]].append(pos)
   i+=length
  out[flags_at]=flags
 return bytes(out)
