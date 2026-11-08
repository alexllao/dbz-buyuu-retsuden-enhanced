; Solo Goku y su tecnica C01: cinco disparos con animacion nativa.
advance:
 cmpi.w #0x0c01,(A0)
 bne.w @native_advance
 tst.b (0x58,A0)
 bne.w @native_advance
 tst.w (0x6,A0)
 bne.w @check_slots
 cmpi.w #0x003c,(0x28,A0)
 bcc.w @check_slots
 ; Sin ki para la rafaga completa: cerrar con el final nativo sin disparar.
 clr.w D5
 move.b #0x01,D5
 rts
check_slots:
 cmpi.b #0x03,(0x3a,A0)
 bcs.w @native_advance
 cmpi.b #0x05,(0x3a,A0)
 bcc.w @native_advance
 move.l D0,-(SP)
 move.l A1,-(SP)
 clr.w D0
 move.b (0x3a,A0),D0
 subi.w #0x0003,D0
 mulu.w #0x001e,D0
 lea (0xe2,A0),A1
 adda.w D0,A1
 tst.b (A1)
 beq.w @slot_free
 movea.l (SP)+,A1
 move.l (SP)+,D0
 clr.w D5
 move.b (0x4,A0),D5
 rts
slot_free:
 movea.l (SP)+,A1
 move.l (SP)+,D0
native_advance:
 jmp 0x000209dc.l

animation:
 lea (0x0002025c).l,A1
 cmpi.w #0x0401,D0
 bne.w @animation_done
 tst.b (0x58,A0)
 bne.w @animation_done
 lea (0x003da7fe).l,A1
 move.w #0x0400,D0
animation_done:
 rts

slot:
 tst.b (0x58,A0)
 bne.w @old_slot
 cmpi.w #0x0c01,(A0)
 bne.w @old_slot
 cmpi.w #0x0003,D0
 bcs.w @old_slot
 subi.w #0x0003,D0
old_slot:
 lea (0x0001d394).l,A1
 adda.w D0,A1
 move.b (A1),D0
 jmp 0x0001d172.l

debit:
 tst.b (0x58,A0)
 bne.w @native_debit
 cmpi.w #0x0c01,(A0)
 bne.w @native_debit
 move.w (0x28,A0),D0
 subi.w #0x000c,D0
 bpl.w @store_ki
 clr.w D0
store_ki:
 move.w D0,(0x28,A0)
 rts
native_debit:
 jmp 0x00013610.l

damage:
 sub.b (0x53,A0),D1
 bcc.w @nonnegative
 clr.w D1
nonnegative:
 tst.b (0x58,A1)
 bne.w @damage_done
 cmpi.w #0x0c01,(A1)
 bne.w @damage_done
 cmpi.b #0x20,(0x7c,A1)
 bne.w @damage_done
 mulu.w #0x0003,D1
 divu.w #0x0005,D1
damage_done:
 rts
