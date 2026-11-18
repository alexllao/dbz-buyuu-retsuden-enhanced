; Prototipo Goku/Vegeta. ↑+C tras SU lanzamiento;16KI, una persecucion
; por cadena. Movimiento y golpes calculados en ROM, nunca en el capturador.
; F800/F840: fase, usado, impactos aereos, contacto del ataque actual;
; +4 plazo, +6 ultimo tick fisico, +8 Y16.16, +C velocidad8.8,
; +E HP rival previo, +10 ventana cancel, +11 pasos de persecucion,
; +20/+24 cajas nativas receptoras, +28 validez.
frame_entry:
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe744).w
 bne.w @frame_done
 tst.b (0xffffe742).w
 bne.w @frame_done
 tst.b (0xffffe73c).w
 bne.w @frame_done
 tst.w (0xffffe9c4).w
 bne.w @frame_done
 cmpi.w #0x0100,(0xffffe756).w
 bne.w @frame_done
 lea (0xffffe75e).w,A0
 jsr @control.l
 lea (0xffffe886).w,A0
 jsr @control.l
frame_done:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x003de000.l
slots:
 lea (0xfffff800).w,A2
 lea (0xfffff840).w,A3
 cmpa.l #0xffffe75e,A0
 beq.w @slots_ready
 exg A2,A3
slots_ready:
 jsr 0x0001335c.l
 rts
control:
 jsr @slots.l
 tst.w (0x24,A0)
 beq.w @control_return
 tst.b (0xbe,A0)
 bne.w @control_return
 cmpi.b #0x04,(A2)
 beq.w @landing_queue
 cmpi.b #0x03,(A2)
 beq.w @air_control
 tst.b (A2)
 bmi.w @control_return
 cmpi.b #0x02,(A2)
 beq.w @control_return
 tst.b (0x58,A0)
 beq.w @eligible
 cmpi.b #0x03,(0x58,A0)
 bne.w @control_return
eligible:
 ; El credito no vuelve mientras siga abierta la cadena.
 tst.b (0xd22,A0)
 bne.w @observe_throw
 cmpi.w #0x01c0,(0x10,A0)
 bne.w @observe_throw
 cmpi.w #0x01c0,(0x10,A1)
 bne.w @observe_throw
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @observe_throw
 cmpi.b #0x08,(0x5b,A1)
 bhi.w @observe_throw
 clr.b (0x01,A2)
observe_throw:
 cmpi.b #0x3a,(0x5b,A0)
 bne.w @check_chase
 cmpi.b #0x17,(0x5b,A1)
 bne.w @check_chase
 tst.b (0x01,A2)
 bne.w @control_return
 move.b #0x01,(A2)
check_chase:
 cmpi.b #0x01,(A2)
 bne.w @control_return
 cmpi.b #0x17,(0x5b,A1)
 bne.w @disarm
 tst.w (0x24,A1)
 beq.w @disarm
 tst.b (0x15,A2)
 beq.w @chase_buffer_input
 subq.b #0x01,(0x15,A2)
chase_buffer_input:
 move.b (0x1b,A0),D0
 btst.l #0x00,D0
 beq.w @chase_buffer_ready
 clr.w D1
 move.b (0xbc,A0),D1
 move.b (0x1d,A0),D0
 btst.l D1,D0
 beq.w @chase_buffer_ready
 move.b #0x08,(0x15,A2)
chase_buffer_ready:
 cmpi.b #0x0e,(0x5b,A0)
 bhi.w @control_return
 cmpi.w #0x01a0,(0x10,A1)
 bcc.w @control_return
 btst.b #0x04,(0x1e,A0)
 bne.w @control_return
 btst.b #0x04,(0x1e,A1)
 bne.w @control_return
 cmpi.w #0x0010,(0x28,A0)
 bcs.w @control_return
 tst.b (0x15,A2)
 beq.w @control_return
 tst.b (A3)
 bne.w @control_return
 subi.w #0x0010,(0x28,A0)
 move.b #0x02,(A2)
 move.b #0x01,(0x01,A2)
 clr.w (0x02,A2)
 clr.l (0x10,A2)
 clr.b (0x14,A2)
 clr.b (0x15,A2)
 move.b #0x0c,(0x11,A2)
 move.w #0xffff,(0x06,A2)
 move.b #0x81,(A3)
 clr.b (0x16,A2)
 move.w (0x0a,A0),D0
 cmp.w (0x0a,A1),D0
 bcs.w @chase_side_ready
 move.b #0x01,(0x16,A2)
