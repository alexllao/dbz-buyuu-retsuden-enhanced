; Prueba limitada: Goku/Vegeta humanos, en suelo. Dos puños cercanos
; y remate nativo de patadas. Ventana sólo tras daño real; reacción de impacto enlazada y acotada.
; Actor104..107: HP rival previo, marca C8+cancelaciones, ventana. Auras110..117 intactas.
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
 move.b (0x58,A0),D0
 beq.w @character_ok
 cmpi.b #0x03,D0
 bne.w @return
character_ok:
 jsr 0x0001335c.l
 move.b (0x106,A0),D2
 andi.b #0xe8,D2
 cmpi.b #0xc8,D2
 beq.w @initialized
 clr.l (0x104,A0)
 move.b #0xc8,(0x106,A0)
 move.w (0x24,A1),(0x104,A0)
initialized:
 move.w (0x104,A0),D0
 move.w (0x24,A1),D1
 move.w D1,(0x104,A0)
 sub.w D1,D0
 tst.w (0x24,A0)
 beq.w @reset
 tst.w D1
 beq.w @reset
 btst.b #0x4,(0x1e,A0)
 bne.w @reset
 move.b (0x5b,A1),D1
 cmpi.b #0x0b,D1
 beq.w @enemy_stunned
 cmpi.b #0x0c,D1
 bne.w @reset
enemy_stunned:
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @reset
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @reset
 ; El hit-stop nativo puede durar varios fotogramas. Conservar una sola
 ; continuación hasta que empiece, sin repetirla al terminar ese ataque.
 btst.b #0x02,(0x106,A0)
 beq.w @not_pending
 tst.b (0x5b,A0)
 bne.w @pending_started
 move.b (0x107,A0),D2
 or.b D2,(0x1a,A0)
 or.b D2,(0x1b,A0)
 or.b D2,(0x1c,A0)
 or.b D2,(0x1d,A0)
 move.b #0xff,(0xb9,A0)
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x02,D2
 bne.w @return
 jsr @select_kick_token.l
 rts
pending_started:
 bclr.b #0x02,(0x106,A0)
 clr.b (0x107,A0)
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
normal_link:
 move.b (0x5b,A0),D1
 cmpi.b #0x20,D1
 beq.w @basic
 cmpi.b #0x23,D1
 bne.w @clear_window
basic:
 ; Acción20 también se usa en algunos especiales: exigir el programa
 ; del puño normal cercano de Goku o Vegeta, no sólo el número de acción.
 move.w (A0),D2
 cmpi.w #0x0400,D2
 beq.w @normal_program
 cmpi.w #0x0424,D2
 bne.w @clear_window
normal_program:
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x02,D2
 bcc.w @clear_window
 tst.b (0x107,A0)
 beq.w @check_hit
 subq.b #0x01,(0x107,A0)
check_hit:
 tst.w D0
 ble.w @check_window
 cmpi.w #0x04,D0
 bcs.w @check_window
 ; Consumir la excepción al confirmar el segundo impacto. El marcador
 ; D9 ya no permite daño repetido con un tercer puño normal.
 move.b (0x106,A0),D2
 andi.b #0x03,D2
 cmpi.b #0x01,D2
 bne.w @open_window
 bset.b #0x04,(0x106,A0)
 clr.w (0x06,A1)
open_window:
 move.b #0x0c,(0x107,A0)
check_window:
 tst.b (0x107,A0)
 beq.w @return
 cmpi.w #0x7d,(0x28,A0)
 bcs.w @return
 tst.w (0x36,A0)
 bne.w @return
 tst.w (0x38,A0)
 bne.w @return
 ; Sólo una pulsación nueva A/B, nunca A+B ni C mantenido.
 moveq #0,D2
 moveq #0,D3
 move.b (0xba,A0),D3
 bset.l D3,D2
 move.b (0xbb,A0),D3
 bset.l D3,D2
 move.b D2,D5
 and.b (0x1b,A0),D2
 beq.w @try_buffer
 move.b D2,D3
 subq.b #0x01,D3
 and.b D2,D3
 bne.w @return
 and.b (0x1d,A0),D2
 bne.w @input_ready
