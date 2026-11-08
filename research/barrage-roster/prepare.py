from pathlib import Path
P=Path('work/barrage-roster');P.mkdir(exist_ok=True)
s=Path('work/barrage-five/helpers.asm').read_text()
s=s.replace('; Solo Goku y su tecnica C01: cinco disparos con animacion nativa.','; Rafagas nativas de seis personajes. No se anaden comandos ni sprites nuevos.')
s=s.replace(' cmpi.w #0x0c01,(A0)\n bne.w @native_advance\n tst.b (0x58,A0)\n bne.w @native_advance',' jsr @selected.l\n bne.w @native_advance',1)
s=s.replace(' cmpi.w #0x003c,(0x28,A0)\n bcc.w @check_slots',' move.w (0xe0,A0),D0\n mulu.w #0x0003,D0\n cmp.w (0x28,A0),D0\n bls.w @check_slots')
a=s.index('animation:\n');z=s.index('\nslot:\n',a)
s=s[:a]+'''animation:
 lea (0x0002025c).l,A1
 jsr @selected.l
 bne.w @animation_done
 ; Cada CID tiene una secuencia propia en bloques de 64 bytes.
 lea (0x003db000).l,A1
 clr.w D0
 move.b (0x58,A0),D0
 lsl.w #0x6,D0
 adda.w D0,A1
 move.w #0x0400,D0
animation_done:
 rts
'''+s[z:]
s=s.replace(' tst.b (0x58,A0)\n bne.w @old_slot\n cmpi.w #0x0c01,(A0)\n bne.w @old_slot',' jsr @selected.l\n bne.w @old_slot')
s=s.replace(' tst.b (0x58,A0)\n bne.w @native_debit\n cmpi.w #0x0c01,(A0)\n bne.w @native_debit',' jsr @selected.l\n bne.w @native_debit')
s=s.replace(' move.w (0x28,A0),D0\n subi.w #0x000c,D0',' move.l D1,-(SP)\n move.w (0xe0,A0),D1\n mulu.w #0x0003,D1\n divu.w #0x0005,D1\n move.w (0x28,A0),D0\n sub.w D1,D0').replace(' move.w D0,(0x28,A0)\n rts',' move.w D0,(0x28,A0)\n move.l (SP)+,D1\n rts')
s=s.replace(' tst.b (0x58,A1)\n bne.w @damage_done\n cmpi.w #0x0c01,(A1)\n bne.w @damage_done',' exg A0,A1\n jsr @selected.l\n exg A0,A1\n bne.w @damage_done')
s=s.replace(' cmpi.b #0x20,(0x7c,A1)\n bne.w @damage_done',' cmpi.b #0x20,(0x7c,A1)\n bcs.w @damage_done\n cmpi.b #0x22,(0x7c,A1)\n bhi.w @damage_done')
s+='''
; Z=1 solo si coinciden personaje y su rafaga. No modifica registros.
selected:
 cmpi.b #0x00,(0x58,A0)
 beq.w @goku
 cmpi.b #0x03,(0x58,A0)
 beq.w @vegeta
 cmpi.b #0x05,(0x58,A0)
 beq.w @cell
 cmpi.b #0x06,(0x58,A0)
 beq.w @a18
 cmpi.b #0x07,(0x58,A0)
 beq.w @krilin
 cmpi.b #0x09,(0x58,A0)
 beq.w @recoome
 .hex 023c00fb
 rts
goku:
 cmpi.w #0x0c01,(A0)
 rts
vegeta:
 cmpi.w #0x0c23,(A0)
 rts
cell:
 cmpi.w #0x0c3a,(A0)
 rts
a18:
 cmpi.w #0x0c46,(A0)
 rts
krilin:
 cmpi.w #0x0c52,(A0)
 rts
recoome:
 cmpi.w #0x0c6a,(A0)
 rts
'''
(P/'helpers.asm').write_text(s)
s=Path('work/barrage-five/build.py').read_text().replace("P=Path('work/barrage-five')","P=Path('work/barrage-roster')").replace('base[0x3da200:0x3da900]','base[0x3da200:0x3db400]')
a=s.index('weights=[1]');z=s.index('now=datetime',a)
s=s[:a]+'''animations=[]
for cid,poses in [(0,[51,52,58,59,60,52,58,59,60,52,51]),(3,[58,59,58,57,58,59,58,57,58,59,58]),(5,[51,52,51,52,51,52,51,52,51,52,51]),(6,[51,52,51,52,51,52,51,52,51,52,51]),(7,[51,52,59,60,59,52,59,60,59,52,51]),(9,[51,52,51,52,51,52,51,52,51,52,51])]:
 weights=[1]*10+[6];unit=8;anim=b'\\x00\\x02'+(sum(weights)*unit).to_bytes(2,'big')+bytes(weights)+b'\\0'+bytes(poses);at=0x3db000+cid*64;r[at:at+len(anim)]=anim;animations.append(dict(cid=cid,address=at,bytes=len(anim),weights=weights,poses=poses,timeUnit=unit))
'''+s[z:]
s=s.replace("'DBZ BUYUU V1.0 FIVE '","'DBZ BUYUU V1.0 FIVE6 '").replace('(0x3da7fe,len(anim)+2)','*[(x[\'address\'],x[\'bytes\']) for x in animations]').replace("variant='Goku five barrage trial'","variant='Six native five-shot barrages on K4'").replace('allowed=allowed,weights=weights,poses=poses','allowed=allowed,animations=animations')
(P/'build.py').write_text(s)
(P/'assemble.ps1').write_text(Path('work/barrage-five/assemble.ps1').read_text())
print('Prepared six character-specific sequences')