chase_side_ready:
 move.b #0x49,(0xffff5000).l
 jsr 0x00020ba0.l
 jsr @jump_id.l
 move.w D0,(A0)
 move.b #0x04,(0x5b,A0)
 clr.b (0xbd,A0)
 ; Consumir C solo al aceptar la nueva accion.
 clr.w D1
 move.b (0xbc,A0),D1
 moveq #-0x01,D2
 bclr.l D1,D2
 and.b D2,(0x1a,A0)
 and.b D2,(0x1b,A0)
 and.b D2,(0x1c,A0)
 and.b D2,(0x1d,A0)
 rts
disarm:
 clr.b (A2)
 clr.b (0x15,A2)
control_return:
 rts
air_control:
 cmpi.b #0x0b,(0x5b,A0)
 beq.w @air_interrupted
 cmpi.b #0x0c,(0x5b,A0)
 beq.w @air_interrupted
 tst.b (0x14,A2)
 beq.w @air_steer
 subq.b #0x01,(0x14,A2)
air_steer:
 ; Direccion manual durante la fase aerea, con los limites nativos de X.
 move.b (0x1b,A0),D1
 andi.b #0x0c,D1
 cmpi.b #0x04,D1
 beq.w @air_left
 cmpi.b #0x08,D1
 bne.w @air_check_hit
 move.w #0x0180,D0
 jsr 0x00020e04.l
 bra.w @air_check_hit
air_left:
 move.w #0x0180,D0
 jsr 0x00020e2c.l
air_check_hit:
 move.w (0x24,A1),D0
 cmp.w (0x0e,A2),D0
 bcc.w @air_no_hit
 move.b (0x5b,A0),D1
 cmpi.b #0x28,D1
 beq.w @air_hit
 cmpi.b #0x29,D1
 bne.w @air_no_hit
air_hit:
 addq.b #0x01,(0x02,A2)
 move.b #0x01,(0x03,A2)
 move.b #0x10,(0x10,A2)
 move.w #0xff40,(0x0c,A2)
 move.w #0xfec0,(0x0c,A3)
 ; Reaccion aerea de enlace: el golpe conserva su daño nativo, pero el
 ; primer/segundo basico no terminan por si solos en el derribo de suelo.
 move.l A0,-(SP)
 movea.l A1,A0
 jsr 0x00020ba0.l
 move.w #0x002f,(A0)
 move.b #0x0c,(0x5b,A0)
 movea.l (SP)+,A0
 jsr @slots.l
 move.w (0x24,A1),D0
 cmpi.b #0x02,(0x02,A2)
 bcs.w @air_no_hit
 move.b #0x24,(0x10,A2)
 move.w #0x0300,(0x0c,A2)
 move.w #0x0300,(0x0c,A3)
air_no_hit:
 move.w D0,(0x0e,A2)
 tst.b (0x10,A2)
 beq.w @control_return
 subq.b #0x01,(0x10,A2)
 tst.b (0x03,A2)
 beq.w @control_return
 move.b (0x5b,A0),D1
 cmpi.b #0x28,D1
 beq.w @air_cancel_input
 cmpi.b #0x29,D1
 bne.w @control_return
air_cancel_input:
 ; Una tecnica reconocida puede rematar; como maximo dos basicos aereos.
 move.b (0xb9,A0),D0
 cmpi.b #0x19,D0
 beq.w @air_cancel
 cmpi.b #0x06,D0
 beq.w @air_cancel
 tst.b (0x58,A0)
 bne.w @air_cancel_normal
 cmpi.b #0x05,D0
 beq.w @air_cancel
air_cancel_normal:
 cmpi.b #0x02,(0x02,A2)
 bcc.w @control_return
 move.b (0x1d,A0),D0
 clr.w D1
 move.b (0xba,A0),D1
 btst.l D1,D0
 bne.w @air_cancel
 move.b (0xbb,A0),D1
 btst.l D1,D0
 beq.w @control_return
air_cancel:
 move.b (0x1d,A0),(0x12,A2)
 move.b (0xb9,A0),(0x13,A2)
 move.b #0x06,(0x14,A2)
 ; Meteor espera la llegada al suelo: no reemplazar su buffer largo por
 ; los seis ticks destinados a un basico/ki de ejecucion aerea inmediata.
 cmpi.b #0x19,(0x13,A2)
 bne.w @air_cancel_ready
 move.b #0x30,(0x14,A2)