try_buffer:
 ; Aprovechar la cola de seis actualizaciones existente para que B
 ; pulsado durante la pausa del segundo impacto no se pierda.
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
 moveq #0,D3
 move.b (0xbc,A0),D3
 move.b (0x1b,A0),D4
 btst.l D3,D4
 bne.w @return
 cmpi.b #0xc8,(0x106,A0)
 bne.w @finisher
 ; Primera prueba: dos puños de pie; no cambiar cajas para forzar patadas
 ; altas contra la pose agachada del rival en daño.
 cmpi.b #0xff,(0xb9,A0)
 bne.w @return
 andi.b #0x03,D4
 bne.w @return
 cmpi.b #0x20,D1
 bne.w @return
 move.b (0xba,A0),D3
check_alternate:
 btst.l D3,D2
 beq.w @return
 bra.w @cancel
finisher:
 ; Remate B sólo tras confirmar el segundo puño, sin A ni vuelo.
 cmpi.b #0xff,(0xb9,A0)
 bne.w @return
 move.b (0xbb,A0),D3
 btst.l D3,D2
 beq.w @return
 jsr @select_kick_token.l
cancel:
 addq.b #0x01,(0x106,A0)
 bset.b #0x02,(0x106,A0)
 move.b D2,(0x107,A0)
 ; Reinicio común nativo. No llamar 20B7E/20CD6: contienen ayudas
 ; con retornos especiales. Se conserva la entrada y el token del parser.
 jsr 0x00020ba0.l
 move.w #0xe020,D0
 jsr 0x0001319a.l
 andi.b #0x3f,(0x20,A0)
 clr.w (A0)
 clr.b (0x5b,A0)
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
 clr.b (0x10c,A0)
 clr.b (0x10e,A0)
 ; Paso corto de seguimiento sólo en el primer enlace: el empuje del
 ; impacto deja al rival fuera del alcance del siguiente puño. No mover al rival.
 move.b (0x106,A0),D0
 andi.b #0x03,D0
 cmpi.b #0x01,D0
 beq.w @follow_step
 cmpi.b #0x02,D0
 bne.w @return
follow_step:
 moveq #0x08,D3
 cmpi.b #0x02,D0
 bne.w @follow_distance
 moveq #0x10,D3
follow_distance:
 move.w (0x0a,A1),D0
 sub.w (0x0a,A0),D0
 cmpi.w #0x28,D0
 bge.w @step_right
 cmpi.w #-0x28,D0
 ble.w @step_left
 rts
step_right:
 add.w D3,(0x0a,A0)
 rts
step_left:
 sub.w D3,(0x0a,A0)
 rts
 rts
clear_window:
 clr.b (0x107,A0)
return:
 rts
reset:
 move.b #0xc8,(0x106,A0)
 clr.b (0x107,A0)
 rts

; Presupuesto del remate: hasta tres impactos de patada reales.
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
 move.b #0x15,(0xb9,A0)
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
 bne.w @victim_check
 cmpi.b #0xda,(0x106,A0)
 bne.w @victim_check
 cmpi.w #0x0803,(A0)
 beq.w @animation_half
 cmpi.w #0x0815,(A0)
 bne.w @animation_done
animation_half:
 lsr.w #0x01,D2
 bne.w @animation_done
 moveq #0x01,D2
animation_done:
 .hex 261f
 .hex 46df
 rts

; Mantener la reacción de impacto durante la ráfaga confirmada. Sólo
; daño de pie0B/0C; no ampliar derribos ni detener la recuperación al acabar.
victim_check:
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @victim_hurt
 cmpi.b #0x0c,(0x5b,A0)
 bne.w @animation_done
victim_hurt:
 cmpa.l #0xffffe75e,A0
 beq.w @victim_p1
 tst.b (0xffffe81c).w
 bne.w @animation_done
 cmpi.b #0xda,(0xffffe864).w
 bne.w @animation_done
 tst.b (0xffffe865).w
 beq.w @animation_done
 cmpi.w #0x0803,(0xffffe75e).w
 beq.w @victim_extend
 cmpi.w #0x0815,(0xffffe75e).w
 bne.w @animation_done
 bra.w @victim_extend
