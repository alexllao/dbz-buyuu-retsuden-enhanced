"""Verificación pasiva de recursos cargados por la ROM, no modifica el estado."""
from pathlib import Path
import struct
def inspect(state,root,slug,label):
 at=0x12425;vram=state[at:at+65536];linear=bytearray(65536);linear[0::2]=vram[1::2];linear[1::2]=vram[0::2]
 assert linear[:0x5c00]==(root/slug/'tiles.bin').read_bytes()[:0x5c00],(slug,label,'VRAM')
 own=(root/slug/'palette.bin').read_bytes();words=list(struct.unpack('>22H',own[:44]))
 base=Path('work/combo-startup/candidate.bin').read_bytes();words+=list(struct.unpack_from('>10H',base,0x9102))
 expected=[((v>>1)&7)|(((v>>5)&7)<<3)|(((v>>9)&7)<<6) for v in words]
 actual=[int.from_bytes(state[at+65536+i*2:at+65536+i*2+2],'little') for i in range(32,64)]
 assert actual==expected,(slug,label,'32 CRAM words',actual,expected)
 return dict(variant=slug,label=label,backgroundVramExact=True,own22PaletteWordsExact=True,common10PaletteWordsExact=True)