air_cancel_ready:
 jsr 0x00020ba0.l
 jsr @jump_id.l
 move.w D0,(A0)
 move.b #0x04,(0x5b,A0)
 clr.b (0x03,A2)
 clr.b (0x10,A2)
 rts
air_interrupted:
 move.b #0x80,(A2)
 clr.b (0x14,A2)
 clr.b (0x10,A2)
 rts
landing_queue:
 tst.b (0x14,A2)
 beq.w @landing_queue_clear
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @landing_queue_clear
 tst.w (0x24,A1)
 beq.w @landing_queue_clear
 subq.b #0x01,(0x14,A2)
 rts
landing_queue_clear:
 clr.b (A2)
 clr.b (0x14,A2)
 rts
jump_id:
 clr.w D0
 move.b (0x58,A0),D0
 mulu.w #0x03,D0
 addq.w #0x04,D0
 rts

; El dispatch nativo permanece en su nivel de pila original cuando no hay
; persecucion. Solo se envuelve a los dos actores durante la accion nueva.
dispatch:
 cmpa.l #0xffffe75e,A0
 beq.w @dispatch_player
 cmpa.l #0xffffe886,A0
 bne.w @native_dispatch
dispatch_player:
 .hex 48e7fffe
 .hex 40e7
 jsr @slots.l
 move.b (A2),D0
 cmpi.b #0x02,D0
 beq.w @dispatch_custom
 cmpi.b #0x03,D0
 beq.w @dispatch_air
 cmpi.b #0x80,D0
 beq.w @dispatch_air
 .hex 46df
 .hex 4cdf7fff
 jmp @native_dispatch.l
dispatch_air:
 ; La actualizacion de salto guardada en un puño aereo no procesa input.
 btst.b #0x02,(0x20,A0)
 bne.w @dispatch_background
 move.w (A0),D2
 tst.w D2
 beq.w @dispatch_idle
 jsr @jump_id.l
 cmp.w D0,D2
 beq.w @dispatch_idle
 .hex 46df
 .hex 4cdf7fff
 jsr @native_dispatch.l
 .hex 48e7fffe
 .hex 40e7
 jsr @slots.l
 jsr @recover_air_cast.l
 jsr @physics.l
 .hex 46df
 .hex 4cdf7fff
 rts
dispatch_background:
 move.w #0x0010,(0x06,A0)
 .hex 46df
 .hex 4cdf7fff
 rts
dispatch_idle:
 tst.w (0x24,A0)
 beq.w @dispatch_native
 jsr @jump_id.l
 move.w D0,(A0)
 move.b #0x04,(0x5b,A0)
 move.b #0x0b,(0x04,A0)
 cmpi.w #0x0190,(0x10,A0)
 bcs.w @dispatch_fall_pose_ready
 move.b #0x08,(0x04,A0)
dispatch_fall_pose_ready:
 move.w #0x0010,(0x06,A0)
 jsr @physics.l
 move.b (A2),D0
 cmpi.b #0x03,D0
 beq.w @dispatch_air_pending
 cmpi.b #0x80,D0
 beq.w @dispatch_air_pending
 .hex 46df
 .hex 4cdf7fff
 rts
dispatch_air_pending:
 tst.b (0x14,A2)
 beq.w @dispatch_no_pending
 cmpi.b #0x19,(0x13,A2)
 beq.w @dispatch_no_pending
 move.b (0x12,A2),D0
 or.b D0,(0x1b,A0)
 or.b D0,(0x1d,A0)
 move.b (0x13,A2),(0xb9,A0)
 clr.b (0x14,A2)
dispatch_no_pending:
 .hex 46df
 .hex 4cdf7fff
 ; Mismos lectores de tecnica y normal aereo que el salto original.
 jsr 0x00021074.l
 jsr @normal_air_input.l
 rts
normal_air_input:
 .hex 48e7fffe
 .hex 40e7
 jsr @slots.l
 cmpi.b #0x03,(A2)
 bne.w @normal_air_allowed
 cmpi.b #0x02,(0x02,A2)
 bcs.w @normal_air_allowed
 .hex 46df
 .hex 4cdf7fff
 rts
normal_air_allowed:
 .hex 46df
 .hex 4cdf7fff
 jmp 0x00021672.l

