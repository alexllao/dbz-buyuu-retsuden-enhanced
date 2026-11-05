; Combos v5 reaccion original: cada ataque termina su animacion nativa antes del enlace.
; Hasta3 basicos y1 tecnica propia; sin saltos de cursor ni paso instantaneo.
; Actor104 HP rival previo;106 marca88+enlaces(0..2),pendiente04,
; confirmado10,remate20,bloqueo40;107 ventana/token/espera neutral.
; Bit7 de107: esperar el final nativo; bits0..6 guardan boton/token.
entry:
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe742).w
 bne.w @done
 tst.b (0xffffe744).w
 bne.w @done
 tst.b (0xffffe9b0).w
 bne.w @done
 tst.b (0xffffe73c).w
 bne.w @done
 tst.w (0xffffe9c4).w
 bne.w @done
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @done
 lea (0xffffe75e).w,A0
 jsr @actor.l
 lea (0xffffe886).w,A0
 jsr @actor.l
done:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x003e0000.l
actor:
 tst.b (0xbe,A0)
 bne.w @return
 jsr 0x0001335c.l
 move.b (0x106,A0),D2
 andi.b #0x88,D2
 cmpi.b #0x88,D2
 beq.w @initialized
 clr.l (0x104,A0)
 move.b #0x88,(0x106,A0)
 move.w (0x24,A1),(0x104,A0)
initialized:
 move.w (0x104,A0),D0
 move.w (0x24,A1),D1
 move.w D1,(0x104,A0)
 sub.w D1,D0
 tst.w (0x24,A0)
 beq.w @lock
 tst.w D1
 beq.w @lock
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @lock
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @lock
 btst.b #0x04,(0x1e,A0)
 bne.w @lock
 btst.b #0x06,(0x106,A0)
 bne.w @neutral_recovery
 move.b (0x5b,A1),D1
 cmpi.b #0x0b,D1
 beq.w @enemy_hurt
 cmpi.b #0x0c,D1
 beq.w @enemy_hurt
 ; Sin cadena empezada, no bloquear el primer golpe desde neutral.
 move.b (0x106,A0),D2
 andi.b #0x37,D2
 beq.w @return
 bra.w @lock
enemy_hurt:
 btst.b #0x02,(0x106,A0)
 beq.w @not_pending
 ; Bit7 de107: orden en espera hasta acabar el ataque actual.
 btst.b #0x07,(0x107,A0)
 beq.w @pending_dispatch
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @return
 bclr.b #0x07,(0x107,A0)
pending_dispatch:
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @pending_started
 moveq #0,D2
 btst.b #0x05,(0x106,A0)
 beq.w @pending_normal
 move.b (0x107,A0),D6
 move.b D6,(0xb9,A0)
 move.b (0xba,A0),D3
 cmpi.b #0x10,D6
 bcs.w @pending_mask
 move.b (0xbb,A0),D3
 bra.w @pending_mask
pending_normal:
 move.b (0x107,A0),D2
 move.b #0xff,(0xb9,A0)
 bra.w @pending_inject
pending_mask:
 bset.l D3,D2
pending_inject:
 or.b D2,(0x1a,A0)
 or.b D2,(0x1b,A0)
 or.b D2,(0x1c,A0)
 or.b D2,(0x1d,A0)
 rts
pending_started:
 bclr.b #0x02,(0x106,A0)
 clr.b (0x107,A0)
not_pending:
 btst.b #0x05,(0x106,A0)
 bne.w @finisher_running
 tst.b (0x107,A0)
 beq.w @check_normal_hit
 subq.b #0x01,(0x107,A0)
check_normal_hit:
 move.w (A0),D2
 cmpi.w #0x0400,D2
 bcs.w @maybe_idle
 cmpi.w #0x0800,D2
 bcc.w @lock
 move.b (0x5b,A0),D1
 cmpi.b #0x20,D1
 beq.w @normal_hit
 cmpi.b #0x21,D1
 beq.w @normal_hit
 cmpi.b #0x23,D1
 beq.w @normal_hit
 cmpi.b #0x24,D1
 bne.w @lock
normal_hit:
 tst.w D0
 ble.w @check_input
 bset.b #0x04,(0x106,A0)
 move.b #0x24,(0x107,A0)
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 beq.w @check_input
 ; Conservar el cursor de reaccion nativo del rival.
 bra.w @check_input
maybe_idle:
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @lock
check_input:
 btst.b #0x04,(0x106,A0)
 beq.w @return
 tst.b (0x107,A0)
 beq.w @return
 cmpi.w #0x7d,(0x28,A0)
 bcs.w @return
 tst.w (0x36,A0)
 bne.w @return
 tst.w (0x38,A0)
 bne.w @return
 moveq #0,D2
 moveq #0,D3
 move.b (0xba,A0),D3
 bset.l D3,D2
 move.b (0xbb,A0),D3
 bset.l D3,D2
 move.b D2,D5
 and.b (0x1b,A0),D2
 beq.w @buffered
 move.b D2,D3
 subq.b #0x01,D3
 and.b D2,D3
 bne.w @return
 and.b (0x1d,A0),D2
 bne.w @input_ready
buffered:
 tst.b (0x109,A0)
 beq.w @return
 move.b (0x10a,A0),D2
 and.b D5,D2
 beq.w @return
 move.b D2,D3
 subq.b #0x01,D3
 and.b D2,D3
 bne.w @return