victim_p1:
 tst.b (0xffffe944).w
 bne.w @animation_done
 cmpi.b #0xda,(0xffffe98c).w
 bne.w @animation_done
 tst.b (0xffffe98d).w
 beq.w @animation_done
 cmpi.w #0x0803,(0xffffe886).w
 beq.w @victim_extend
 cmpi.w #0x0815,(0xffffe886).w
 bne.w @animation_done
victim_extend:
 lsl.w #0x01,D2
 bra.w @animation_done

; Daño moderado sólo para las patadas confirmadas del remate: conservar
; la fórmula y descuento nativos, usando un cuarto del valor positivo.
damage_apply:
 .hex 48e7d040
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @damage_calculate
 cmpa.l #0xffffe75e,A0
 beq.w @damage_victim_p1
 cmpa.l #0xffffe886,A0
 bne.w @damage_calculate
 tst.b (0xffffe81c).w
 bne.w @damage_calculate
 cmpi.b #0xda,(0xffffe864).w
 bne.w @damage_calculate
 tst.b (0xffffe865).w
 beq.w @damage_calculate
 cmpi.w #0x0803,(0xffffe75e).w
 beq.w @damage_scale
 cmpi.w #0x0815,(0xffffe75e).w
 bne.w @damage_calculate
 bra.w @damage_scale
damage_victim_p1:
 tst.b (0xffffe944).w
 bne.w @damage_calculate
 cmpi.b #0xda,(0xffffe98c).w
 bne.w @damage_calculate
 tst.b (0xffffe98d).w
 beq.w @damage_calculate
 cmpi.w #0x0803,(0xffffe886).w
 beq.w @damage_scale
 cmpi.w #0x0815,(0xffffe886).w
 bne.w @damage_calculate
damage_scale:
 tst.w D1
 ble.w @damage_calculate
 lsr.w #0x02,D1
 bne.w @damage_calculate
 moveq #0x01,D1
damage_calculate:
 move.w (0x24,A0),D2
 sub.w D1,D2
 bcc.w @damage_store
 clr.w D2
damage_store:
 move.w D2,(0x24,A0)
 .hex 4cdf020b
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
eligible_p1:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @ineligible
 tst.b (0xffffe81c).w
 bne.w @ineligible
 cmpi.b #0xc9,(0xffffe864).w
 bne.w @eligible_p1_kick
 cmpi.w #0x0400,(0xffffe75e).w
 beq.w @eligible
 cmpi.w #0x0424,(0xffffe75e).w
 beq.w @eligible
 bra.w @ineligible
eligible_p1_kick:
 cmpi.b #0xda,(0xffffe864).w
 bne.w @ineligible
 tst.b (0xffffe865).w
 beq.w @ineligible
 cmpi.w #0x0803,(0xffffe75e).w
 beq.w @eligible
 cmpi.w #0x0815,(0xffffe75e).w
 beq.w @eligible
 bra.w @ineligible
eligible_p2:
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @ineligible
 tst.b (0xffffe944).w
 bne.w @ineligible
 cmpi.b #0xc9,(0xffffe98c).w
 bne.w @eligible_p2_kick
 cmpi.w #0x0400,(0xffffe886).w
 beq.w @eligible
 cmpi.w #0x0424,(0xffffe886).w
 beq.w @eligible
 bra.w @ineligible
eligible_p2_kick:
 cmpi.b #0xda,(0xffffe98c).w
 bne.w @ineligible
 tst.b (0xffffe98d).w
 beq.w @ineligible
 cmpi.w #0x0803,(0xffffe886).w
 beq.w @eligible
 cmpi.w #0x0815,(0xffffe886).w
 beq.w @eligible
 bra.w @ineligible
eligible:
 .hex 003c0004
 rts
ineligible:
 .hex 023c00fb
 rts