; Tras la salida real del proyectil se conserva una breve pose de disparo,
; y se recupera el descenso. Solo en la persecucion: no cancela la carga,
; no recorta un Meteor ni cambia la recuperacion de especiales en suelo.
recover_air_cast:
 cmpi.b #0x03,(A2)
 bne.w @recover_cast_done
 tst.w (0x24,A0)
 beq.w @recover_cast_done
 cmpi.b #0x39,(0x5b,A0)
 bne.w @recover_cast_done
 move.w (A0),D0
 cmpi.w #0x0c04,D0
 beq.w @recover_kame
 cmpi.w #0x0c05,D0
 beq.w @recover_super
 cmpi.w #0x0c27,D0
 bne.w @recover_cast_done
 cmpi.b #0x53,(0x04,A0)
 bne.w @recover_cast_done
 cmpi.w #0x004b,(0x06,A0)
 bcs.w @recover_cast_done
 bra.w @recover_cast_jump
recover_kame:
 cmpi.b #0x4d,(0x04,A0)
 bne.w @recover_cast_done
 cmpi.w #0x001b,(0x06,A0)
 bcs.w @recover_cast_done
 bra.w @recover_cast_jump
recover_super:
 cmpi.b #0x4d,(0x04,A0)
 bne.w @recover_cast_done
 cmpi.w #0x007f,(0x06,A0)
 bcs.w @recover_cast_done
recover_cast_jump:
 jsr 0x00020ba0.l
 jsr @jump_id.l
 move.w D0,(A0)
 move.w #0x0010,(0x06,A0)
 move.b #0x04,(0x5b,A0)
 move.b #0x0b,(0x04,A0)
 jsr @slots.l
recover_cast_done:
 rts
dispatch_native:
 clr.b (A2)
 .hex 46df
 .hex 4cdf7fff
 jmp @native_dispatch.l
dispatch_custom:
 tst.w (0x24,A0)
 beq.w @dash_abort
 cmpi.b #0x04,(0x5b,A0)
 bne.w @dash_abort
 cmpi.b #0x17,(0x5b,A1)
 bne.w @dash_abort
 jsr @dash.l
 .hex 46df
 .hex 4cdf7fff
 rts
dash_abort:
 cmpi.b #0x81,(A3)
 bne.w @dash_abort_clear
 clr.b (A3)
dash_abort_clear:
 move.b #0x80,(A2)
 move.l (0x10,A0),(0x08,A2)
 move.w #0x0200,(0x0c,A2)
 move.w #0x0040,(0x04,A2)
 .hex 46df
 .hex 4cdf7fff
 jmp @native_dispatch.l
native_dispatch:
 lea (0x00019bce).l,A1
 move.w (A0),D0
 jmp 0x00013026.l

dash:
 move.w (0xffffe6a8).w,D0
 cmp.w (0x06,A2),D0
 beq.w @dash_return
 move.w D0,(0x06,A2)
 move.b #0x08,(0x04,A0)
 clr.w D3
 move.b (0x11,A2),D3
 beq.w @catch
 move.w (0x0a,A1),D0
 move.b (0x16,A2),(0x59,A0)
 tst.b (0x16,A2)
 beq.w @dash_target_left
 addi.w #0x0018,D0
 bra.w @dash_target_side
dash_target_left:
 subi.w #0x0018,D0
dash_target_side:
 cmpi.w #0x0030,D0
 bcc.w @dash_target
 move.w #0x0030,D0
dash_target:
 cmp.w (0xffffe722).w,D0
 bls.w @dash_x_ready
 move.w (0xffffe722).w,D0
dash_x_ready:
 sub.w (0x0a,A0),D0
 ext.l D0
 divs.w D3w,D0
 add.w D0,(0x0a,A0)
 clr.w (0x0c,A0)
 move.w (0x10,A1),D0
 sub.w (0x10,A0),D0
 ext.l D0
 divs.w D3w,D0
 add.w D0,(0x10,A0)
 clr.w (0x12,A0)
 subq.b #0x01,(0x11,A2)
 bne.w @dash_return
