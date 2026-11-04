; COPIA DIDÁCTICA ANOTADA EN CASTELLANO
; Nuevo comando humano FBF+C; reutiliza el movimiento nativo sin golpe.
; Las instrucciones/directivas conservan la fuente del parche.
; Los comentarios de operación no prueban por sí solos el significado del juego.


; Entrada del gancho; conserva registros y vuelve a la ruta nativa.
entry:
 .hex 48e7fffe ; Guarda los registros del llamador.
 .hex 40e7 ; Guarda el registro de estado en la pila.
 tst.b (0xffffe742).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @done ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xffffe744).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @done ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xffffe9b0).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @done ; Bifurcación según la condición indicada por el mnemónico.
 tst.b (0xffffe73c).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @done ; Bifurcación según la condición indicada por el mnemónico.
 tst.w (0xffffe9c4).w ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @done ; Bifurcación según la condición indicada por el mnemónico.
 lea (0xffffe75e).w,A0 ; Calcula una dirección y la deja en un registro de direcciones.
 jsr @actor.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 lea (0xffffe886).w,A0 ; Calcula una dirección y la deja en un registro de direcciones.
 jsr @actor.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
done:
 .hex 46df ; Restaura el registro de estado desde la pila.
 .hex 4cdf7fff ; Restaura los registros guardados.
 jmp 0x00011c9c.l ; Salta a otra dirección sin apilar un retorno nuevo.

