from pathlib import Path
P=Path('work/jump-two');s=Path('work/gravity-g2/gravity.asm').read_text()
s=s.replace('dash_actor:\n','dash_actor:\n tst.b (0x58,A0)\n bne.w @dash_return\n',1)
s=s.replace(' mulu.w #0x09,D3\n divu.w #0x04,D3',' mulu.w #0x0a,D3\n divu.w #0x07,D3')
s+='''
; Recorrido diagonal propio de Goku: normal2/3, desde carrera5/4.
; La rutina original conserva sentido, plano, limites de camara y efectos.
horizontal:
 move.l D7,-(SP)
 jsr @is_jump.l
 bne.w @horizontal_native
 btst.b #0x07,(0x20,A0)
 bne.w @horizontal_run
 mulu.w #0x02,D1
 divu.w #0x03,D1
 andi.l #0x0000ffff,D1
 bra.w @horizontal_native
horizontal_run:
 mulu.w #0x05,D1
 divu.w #0x04,D1
 andi.l #0x0000ffff,D1
horizontal_native:
 move.l (SP)+,D7
 jmp 0x00021e90.l
'''
s=s.replace('duration:\n','duration:\n tst.b (0x58,A0)\n bne.w @duration_fast\n',1).replace(' move.l (SP)+,D7\n jsr 0x00020adc.l',' move.l (SP)+,D7\nduration_fast:\n jsr 0x00020adc.l',1)
s=s.replace('vertical:\n','vertical:\n tst.b (0x58,A0)\n bne.w @vertical_passthrough\n',1)
s=s.replace('horizontal:\n','horizontal:\n tst.b (0x58,A0)\n bne.w @horizontal_passthrough\n',1)
s+='\nvertical_passthrough:\n jmp 0x00021e9c.l\nhorizontal_passthrough:\n jmp 0x00021e90.l\n'
(P/'jump.asm').write_text(s)
s=Path('work/gravity-probe/assemble.ps1').read_text();(P/'assemble.ps1').write_text(s)