catch:
 move.b (0x16,A2),D0
 move.b D0,(0x59,A0)
 eori.b #0x01,D0
 move.b D0,(0x59,A1)
 ; Liquidar una sola vez el daño nativo del agarre al interceptarlo.
 move.l A0,-(SP)
 move.l A1,-(SP)
 movea.l A1,A0
 clr.w D0
 jsr 0x003dc040.l
 jsr 0x00020ba0.l
 move.w #0x002f,(A0)
 move.b #0x0c,(0x5b,A0)
 move.b #0x02,(0x04,A0)
 jsr 0x003e1256.l
 movea.l (SP)+,A1
 movea.l (SP)+,A0
 jsr @slots.l
 move.l (0x6c,A1),(0x20,A3)
 move.l (0x70,A1),(0x24,A3)
 move.b #0x01,(0x28,A3)
 move.b #0x80,(A3)
 move.b #0x03,(A2)
 move.w #0x0060,(0x04,A2)
 move.w #0x0060,(0x04,A3)
 clr.w (0x0c,A2)
 clr.w (0x0c,A3)
 move.l (0x10,A0),(0x08,A2)
 move.l (0x10,A1),(0x08,A3)
 move.w #0xffff,(0x06,A3)
 move.w (0x24,A1),(0x0e,A2)
 clr.w (0x02,A2)
 jsr @jump_id.l
 move.w D0,(A0)
 clr.w (0x06,A0)
 move.b #0x04,(0x5b,A0)
dash_return:
 rts
physics:
 move.b (A2),D0
 cmpi.b #0x03,D0
 beq.w @physics_tick
 cmpi.b #0x80,D0
 bne.w @physics_return
physics_tick:
 move.w (0xffffe6a8).w,D0
 cmp.w (0x06,A2),D0
 beq.w @physics_return
 move.w D0,(0x06,A2)
 tst.w (0x04,A2)
 beq.w @fall_fast
 subq.w #0x01,(0x04,A2)
 bra.w @gravity
fall_fast:
 move.w #0x0400,(0x0c,A2)
gravity:
 addi.w #0x0028,(0x0c,A2)
 move.w (0x0c,A2),D0
 ext.l D0
 lsl.l #0x08,D0
 add.l D0,(0x08,A2)
 move.l (0x08,A2),(0x10,A0)
 cmpi.w #0x01c0,(0x10,A0)
 bcs.w @physics_return
 move.l #0x01c00000,(0x10,A0)
 cmpi.b #0x03,(A2)
 bne.w @land_no_meteor
 cmpi.b #0x19,(0x13,A2)
 bne.w @land_no_meteor
 tst.b (0x14,A2)
 beq.w @land_no_meteor
 move.b #0x04,(A2)
 bra.w @land_cleanup
land_no_meteor:
 clr.b (A2)
land_cleanup:
 clr.w (0x08,A0)
 tst.w (0x24,A0)
 beq.w @physics_return
 cmpi.w #0x0400,(A0)
 bcc.w @physics_return
 jsr 0x00020ba0.l
 clr.w (A0)
 clr.b (0x5b,A0)
physics_return:
 rts

boxes:
 jsr 0x003e1148.l
 .hex 48e7fffe
 .hex 40e7
 cmpa.l #0xffffe75e,A0
 beq.w @boxes_player
 cmpa.l #0xffffe886,A0
 bne.w @boxes_done
boxes_player:
 jsr @slots.l
 tst.w (0x24,A0)
 beq.w @boxes_done
 cmpi.b #0x80,(A2)
 bne.w @boxes_done
 tst.b (0x28,A2)
 beq.w @boxes_done
 move.b (0x5b,A0),D0
 cmpi.b #0x0b,D0
 beq.w @boxes_apply
 cmpi.b #0x0c,D0
 bne.w @boxes_done
boxes_apply:
 move.l (0x20,A2),(0x6c,A0)
 move.l (0x24,A2),(0x70,A0)
boxes_done:
 .hex 46df
 .hex 4cdf7fff
 rts

damage_p1:
 cmpi.b #0x03,(0xfffff800).w
 bne.w @damage_original_p1
 tst.b (0xfffff803).w
 bne.w @damage_original_p1
 cmpi.b #0x02,(0xfffff802).w
 bcc.w @damage_original_p1
 cmpi.b #0x28,(0xffffe7b9).w
 beq.w @damage_allow
 cmpi.b #0x29,(0xffffe7b9).w
 beq.w @damage_allow
damage_original_p1:
 jmp 0x003d038e.l
damage_p2:
 cmpi.b #0x03,(0xfffff840).w
 bne.w @damage_original_p2
 tst.b (0xfffff843).w
 bne.w @damage_original_p2
 cmpi.b #0x02,(0xfffff842).w
 bcc.w @damage_original_p2
 cmpi.b #0x28,(0xffffe8e1).w
 beq.w @damage_allow
 cmpi.b #0x29,(0xffffe8e1).w
 beq.w @damage_allow
