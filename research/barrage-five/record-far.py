from pathlib import Path
import sys
which=sys.argv[1];s=Path('work/barrage-five/record.py').read_text();a=s.index(' for label,guard in ');z=s.index(" (root/'chapters.json')",a)
s=s[:a]+''' start('03 distancia larga',Path('work/responsive-v3/routes/0/charged.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
 for b,x,facevalue in [(P1,300,0),(P2,480,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facevalue)
 idle(20);command();idle(285);finish()
'''+s[z:];sys.argv=['record',which];exec(compile(s,'record-far','exec'),globals())
