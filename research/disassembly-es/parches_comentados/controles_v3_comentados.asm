; COPIA DIDÁCTICA ANOTADA EN CASTELLANO
; Controles propios: cola de pulsaciones, recuperación y transición visual.
; Las instrucciones/directivas conservan la fuente del parche.
; Los comentarios de operación no prueban por sí solos el significado del juego.

input_entry:
 tst.b (0xffffe744).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @input_body ; Bifurcación según la condición indicada por el mnemónico.
 jsr 0x00009066.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 bcs.w @input_blocked ; Bifurcación según la condición indicada por el mnemónico.
input_body:
 jsr 0x00008f68.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 .hex 48e7fffe ; Guarda los registros del llamador.
 .hex 40e7 ; Guarda el registro de estado en la pila.
 tst.b (0xffffe744).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @input_done ; Bifurcación según la condición indicada por el mnemónico.
 lea (0xffffe75e).w,A0 ; Calcula una dirección y la deja en un registro de direcciones.
 jsr @actor_input.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 lea (0xffffe886).w,A0 ; Calcula una dirección y la deja en un registro de direcciones.
 jsr @actor_input.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
input_done:
 .hex 46df ; Restaura el registro de estado desde la pila.
 .hex 4cdf7fff ; Restaura los registros guardados.
 rts ; Regresa usando la dirección de retorno de la pila.
input_blocked:
 jmp 0x00009054.l ; Salta a otra dirección sin apilar un retorno nuevo.