damage_original_p2:
 jmp 0x003d039a.l
damage_allow:
 .hex 003c0004
 rts

; Retener solo un comando reconocido por el lector existente. El combate
; consume B9 en la misma actualizacion, antes del asistente de cancels.
matcher:
 cmpa.l #0xffffe75e,A0
 beq.w @matcher_owner_p1
 cmpa.l #0xffffe886,A0
 bne.w @matcher_original
 cmpi.b #0x03,(0xfffff840).w
 beq.w @matcher_active
 cmpi.b #0x04,(0xfffff840).w
 beq.w @matcher_active
 bra.w @matcher_original
matcher_owner_p1:
 cmpi.b #0x03,(0xfffff800).w
 beq.w @matcher_active
 cmpi.b #0x04,(0xfffff800).w
 beq.w @matcher_active
matcher_original:
 jmp 0x003de0e2.l
matcher_active:
 jsr 0x003de0e2.l
 .hex 48e7fffe
 .hex 40e7
 jsr @slots.l
 cmpi.b #0x04,(A2)
 beq.w @matcher_landing
 cmpi.b #0x03,(A2)
 bne.w @matcher_done
 tst.b (0x02,A2)
 beq.w @matcher_done
 tst.b (0x10,A2)
 beq.w @matcher_done
 move.b (0xb9,A0),D0
 cmpi.b #0x19,D0
 beq.w @queue_finisher
 cmpi.b #0x06,D0
 beq.w @queue_finisher
 tst.b (0x58,A0)
 bne.w @matcher_done
 cmpi.b #0x05,D0
 bne.w @matcher_done
queue_finisher:
 move.b D0,(0x13,A2)
 clr.b (0x12,A2)
 move.b #0x08,(0x14,A2)
 cmpi.b #0x19,D0
 bne.w @queue_cancel_check
 move.b #0x30,(0x14,A2)
 bra.w @matcher_done
queue_cancel_check:
 move.b (0x5b,A0),D1
 cmpi.b #0x28,D1
 beq.w @queue_cancel
 cmpi.b #0x29,D1
 bne.w @matcher_done
queue_cancel:
 jsr 0x00020ba0.l
 jsr @jump_id.l
 move.w D0,(A0)
 move.w #0x0010,(0x06,A0)
 move.b #0x04,(0x5b,A0)
 bra.w @matcher_done
matcher_landing:
 tst.b (0x14,A2)
 beq.w @matcher_done
 cmpi.b #0x08,(0x5b,A0)
 bhi.w @matcher_done
 tst.w (0x24,A1)
 beq.w @matcher_done
 cmpi.w #0x01c0,(0x10,A0)
 bne.w @matcher_done
 cmpi.w #0x01c0,(0x10,A1)
 bne.w @matcher_done
 move.b (0x13,A2),(0xb9,A0)
 clr.b (A2)
 clr.b (0x14,A2)
matcher_done:
 .hex 46df
 .hex 4cdf7fff
 rts

; Condicion3: permitir los remates seleccionados en el aire SOLO durante
; una persecucion confirmada. Las demas tecnicas conservan la prueba nativa.
ground_gate:
 .hex 48e7fffe
 .hex 40e7
 movea.l A2,A4
 jsr @slots.l
 cmpi.b #0x03,(A2)
 bne.w @ground_original
 tst.b (0x02,A2)
 beq.w @ground_original
 move.w (0x02,A4),D0
 cmpi.w #0x0c04,D0
 beq.w @ground_allowed
 cmpi.w #0x0c05,D0
 beq.w @ground_allowed
 cmpi.w #0x0c27,D0
 beq.w @ground_allowed
ground_original:
 .hex 46df
 .hex 4cdf7fff
 move.w #0x01c0,D0
 btst.b #0x04,(0x1e,A0)
 jmp 0x00021224.l
ground_allowed:
 .hex 46df
 .hex 4cdf7fff
 .hex 003c0008
 rts

round_reset:
 .hex 48e7fffe
 .hex 40e7
 lea (0xfffff800).w,A1
 moveq #0x1f,D0
reset_loop:
 clr.l (A1)+
 subq.w #0x01,D0
 bpl.w @reset_loop
 .hex 46df
 .hex 4cdf7fff
 jmp 0x003e128e.l