; Comprueba condiciones del comando nuevo para un actor humano.
actor:
 tst.b (0xbe,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0x108,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.b #0xf7,D0 ; Operación lógica o máscara de bits.
 cmpi.b #0xc7,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 btst.b #0x3,(0x108,A0) ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @consume ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xbc,A0),D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x1b,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 btst.l D4,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 beq.w @released ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0x1d,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 btst.l D4,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 beq.w @return ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D5 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xba,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D1,D5 ; Establece el bit indicado.
 move.b (0xbb,A0),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D1,D5 ; Establece el bit indicado.
 and.b (0x1b,A0),D5 ; Operación lógica o máscara de bits.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0xff,(0xb9,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0x08,(0x5b,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @return ; Bifurcación según la condición indicada por el mnemónico.
 tst.w (0x24,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @return ; Bifurcación según la condición indicada por el mnemónico.
 jsr 0x0001335c.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 tst.w (0x24,A1) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 beq.w @return ; Bifurcación según la condición indicada por el mnemónico.
 move.b (0x1e,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x1e,A1),D1 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 eor.b D1,D0 ; Operación lógica o máscara de bits.
 btst.l #0x4,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 move.w (0xa,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0xa,A1),D0 ; Operación aritmética de suma o resta sobre los operandos.
 bpl.w @positive_x ; Bifurcación según la condición indicada por el mnemónico.
 neg.w D0 ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
positive_x:
 cmpi.w #0x60,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @return ; Bifurcación según la condición indicada por el mnemónico.
 move.w (0x10,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 sub.w (0x10,A1),D0 ; Operación aritmética de suma o resta sobre los operandos.
 bpl.w @positive_y ; Bifurcación según la condición indicada por el mnemónico.
 neg.w D0 ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
positive_y:
 cmpi.w #0x20,D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bhi.w @return ; Bifurcación según la condición indicada por el mnemónico.
 lea (0x94,A0),A3 ; Calcula una dirección y la deja en un registro de direcciones.
 moveq #0x13,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.

; Guarda temporalmente el historial para no modificarlo si el comando falla.
save_history:
 move.w (A3)+,-(SP) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 subq.w #0x1,D6 ; Operación aritmética de suma o resta sobre los operandos.
 bpl.w @save_history ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D4,D0 ; Establece el bit indicado.
 not.b D0 ; Operación lógica o máscara de bits.
 lea (0x94,A0),A3 ; Calcula una dirección y la deja en un registro de direcciones.
 moveq #0x0f,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
strip_flight_from_history:
 and.b D0,(A3) ; Operación lógica o máscara de bits.
 addq.w #0x2,A3 ; Operación aritmética de suma o resta sobre los operandos.
 subq.w #0x1,D6 ; Operación aritmética de suma o resta sobre los operandos.
 bpl.w @strip_flight_from_history ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xb6,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 andi.w #0x1f,D0 ; Operación lógica o máscara de bits.
 lea (0x94,A0),A3 ; Calcula una dirección y la deja en un registro de direcciones.
 adda.w D0,A3 ; Operación aritmética de suma o resta sobre los operandos.
 clr.w (A3) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 addq.w #0x2,D0 ; Operación aritmética de suma o resta sobre los operandos.
 andi.w #0x1f,D0 ; Operación lógica o máscara de bits.
 move.b D0,(0xb6,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 cmp.b (0xb7,A0),D0 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @virtual_entry_ready ; Bifurcación según la condición indicada por el mnemónico.
 addq.w #0x2,D0 ; Operación aritmética de suma o resta sobre los operandos.
 andi.w #0x1f,D0 ; Operación lógica o máscara de bits.
 move.b D0,(0xb7,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
virtual_entry_ready:
 move.b #0xff,(0xb9,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 lea (@sequence).l,A1 ; Calcula una dirección y la deja en un registro de direcciones.
 jsr 0x000092b2.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 moveq #0,D7 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xb9,A0),D7 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 lea (0xbc,A0),A3 ; Calcula una dirección y la deja en un registro de direcciones.
 moveq #0x13,D6 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.

; Restaura el historial original tras consultar el reconocedor nativo.
restore_history:
 move.w (SP)+,-(A3) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 subq.w #0x1,D6 ; Operación aritmética de suma o resta sobre los operandos.
 bpl.w @restore_history ; Bifurcación según la condición indicada por el mnemónico.
 cmpi.b #0xfe,D7 ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 move.b #0x3a,(0x7c,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 clr.w (0xe0,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 move.b #0x38,(0x5b,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.w #0x20,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 jsr 0x0001318a.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 jsr 0x00020ba0.l ; Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
 move.w #0x0843,(A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xb6,A0),(0xb7,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b #0xff,(0xb9,A0) ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 clr.b (0x109,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.b (0x10a,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 clr.b (0x10e,A0) ; Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
 bset.b #0x3,(0x108,A0) ; Establece el bit indicado.

; Enmascara el botón de vuelo en los campos de entrada del actor.
consume:
 moveq #0,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xbc,A0),D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 bset.l D4,D0 ; Establece el bit indicado.
 not.b D0 ; Operación lógica o máscara de bits.
 and.b D0,(0x1a,A0) ; Operación lógica o máscara de bits.
 and.b D0,(0x1b,A0) ; Operación lógica o máscara de bits.
 and.b D0,(0x1c,A0) ; Operación lógica o máscara de bits.
 and.b D0,(0x1d,A0) ; Operación lógica o máscara de bits.
return:
 rts ; Regresa usando la dirección de retorno de la pila.
released:
 bclr.b #0x3,(0x108,A0) ; Borra el bit indicado.
 rts ; Regresa usando la dirección de retorno de la pila.

; Consume C mientras está retenida la maniobra, antes del historial nativo.
pre_input:
 cmpi.b #0xcf,(0x108,A0) ; Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
 bne.w @return ; Bifurcación según la condición indicada por el mnemónico.
 moveq #0,D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0xbc,A0),D4 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 moveq #0,D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 move.b (0x1b,A0),D0 ; Transfiere valores entre los operandos; el sufijo indica el tamaño.
 btst.l D4,D0 ; Comprueba el bit indicado y actualiza la condición de cero.
 beq.w @released ; Bifurcación según la condición indicada por el mnemónico.
 bra.w @consume ; Bifurcación según la condición indicada por el mnemónico.
sequence:
 .hex 0308040800fe00 ; Bytes literales. Pueden ser código o tablas: no se traducen automáticamente a instrucciones.
