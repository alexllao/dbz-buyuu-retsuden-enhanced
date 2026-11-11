; Cartucho de audicion independiente: no contiene el juego ni su driver.
; Reproduce escrituras YM2612/PSG a ritmo de VBlank para comprobar el boceto.
entry:
 .hex 46fc2700
 move.l #0x53454741,(0x00a14000).l
 move.w #0x0100,(0x00a11100).l
 move.w #0x0100,(0x00a11200).l
 move.w #0x8004,(0x00c00004).l
 move.w #0x8144,(0x00c00004).l
 lea (0x00001000).l,A0
 clr.w (0xfffff000).w
frame:
 move.w (0x00c00004).l,D0
 andi.w #0x0008,D0
 bne.w @frame
wait_blank:
 move.w (0x00c00004).l,D0
 andi.w #0x0008,D0
 beq.w @wait_blank
 addq.w #0x01,(0xfffff000).w
 move.w (A0)+,D7
 cmpi.w #0xffff,D7
 beq.w @finished
 tst.w D7
 beq.w @frame
 subq.w #0x01,D7
event:
 clr.w D0
 move.b (A0)+,D0
 move.b (A0)+,D1
 move.b (A0)+,D2
 addq.l #0x01,A0
 cmpi.b #0x02,D0
 beq.w @psg
 lea (0x00a04000).l,A1
 tst.b D0
 beq.w @fm_ready
 addq.l #0x02,A1
fm_ready:
 tst.b (0x00a04000).l
 bmi.w @fm_ready
 move.b D1,(A1)
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 move.b D2,(0x01,A1)
 bra.w @next
psg:
 move.b D2,(0x00c00011).l
next:
 dbf D7w,@event
 bra.w @frame
finished:
 bra.w @finished
