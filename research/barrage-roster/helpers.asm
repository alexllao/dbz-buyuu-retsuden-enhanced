; Rafagas nativas de seis personajes. No se anaden comandos ni sprites nuevos.
advance:
 jsr @selected.l
 bne.w @native_advance
 tst.w (0x6,A0)
 bne.w @check_slots
 move.w (0xe0,A0),D0
 mulu.w #0x0003,D0
 cmp.w (0x28,A0),D0
 bls.w @check_slots
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

slot:
 jsr @selected.l
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
 jsr @selected.l
 bne.w @native_debit
 move.l D1,-(SP)
 move.w (0xe0,A0),D1
 mulu.w #0x0003,D1
 divu.w #0x0005,D1
 move.w (0x28,A0),D0
 sub.w D1,D0
 bpl.w @store_ki
 clr.w D0
store_ki:
 move.w D0,(0x28,A0)
 move.l (SP)+,D1
 rts
native_debit:
 jmp 0x00013610.l

damage:
 sub.b (0x53,A0),D1
 bcc.w @nonnegative
 clr.w D1
nonnegative:
 exg A0,A1
 jsr @selected.l
 exg A0,A1
 bne.w @damage_done
 cmpi.b #0x20,(0x7c,A1)
 bcs.w @damage_done
 cmpi.b #0x22,(0x7c,A1)
 bhi.w @damage_done
 mulu.w #0x0003,D1
 divu.w #0x0005,D1
damage_done:
 rts

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
