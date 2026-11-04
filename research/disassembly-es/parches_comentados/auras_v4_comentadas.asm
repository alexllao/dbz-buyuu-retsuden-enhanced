; COPIA DIDÁCTICA ANOTADA EN CASTELLANO
; Código propio de auras v4; atlas por jugador, paleta y restauración tras efectos.
; Las instrucciones/directivas conservan la fuente del parche.
; Los comentarios de operación no prueban por sí solos el significado del juego.

aura_entry:
 tst.b (0xffffe874).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_resources_ready ; Bifurcación según la condición indicada por el mnemónico.
 tst.w (0xffffe9c4).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_skip_busy ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xffffe73c).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_skip_busy ; Bifurcación según la condición indicada por el mnemónico.
 jsr @aura_load_graphics.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
aura_resources_ready:
 cmpi.b #0xc2,(0x110,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_initialized ; Bifurcación según la condición indicada por el mnemónico.
 move.b #0xc2,(0x110,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 clr.b (0x111,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 move.w (0xffffe6a8).w,(0x112,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.w (0x24,A0),(0x114,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_initialized:
 move.w (0x24,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmp.w (0x114,A0),D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @aura_hit_cancel ; Bifurcación según la condición indicada por el mnemónico.
 move.w D0,(0x114,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.w (0xffffe6a8).w,D2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.w D2,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0x112,A0),D4 ; Operación aritmética de suma o resta sobre los operandos.
 move.w D2,(0x112,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x10,D4 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @aura_elapsed_valid ; Bifurcación según la condición indicada por el mnemónico.
 clr.b (0x111,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 moveq #0,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_elapsed_valid:
 tst.b (0xbd,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_inactive ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x0f,(0x5b,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_sustain ; Bifurcación según la condición indicada por el mnemónico.
 move.w (0x1a,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xba,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 btst.l D1,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 beq.w @aura_release ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0xbb,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 btst.l D1,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 beq.w @aura_release ; Bifurcación según la condición indicada por el mnemónico.
aura_sustain:
 move.b #0x80,(0x111,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bra.w @aura_draw ; Bifurcación según la condición indicada por el mnemónico.
aura_inactive:
 move.b (0x5b,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 beq.w @aura_release ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x0f,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_cancel ; Bifurcación según la condición indicada por el mnemónico.
aura_release:
 cmpi.b #0x80,(0x111,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_countdown ; Bifurcación según la condición indicada por el mnemónico.
 move.b #0x0c,(0x111,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bra.w @aura_draw ; Bifurcación según la condición indicada por el mnemónico.
aura_countdown:
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x111,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 beq.w @aura_return ; Bifurcación según la condición indicada por el mnemónico.
 sub.w D4,D0 ; Operación aritmética de suma o resta sobre los operandos.
 ble.w @aura_cancel ; Bifurcación según la condición indicada por el mnemónico.
 move.b D0,(0x111,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x0a,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcc.w @aura_draw ; Bifurcación según la condición indicada por el mnemónico.
 moveq #1,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x07,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcc.w @aura_draw ; Bifurcación según la condición indicada por el mnemónico.
 moveq #2,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x04,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcc.w @aura_draw ; Bifurcación según la condición indicada por el mnemónico.
 moveq #3,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_draw:
 tst.w D5 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_density_keep ; Bifurcación según la condición indicada por el mnemónico.
 move.w (0xffffe6a8).w,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 lsr.w #0x1,D6 ; Desplaza o rota bits según la operación indicada.
 andi.w #0x0003,D6 ; Operación lógica o máscara de bits.
 cmpi.w #0x0001,D5 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_density_three_quarters ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0x0002,D5 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_density_half ; Bifurcación según la condición indicada por el mnemónico.
 tst.w D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_return ; Bifurcación según la condición indicada por el mnemónico.
 bra.w @aura_density_keep ; Bifurcación según la condición indicada por el mnemónico.
aura_density_three_quarters:
 cmpi.w #0x0003,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_return ; Bifurcación según la condición indicada por el mnemónico.
 bra.w @aura_density_keep ; Bifurcación según la condición indicada por el mnemónico.
aura_density_half:
 andi.w #0x0001,D6 ; Operación lógica o máscara de bits.
 bne.w @aura_return ; Bifurcación según la condición indicada por el mnemónico.
aura_density_keep:
 lsl.w #0x2,D5 ; Desplaza o rota bits según la operación indicada.
aura_animation:
 moveq #0,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.w (0xffffe6a8).w,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 divu.w #0x0006,D6 ; Multiplicación o división; el mnemónico distingue signo y tamaño.
 andi.l #0x0000ffff,D6 ; Operación lógica o máscara de bits.
 divu.w #0x0018,D6 ; Multiplicación o división; el mnemónico distingue signo y tamaño.
 swap D6 ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 lsl.w #0x4,D6 ; Desplaza o rota bits según la operación indicada.
 add.w D6,D5 ; Operación aritmética de suma o resta sobre los operandos.
 cmpi.w #0x01c0,(0x10,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_ground_map ; Bifurcación según la condición indicada por el mnemónico.
 addi.w #0x0180,D5 ; Operación aritmética de suma o resta sobre los operandos.
aura_ground_map:
 moveq #0,D7 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpa.w #0xe886,A0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_player_ready ; Bifurcación según la condición indicada por el mnemónico.
 move.w #0x0600,D7 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_player_ready:
 moveq #0,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x58,A0),D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x02,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_actor_palette ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0x06,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_actor_palette ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0x08,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_actor_palette ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0x09,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @aura_actor_palette ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.w #0x0a,D6 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_palette_ready ; Bifurcación según la condición indicada por el mnemónico.
aura_actor_palette:
 addi.w #0x0300,D7 ; Operación aritmética de suma o resta sobre los operandos.
aura_palette_ready:
 add.w D7,D5 ; Operación aritmética de suma o resta sobre los operandos.
 move.w (0x0a,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0x16,A0),D0 ; Operación aritmética de suma o resta sobre los operandos.
 move.w (0x10,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0x18,A0),D1 ; Operación aritmética de suma o resta sobre los operandos.
 addi.w #0x20,D1 ; Operación aritmética de suma o resta sobre los operandos.
 lea (@aura_map_table).l,A1 ; Calcula una dirección y la deja en un registro de direcciones.
 adda.w D5,A1 ; Operación aritmética de suma o resta sobre los operandos.
 movea.l (A1),A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x00001c66.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 bra.w @aura_return ; Bifurcación según la condición indicada por el mnemónico.
aura_hit_cancel:
 move.w D0,(0x114,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_cancel:
 clr.b (0x111,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
aura_return:
 jmp 0x00009f08.l ; Salta a otra dirección sin apilar un retorno nuevo.
aura_skip_busy:
 clr.b (0x111,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 jmp 0x00009f08.l ; Salta a otra dirección sin apilar un retorno nuevo.
aura_load_graphics:
 .hex 48e7fffe ; Guarda los registros del llamador.
 tst.w (0xffffe9c4).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_loader_defer ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xffffe73c).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_loader_defer ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xffffe7b6).w,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x0b,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @aura_loader_p1_valid ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_loader_p1_valid:
 lsl.w #0x3,D0 ; Desplaza o rota bits según la operación indicada.
 lea (0x00280000).l,A2 ; Calcula una dirección y la deja en un registro de direcciones.
 adda.w D0,A2 ; Operación aritmética de suma o resta sobre los operandos.
 movea.l (A2)+,A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.w #0xa260,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.l A2,-(SP) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 movea.l (SP)+,A2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.l (A2),A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.w #0xa820,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xffffe8de).w,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmpi.w #0x0b,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bcs.w @aura_loader_p2_valid ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_loader_p2_valid:
 cmpi.w #0x09,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_loader_p2_normal ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x09,(0xffffe7b6).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @aura_loader_p2_normal ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0x0b,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_loader_p2_normal:
 mulu.w #0x000c,D0 ; Multiplicación o división; el mnemónico distingue signo y tamaño.
 lea (0x00280100).l,A2 ; Calcula una dirección y la deja en un registro de direcciones.
 adda.w D0,A2 ; Operación aritmética de suma o resta sobre los operandos.
 movea.l (A2)+,A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.w #0xa960,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.l A2,-(SP) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 movea.l (SP)+,A2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.l (A2)+,A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.w #0x5c00,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.l A2,-(SP) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 movea.l (SP)+,A2 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.l (A2),A0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 movea.w #0xae80,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 lea (0x00280300).l,A0 ; Calcula una dirección y la deja en un registro de direcciones.
 movea.w #0xaec0,A1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 clr.b (0xffffe874).w ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 bra.w @aura_loader_return ; Bifurcación según la condición indicada por el mnemónico.
aura_loader_defer:
 move.b #0x01,(0xffffe874).w ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
aura_loader_return:
 .hex 4cdf7fff ; Restaura los registros guardados.
 rts ; Regresa usando la dirección de retorno de la pila.
aura_native_effect_load:
 jsr 0x000015d2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 move.b #0x01,(0xffffe874).w ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 rts ; Regresa usando la dirección de retorno de la pila.
recoome_select_table:
 lea (0x00080000).l,A0 ; Calcula una dirección y la deja en un registro de direcciones.
  .hex 20704000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 cmpi.w #0x0024,D4 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @recoome_table_done ; Bifurcación según la condición indicada por el mnemónico.
 cmpa.w #0xe390,A4 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @recoome_table_normal ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x09,(0xffffe7b6).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @recoome_table_done ; Bifurcación según la condición indicada por el mnemónico.
recoome_table_normal:
 lea (0x00227314).l,A0 ; Calcula una dirección y la deja en un registro de direcciones.
recoome_table_done:
 rts ; Regresa usando la dirección de retorno de la pila.
aura_map_table:
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
 .hex 00000000000000000000000000000000 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