input_ready:
 move.b (0xbc,A0),D3
 move.b (0x1b,A0),D4
 btst.l D3,D4
 bne.w @return
 move.b (0xb9,A0),D6
 cmpi.b #0xff,D6
 bne.w @special_candidate
 ; Básicos libres A/B; máximo dos transiciones, sin saltar/agacharse.
 andi.b #0x03,D4
 bne.w @return
 move.b (0x106,A0),D3
 andi.b #0x03,D3
 cmpi.b #0x02,D3
 bcc.w @return
 addq.b #0x01,(0x106,A0)
 bclr.b #0x04,(0x106,A0)
 bset.b #0x02,(0x106,A0)
 move.b D2,(0x107,A0)
 jsr @common_cancel.l
 ; Sin desplazamiento instantaneo para fabricar alcance.
 rts
special_candidate:
 ; Localizar la técnica del CID real. No copiar programas entre personajes.
 moveq #0,D0
 move.b (0x58,A0),D0
 add.w D0,D0
 lea (0x0002216a).l,A2
 adda.w D0,A2
 adda.w (A2),A2
 moveq #0x27,D7
find_command:
 tst.w (A2)
 bmi.w @no_entry
 cmp.b (0x01,A2),D6
 beq.w @command_found
 adda.w #0x0c,A2
 subq.w #0x01,D7
 bpl.w @find_command
 bra.w @return
no_entry:
 ; Token0 es el proyectil común para los CID sin fila específica.
 tst.b D6
 bne.w @return
 bra.w @commit_finisher
command_found:
 ; Estas comprobaciones nativas sólo consultan condiciones; no cobran ki.
 ; El despacho original volverá a ejecutarlas al iniciar la técnica.
 .hex 48e70200
 jsr 0x0002118c.l
 .hex 4cdf0040
 bpl.w @return
 .hex 48e70200
 jsr 0x000213a6.l
 .hex 4cdf0040
 bcs.w @return
commit_finisher:
 bset.b #0x05,(0x106,A0)
 bset.b #0x02,(0x106,A0)
 bclr.b #0x04,(0x106,A0)
 move.b D6,(0x107,A0)
 move.b D6,(0xb9,A0)
 jsr @common_cancel.l
 rts
common_cancel:
 ; Guardar la orden sin reiniciar programa, accion, cursor ni banderas nativas.
 ; El despacho original la recibira al terminar por si solo el movimiento.
 bset.b #0x07,(0x107,A0)
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
 rts
finisher_running:
 ; Cerrar las excepciones cuando termina el programa del remate.
 cmpi.w #0x0800,(A0)
 bcs.w @lock
 ; Sólo completar la técnica; nunca cancelar de vuelta a básicos.
 tst.w D0
 ble.w @return
 ; Conservar el cursor de reaccion nativo del rival.
 rts
lock:
 bset.b #0x06,(0x106,A0)
 bclr.b #0x02,(0x106,A0)
 clr.b (0x107,A0)
neutral_recovery:
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @neutral_wait
 cmpi.b #0x08,(0x5b,A1)
 bhi.w @neutral_wait
 addq.b #0x01,(0x107,A0)
 cmpi.b #0x06,(0x107,A0)
 bcs.w @return
 move.b #0x88,(0x106,A0)
 clr.b (0x107,A0)
 rts
neutral_wait:
 clr.b (0x107,A0)
return:
 rts

; Sin ayuda de prolongacion de reaccion; se usa20A4C nativo.

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
eligible_p1:
 .hex 48e71010
 lea (0xffffe75e).w,A3
 jsr @can_damage.l
 .hex 4cdf0808
 rts
eligible_p2:
 .hex 48e71010
 lea (0xffffe886).w,A3
 jsr @can_damage.l
 .hex 4cdf0808
 rts
can_damage:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @ineligible
 tst.b (0xbe,A3)
 bne.w @ineligible
 move.b (0x106,A3),D3
 andi.b #0xc8,D3
 cmpi.b #0x88,D3
 bne.w @ineligible
 btst.b #0x02,(0x106,A3)
 bne.w @ineligible
 btst.b #0x05,(0x106,A3)
 bne.w @finisher_damage
 btst.b #0x04,(0x106,A3)
 bne.w @ineligible
 move.b (0x106,A3),D3
 andi.b #0x03,D3
 beq.w @ineligible
 cmpi.w #0x0400,(A3)
 bcs.w @ineligible
 cmpi.w #0x0800,(A3)
 bcc.w @ineligible
 move.b (0x5b,A3),D3
 cmpi.b #0x20,D3
 beq.w @eligible
 cmpi.b #0x21,D3
 beq.w @eligible
 cmpi.b #0x23,D3
 beq.w @eligible
 cmpi.b #0x24,D3
 beq.w @eligible
 bra.w @ineligible
finisher_damage:
 cmpi.w #0x0800,(A3)
 bcs.w @ineligible
 move.b (0x5b,A3),D3
 cmpi.b #0x38,D3
 beq.w @eligible
 cmpi.b #0x39,D3
 beq.w @eligible
 cmpi.b #0x40,D3
 beq.w @eligible
ineligible:
 .hex 023c00fb
 rts
eligible:
 .hex 003c0004
 rts