; Entrada por actor: control humano, cola de pulsaciones y acción previa.
actor_input:
 tst.b (0xbe,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @actor_cpu ; Bifurcación según la condición indicada por el mnemónico.
 jsr 0x003e01f4.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 move.b (0x108,A0),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.b #0xf7,D6 ; Operación lógica o máscara de bits.
 cmpi.b #0xc7,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_initialized ; Bifurcación según la condición indicada por el mnemónico.
 clr.l (0x108,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.l (0x10c,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 move.b #0xc7,(0x108,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
actor_initialized:
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x5b,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x10b,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmp.b D1,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
 clr.b (0x10c,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 move.b D0,(0x10b,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 tst.b D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @actor_new_nonidle ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x20,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x27,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
 btst.b #0x4,(0x1e,A0) ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0x4,A0),(0x10f,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b #0x02,(0x10e,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bra.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
actor_new_nonidle:
 clr.b (0x10e,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 cmpi.b #0x20,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @clear_queue_new_action ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x27,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bls.w @actor_same_action ; Bifurcación según la condición indicada por el mnemónico.
clear_queue_new_action:
 clr.b (0x109,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.b (0x10a,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
actor_same_action:
 tst.b (0x109,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_queue_aged ; Bifurcación según la condición indicada por el mnemónico.
 subq.b #0x1,(0x109,A0) ; Operación aritmética de suma o resta sobre los operandos.
 bne.w @actor_queue_aged ; Bifurcación según la condición indicada por el mnemónico.
 clr.b (0x10a,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
actor_queue_aged:
 tst.b D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @actor_not_idle ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0x109,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0x10a,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 or.b D1,(0x1a,A0) ; Operación lógica o máscara de bits.
 or.b D1,(0x1b,A0) ; Operación lógica o máscara de bits.
 or.b D1,(0x1c,A0) ; Operación lógica o máscara de bits.
 or.b D1,(0x1d,A0) ; Operación lógica o máscara de bits.
 clr.b (0x109,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.b (0x10a,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 rts ; Regresa usando la dirección de retorno de la pila.
actor_not_idle:
 cmpi.b #0x1,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_walking ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x2,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @actor_walking ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x20,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x27,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 btst.b #0x4,(0x1e,A0) ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xba,A0),D2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D2,D1 ; Establece el bit indicado.
 move.b (0xbb,A0),D2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D2,D1 ; Establece el bit indicado.
 move.b (0x1d,A0),D2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 and.b D1,D2 ; Operación lógica o máscara de bits.
 beq.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 move.b D2,D3 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 subq.b #0x1,D3 ; Operación aritmética de suma o resta sobre los operandos.
 and.b D2,D3 ; Operación lógica o máscara de bits.
 bne.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 move.b D2,(0x10a,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b #0x06,(0x109,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
actor_return:
 rts ; Regresa usando la dirección de retorno de la pila.
actor_cpu:
 move.b (0x108,A0),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.b #0xf7,D6 ; Operación lógica o máscara de bits.
 cmpi.b #0xc7,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @actor_return ; Bifurcación según la condición indicada por el mnemónico.
 clr.l (0x108,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.l (0x10c,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 rts ; Regresa usando la dirección de retorno de la pila.
actor_walking:
 rts ; Regresa usando la dirección de retorno de la pila.
animation_entry:
 .hex 48e70060 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 jsr 0x00020a4c.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 .hex 48e7fffe ; Guarda los registros del llamador.
 .hex 40e7 ; Guarda el registro de estado en la pila.
 jsr @animation_recovery.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 .hex 46df ; Restaura el registro de estado desde la pila.
 .hex 4cdf7fff ; Restaura los registros guardados.
 jmp 0x000209e4.l ; Salta a otra dirección sin apilar un retorno nuevo.

; Recorte de la recuperación final de golpes básicos en las condiciones admitidas.
animation_recovery:
 cmpa.l #0xffffe75e,A0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @animation_actor_valid ; Bifurcación según la condición indicada por el mnemónico.
 cmpa.l #0xffffe886,A0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
animation_actor_valid:
 move.b (0x108,A0),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.b #0xf7,D6 ; Operación lógica o máscara de bits.
 cmpi.b #0xc7,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xbe,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 move.w D1,D7 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 mulu.w D2w,D7 ; Multiplicación o división; el mnemónico distingue signo y tamaño.
 move.b (0x5b,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.b #0x20,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @animation_clear_remaining ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x27,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @animation_clear_remaining ; Bifurcación según la condición indicada por el mnemónico.
 btst.b #0x4,(0x1e,A0) ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @animation_clear_remaining ; Bifurcación según la condición indicada por el mnemónico.
 move.w D7,D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0x6,A0),D1 ; Operación aritmética de suma o resta sobre los operandos.
 bls.w @animation_clear_remaining ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0xff,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @animation_clear_remaining ; Bifurcación según la condición indicada por el mnemónico.
 move.b D1,(0x10d,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x03,D1 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0x10c,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 tst.w (0x6,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 movea.l A1,A3 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
animation_scan_phase:
 move.b (A3)+,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 beq.w @animation_last_phase ; Bifurcación según la condición indicada por el mnemónico.
 bmi.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 addq.w #0x1,D4 ; Operación aritmética de suma o resta sobre los operandos.
 cmpi.w #0x08,D4 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 bra.w @animation_scan_phase ; Bifurcación según la condición indicada por el mnemónico.
animation_last_phase:
 cmpi.w #0x02,D4 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 subq.w #0x1,D4 ; Operación aritmética de suma o resta sobre los operandos.
 adda.w D4,A2 ; Operación aritmética de suma o resta sobre los operandos.
 move.b (A2),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmp.b (0x4,A0),D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @animation_return ; Bifurcación según la condición indicada por el mnemónico.
 addq.w #0x2,(0x6,A0) ; Operación aritmética de suma o resta sobre los operandos.
 move.b #0x1,(0x10c,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b #0x1,(0x10d,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
animation_return:
 rts ; Regresa usando la dirección de retorno de la pila.
animation_clear_remaining:
 clr.b (0x10d,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 rts ; Regresa usando la dirección de retorno de la pila.
animation_exit:
 .hex 4cdf0600 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 48e7fbfe ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 40e7 ; Guarda el registro de estado en la pila.
 jsr @animation_settle.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 .hex 46df ; Restaura el registro de estado desde la pila.
 .hex 4cdf7fdf ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 rts ; Regresa usando la dirección de retorno de la pila.

; Transición visual final; otra acción cancela esta transición.
animation_settle:
 cmpa.l #0xffffe75e,A0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @settle_actor_valid ; Bifurcación según la condición indicada por el mnemónico.
 cmpa.l #0xffffe886,A0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @settle_return ; Bifurcación según la condición indicada por el mnemónico.
settle_actor_valid:
 move.b (0x108,A0),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.b #0xf7,D6 ; Operación lógica o máscara de bits.
 cmpi.b #0xc7,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @settle_return ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xbe,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @settle_cancel ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0x5b,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @settle_cancel ; Bifurcación según la condición indicada por el mnemónico.
 btst.b #0x4,(0x1e,A0) ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @settle_cancel ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0x10e,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @settle_return ; Bifurcación según la condición indicada por el mnemónico.
 subq.b #0x1,(0x10e,A0) ; Operación aritmética de suma o resta sobre los operandos.
 beq.w @settle_neutral_pose ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x10f,A0),D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 rts ; Regresa usando la dirección de retorno de la pila.
settle_neutral_pose:
 moveq #0x02,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
settle_return:
 rts ; Regresa usando la dirección de retorno de la pila.
settle_cancel:
 clr.b (0x10e,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 rts ; Regresa usando la dirección de retorno de la pila.
