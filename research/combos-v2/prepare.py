from pathlib import Path
p=Path('work/kick-combos');p.mkdir(parents=True,exist_ok=True)
s=Path('work/combos/combo-v1.asm').read_text(encoding='utf-8')
s=s.replace('y Energy Blast nativo.','y remate nativo de patadas.').replace('movimiento especial.','movimiento especial.')
s=s.replace(' clr.b (0xb9,A0)\n rts\npending_started:', ' jsr @select_kick_token.l\n rts\npending_started:')
s=s.replace(' clr.b (0x107,A0)\nnot_pending:', ''' clr.b (0x107,A0)
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x02,D2
 bne.w @not_pending
 move.b #0x03,(0x107,A0)
not_pending:
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x02,D2
 bne.w @normal_link
 cmpi.w #0x0803,(A0)
 beq.w @kick_running
 cmpi.w #0x0815,(A0)
 beq.w @kick_running
 bra.w @return
normal_link:''')
s=s.replace(' bset.b #0x04,(0x106,A0)\nopen_window:', ' bset.b #0x04,(0x106,A0)\n clr.w (0x06,A1)\nopen_window:')
a=s.index('finisher:\n');b=s.index('cancel:\n',a)
s=s[:a]+'''finisher:
 ; Remate B sólo tras confirmar el segundo puño, sin A ni vuelo.
 cmpi.b #0xff,(0xb9,A0)
 bne.w @return
 move.b (0xbb,A0),D3
 btst.l D3,D2
 beq.w @return
 jsr @select_kick_token.l
'''+s[b:]
s=s.replace(' cmpi.b #0x01,D0\n bne.w @return',' cmpi.b #0x01,D0\n beq.w @follow_step\n cmpi.b #0x02,D0\n bne.w @return\nfollow_step:')
a=s.index('; El original descarta golpes normales')
s=s[:a]+'''; Presupuesto del remate: hasta tres impactos de patada reales.
kick_running:
 tst.w D0
 ble.w @kick_budget
 clr.w (0x06,A1)
 tst.b (0x107,A0)
 beq.w @kick_budget
 subq.b #0x01,(0x107,A0)
kick_budget:
 tst.b (0x107,A0)
 bne.w @return
 bclr.b #0x07,(0x1e,A0)
 rts
select_kick_token:
 move.b #0x12,(0xb9,A0)
 tst.b (0x58,A0)
 beq.w @return
 move.b #0x17,(0xb9,A0)
 rts

; Sólo acelerar estas animaciones cuando son el remate confirmado del
; combo. Los especiales introducidos normalmente conservan su velocidad.
animation_entry:
 jsr 0x00020a4c.l
 .hex 40e7
 .hex 2f03
 cmpa.l #0xffffe75e,A0
 beq.w @animation_actor
 cmpa.l #0xffffe886,A0
 bne.w @animation_done
animation_actor:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @animation_done
 tst.b (0xbe,A0)
 bne.w @animation_done
 cmpi.b #0xda,(0x106,A0)
 bne.w @animation_done
 cmpi.w #0x0803,(A0)
 beq.w @animation_half
 cmpi.w #0x0815,(A0)
 bne.w @animation_done
 lsr.w #0x01,D2
animation_half:
 lsr.w #0x01,D2
 bne.w @animation_done
 moveq #0x01,D2
animation_done:
 .hex 261f
 .hex 46df
 rts

; Excepción de daño acotada al segundo puño o a los impactos finitos
; del remate nativo. Fuera de estos casos se respeta la comprobación original.
damage_p1:
 jsr @eligible_p1.l
 bne.w @damage_original
 rts
damage_p2:
 jsr @eligible_p2.l
 bne.w @damage_original
 rts
damage_original:
 cmpi.b #0x38,(0xffffe7b9).w
 rts
repeat_p1:
 jsr @eligible_p1.l
 beq.w @repeat_p1_allow
 cmpi.b #0x22,D0
 beq.w @repeat_p1_allow
 jmp 0x00011efa.l
repeat_p1_allow:
 jmp 0x00011f08.l
repeat_p2:
 jsr @eligible_p2.l
 beq.w @repeat_p2_allow
 cmpi.b #0x22,D0
 beq.w @repeat_p2_allow
 jmp 0x000120da.l
repeat_p2_allow:
 jmp 0x000120e0.l
'''
for port,base in [(1,0xffffe75e),(2,0xffffe886)]:
 def loc(off):return f'(0x{base+off:08x}).w'
 s+=f'''eligible_p{port}:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @ineligible
 tst.b {loc(0xbe)}
 bne.w @ineligible
 cmpi.b #0xc9,{loc(0x106)}
 bne.w @eligible_p{port}_kick
 cmpi.w #0x0400,{loc(0)}
 beq.w @eligible
 cmpi.w #0x0424,{loc(0)}
 beq.w @eligible
 bra.w @ineligible
eligible_p{port}_kick:
 cmpi.b #0xda,{loc(0x106)}
 bne.w @ineligible
 tst.b {loc(0x107)}
 beq.w @ineligible
 cmpi.w #0x0803,{loc(0)}
 beq.w @eligible
 cmpi.w #0x0815,{loc(0)}
 beq.w @eligible
 bra.w @ineligible
'''
s+='''eligible:
 .hex 003c0004
 rts
ineligible:
 .hex 023c00fb
 rts
'''
(p/'combos-v2.asm').write_text(s,encoding='utf-8')
s=Path('work/combos/build.py').read_text().replace("Path('work/combos')","Path('work/kick-combos')").replace('combo-v1.bin','combos-v2.bin').replace('combo-v1.labels.txt','combos-v2.labels.txt')
needle="struct.pack_into('>H',rom,0x18e,"
pos=s.index(needle)
s=s[:pos]+'''needle=bytes.fromhex('4eb900020a4c');offset=base.find(needle,0x7b000,0x7b400);assert offset>=0 and base.find(needle,offset+6,0x7b400)<0
rom[offset:offset+6]=bytes.fromhex('4eb9')+struct.pack('>I',labels['animation_entry'])
'''+s[pos:]
s=s.replace("'contact checks 0x11E14/11FF8/11EF4/120D4'","'contact checks 0x11E14/11FF8/11EF4/120D4','animation helper call inside controls block'")
(p/'build.py').write_text(s)
print('Prepared kick finisher prototype')
