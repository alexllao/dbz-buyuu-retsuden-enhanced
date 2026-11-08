; Guardar el tipo/potencia del lanzamiento antes de devolver el control.
; El codigo nativo calcula su dano al aterrizar; preparar otro ataque no debe
; sustituir el tipo usado en ese calculo. Dos caches de ocho bytes por victima.
capture:
 jsr 0x00020ca4.l
 .hex 48e7fffe
 .hex 40e7
 jsr @cache_address.l
 bne.w @capture_done
 clr.w (A2)
 jsr 0x0001335c.l
 ; No modificar lanzamientos internos de Meteor u otras tecnicas.
 cmpi.b #0x3a,(0x5b,A1)
 bne.w @capture_done
 move.b (0x7c,A1),(0x2,A2)
 move.b (0x52,A1),(0x3,A2)
 move.w #0x746b,(A2)
capture_done:
 .hex 46df
 .hex 4cdf7fff
 rts

impact:
 .hex 48e7fffe
 .hex 40e7
 jsr @cache_address.l
 bne.w @fallback
 cmpi.w #0x746b,(A2)
 bne.w @fallback
 jsr 0x0001335c.l
 ; Conservar en pila los valores actuales del lanzador: el especial sigue vivo.
 move.l A1,-(SP)
 clr.w D0
 move.b (0x7c,A1),D0
 lsl.w #0x08,D0
 move.b (0x52,A1),D0
 move.w D0,-(SP)
 move.b (0x2,A2),(0x7c,A1)
 move.b (0x3,A2),(0x52,A1)
 clr.w (A2)
 clr.w D0
 jsr 0x000219e4.l
 move.w (SP)+,D0
 movea.l (SP)+,A1
 move.b D0,(0x52,A1)
 lsr.w #0x08,D0
 move.b D0,(0x7c,A1)
 .hex 46df
 .hex 4cdf7fff
 rts
fallback:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x000219e4.l

cache_address:
 cmpa.l #0xffffe75e,A0
 beq.w @victim_p1
 cmpa.l #0xffffe886,A0
 beq.w @victim_p2
 .hex 023c00fb
 rts
victim_p1:
 lea (0xfffff7a0).w,A2
 .hex 003c0004
 rts
victim_p2:
 lea (0xfffff7a8).w,A2
 .hex 003c0004
 rts
