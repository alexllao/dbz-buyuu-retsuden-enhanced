; EXTRACTOS NATIVOS AUDITADOS, COMENTADOS EN CASTELLANO
; No es todo el juego. Los tramos se delimitan por evidencia independiente.


; Lee las entradas de ambos jugadores y distingue control humano/CPU; incluye la ruta que bloquea entradas.
; Fuente: evidence/gameplay-v1 y research/gameplay-v2/gameplay_probe.py
        org $008F58
entrada_mandos:
        tst.b $e744.w                                    ; $008F58 [4a38e744] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $8f68                                      ; $008F5C [6600000a] Bifurcación según la condición indicada por el mnemónico.
        bsr.w $9066                                      ; $008F60 [61000104] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        bcs.w $9054                                      ; $008F64 [650000ee] Bifurcación según la condición indicada por el mnemónico.
        lea.l $e75e.w, a0                                ; $008F68 [41f8e75e] Calcula una dirección y la deja en un registro de direcciones.
        lea.l $e886.w, a1                                ; $008F6C [43f8e886] Calcula una dirección y la deja en un registro de direcciones.
        btst.b #$4, $20(a1)                              ; $008F70 [082900040020] Comprueba el bit indicado y actualiza la condición de cero.
        bne.b $8fd4                                      ; $008F76 [665c] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$2f, $e2(a0)                             ; $008F78 [0c28002f00e2] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $8fc8                                      ; $008F7E [67000048] Bifurcación según la condición indicada por el mnemónico.
        btst.b #$3, $20(a1)                              ; $008F82 [082900030020] Comprueba el bit indicado y actualiza la condición de cero.
        bne.w $8fc8                                      ; $008F88 [6600003e] Bifurcación según la condición indicada por el mnemónico.
        tst.w $24(a1)                                    ; $008F8C [4a690024] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $8fc8                                      ; $008F90 [6736] Bifurcación según la condición indicada por el mnemónico.
        tst.b $be(a0)                                    ; $008F92 [4a2800be] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $8fb8                                      ; $008F96 [6620] Bifurcación según la condición indicada por el mnemónico.
        move.b $e6bc.w, $1a(a0)                          ; $008F98 [1178e6bc001a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e666.w, $1b(a0)                          ; $008F9E [1178e666001b] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e6bd.w, $1c(a0)                          ; $008FA4 [1178e6bd001c] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e667.w, $1d(a0)                          ; $008FAA [1178e667001d] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e6b9.w, $8e(a0)                          ; $008FB0 [1178e6b9008e] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        bra.b $8fdc                                      ; $008FB6 [6024] Bifurcación según la condición indicada por el mnemónico.
        tst.b $e744.w                                    ; $008FB8 [4a38e744] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $8fdc                                      ; $008FBC [6600001e] Bifurcación según la condición indicada por el mnemónico.
        jsr $2b936.l                                     ; $008FC0 [4eb90002b936] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        bra.b $8fdc                                      ; $008FC6 [6014] Bifurcación según la condición indicada por el mnemónico.
        move.b #$ff, $b9(a0)                             ; $008FC8 [117c00ff00b9] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $b6(a0), $b7(a0)                          ; $008FCE [116800b600b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.w $1a(a0)                                    ; $008FD4 [4268001a] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $1c(a0)                                    ; $008FD8 [4268001c] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        lea.l $e886.w, a0                                ; $008FDC [41f8e886] Calcula una dirección y la deja en un registro de direcciones.
        lea.l $e75e.w, a1                                ; $008FE0 [43f8e75e] Calcula una dirección y la deja en un registro de direcciones.
        btst.b #$4, $20(a1)                              ; $008FE4 [082900040020] Comprueba el bit indicado y actualiza la condición de cero.
        bne.b $904a                                      ; $008FEA [665e] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$2f, $e2(a0)                             ; $008FEC [0c28002f00e2] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $903e                                      ; $008FF2 [6700004a] Bifurcación según la condición indicada por el mnemónico.
        btst.b #$3, $20(a1)                              ; $008FF6 [082900030020] Comprueba el bit indicado y actualiza la condición de cero.
        bne.w $903e                                      ; $008FFC [66000040] Bifurcación según la condición indicada por el mnemónico.
        tst.w $24(a1)                                    ; $009000 [4a690024] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $903e                                      ; $009004 [67000038] Bifurcación según la condición indicada por el mnemónico.
        tst.b $be(a0)                                    ; $009008 [4a2800be] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $902e                                      ; $00900C [6620] Bifurcación según la condición indicada por el mnemónico.
        move.b $e6e4.w, $1a(a0)                          ; $00900E [1178e6e4001a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e668.w, $1b(a0)                          ; $009014 [1178e668001b] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e6e5.w, $1c(a0)                          ; $00901A [1178e6e5001c] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e669.w, $1d(a0)                          ; $009020 [1178e669001d] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $e6e1.w, $8e(a0)                          ; $009026 [1178e6e1008e] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        bra.b $9064                                      ; $00902C [6036] Bifurcación según la condición indicada por el mnemónico.
        tst.b $e744.w                                    ; $00902E [4a38e744] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $9064                                      ; $009032 [66000030] Bifurcación según la condición indicada por el mnemónico.
        jsr $2b936.l                                     ; $009036 [4eb90002b936] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        bra.b $9064                                      ; $00903C [6026] Bifurcación según la condición indicada por el mnemónico.
        move.b #$ff, $b9(a0)                             ; $00903E [117c00ff00b9] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $b6(a0), $b7(a0)                          ; $009044 [116800b600b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.w $1a(a0)                                    ; $00904A [4268001a] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $1c(a0)                                    ; $00904E [4268001c] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        bra.b $9064                                      ; $009052 [6010] Bifurcación según la condición indicada por el mnemónico.
        clr.w $e778.w                                    ; $009054 [4278e778] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $e8a0.w                                    ; $009058 [4278e8a0] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $e77a.w                                    ; $00905C [4278e77a] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $e8a2.w                                    ; $009060 [4278e8a2] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        rts                                              ; $009064 [4e75] Regresa usando la dirección de retorno de la pila.

; Conserva direcciones, normaliza según orientación y resuelve combinaciones originales de A/B. El reconocedor nativo modifica B7 y B9, incluso al fallar.
; Fuente: evidence/side-switch/input-audit.json
        org $009170
historial_y_combinaciones:
        lea.l $e75e.w, a0                                ; $009170 [41f8e75e] Calcula una dirección y la deja en un registro de direcciones.
        bsr.w $917c                                      ; $009174 [61000006] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        lea.l $e886.w, a0                                ; $009178 [41f8e886] Calcula una dirección y la deja en un registro de direcciones.
        move.b $b6(a0), d0                               ; $00917C [102800b6] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.w #$1f, d0                                  ; $009180 [0240001f] Operación lógica o máscara de bits.
        move.b $b7(a0), d1                               ; $009184 [122800b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.w #$1f, d1                                  ; $009188 [0241001f] Operación lógica o máscara de bits.
        move.b $1b(a0), d2                               ; $00918C [1428001b] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        swap d3                                          ; $009190 [4843] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b $b5(a0), d3                               ; $009192 [162800b5] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        beq.b $919c                                      ; $009196 [6704] Bifurcación según la condición indicada por el mnemónico.
        bchg.b d3, d2                                    ; $009198 [0742] Invierte el bit indicado.
        swap d3                                          ; $00919A [4843] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        tst.b d2                                         ; $00919C [4a02] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $920e                                      ; $00919E [676e] Bifurcación según la condición indicada por el mnemónico.
        bsr.w $922a                                      ; $0091A0 [61000088] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        lea.l $94(a0), a1                                ; $0091A4 [43e80094] Calcula una dirección y la deja en un registro de direcciones.
        tst.b $b8(a0)                                    ; $0091A8 [4a2800b8] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $91ce                                      ; $0091AC [6620] Bifurcación según la condición indicada por el mnemónico.
        cmp.w d0, d1                                     ; $0091AE [b240] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $91ce                                      ; $0091B0 [671c] Bifurcación según la condición indicada por el mnemónico.
        move.w d0, d3                                    ; $0091B2 [3600] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        subq.w #$2, d3                                   ; $0091B4 [5543] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d3                                  ; $0091B6 [0243001f] Operación lógica o máscara de bits.
        cmp.b (a1, d3.w), d2                             ; $0091BA [b4313000] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $91ee                                      ; $0091BE [672e] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$0, (a1, d3.w)                           ; $0091C0 [0c3100003000] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.b $91ce                                      ; $0091C6 [6406] Bifurcación según la condición indicada por el mnemónico.
        subq.w #$2, d0                                   ; $0091C8 [5540] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d0                                  ; $0091CA [0240001f] Operación lógica o máscara de bits.
        clr.b $b8(a0)                                    ; $0091CE [422800b8] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b d2, (a1, d0.w)                            ; $0091D2 [13820000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.b $1(a1, d0.w)                               ; $0091D6 [42310001] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        addq.w #$2, d0                                   ; $0091DA [5440] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d0                                  ; $0091DC [0240001f] Operación lógica o máscara de bits.
        cmp.w d0, d1                                     ; $0091E0 [b240] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $9220                                      ; $0091E2 [663c] Bifurcación según la condición indicada por el mnemónico.
        move.w d0, d1                                    ; $0091E4 [3200] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addq.w #$2, d1                                   ; $0091E6 [5441] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d1                                  ; $0091E8 [0241001f] Operación lógica o máscara de bits.
        bra.b $9220                                      ; $0091EC [6032] Bifurcación según la condición indicada por el mnemónico.
        move.b $1(a1, d3.w), d2                          ; $0091EE [14313001] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addq.b #$1, d2                                   ; $0091F2 [5202] Operación aritmética de suma o resta sobre los operandos.
        bne.b $91fa                                      ; $0091F4 [6604] Bifurcación según la condición indicada por el mnemónico.
        move.b #$ff, d2                                  ; $0091F6 [143c00ff] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b d2, $1(a1, d3.w)                          ; $0091FA [13823001] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$1e, d2                                  ; $0091FE [0c02001e] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $9220                                      ; $009202 [651c] Bifurcación según la condición indicada por el mnemónico.
        move.w d0, d1                                    ; $009204 [3200] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        subq.w #$2, d1                                   ; $009206 [5541] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d1                                  ; $009208 [0241001f] Operación lógica o máscara de bits.
        bra.b $9220                                      ; $00920C [6012] Bifurcación según la condición indicada por el mnemónico.
        move.b $b8(a0), d2                               ; $00920E [142800b8] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addq.b #$1, d2                                   ; $009212 [5202] Operación aritmética de suma o resta sobre los operandos.
        move.b d2, $b8(a0)                               ; $009214 [114200b8] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$c, d2                                   ; $009218 [0c02000c] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $9220                                      ; $00921C [6502] Bifurcación según la condición indicada por el mnemónico.
        move.w d0, d1                                    ; $00921E [3200] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b d0, $b6(a0)                               ; $009220 [114000b6] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b d1, $b7(a0)                               ; $009224 [114100b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $009228 [4e75] Regresa usando la dirección de retorno de la pila.
        cmpi.b #$0, $59(a0)                              ; $00922A [0c2800000059] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $9256                                      ; $009230 [6724] Bifurcación según la condición indicada por el mnemónico.
        move.w d3, -(a7)                                 ; $009232 [3f03] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b d2, d3                                    ; $009234 [1602] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.w #$c, d3                                   ; $009236 [0243000c] Operación lógica o máscara de bits.
        beq.b $9254                                      ; $00923A [6718] Bifurcación según la condición indicada por el mnemónico.
        btst.b #$3, d2                                   ; $00923C [08020003] Comprueba el bit indicado y actualiza la condición de cero.
        beq.b $924c                                      ; $009240 [670a] Bifurcación según la condición indicada por el mnemónico.
        bset.b #$2, d2                                   ; $009242 [08c20002] Establece el bit indicado.
        bclr.b #$3, d2                                   ; $009246 [08820003] Borra el bit indicado.
        bra.b $9254                                      ; $00924A [6008] Bifurcación según la condición indicada por el mnemónico.
        bset.b #$3, d2                                   ; $00924C [08c20003] Establece el bit indicado.
        bclr.b #$2, d2                                   ; $009250 [08820002] Borra el bit indicado.
        move.w (a7)+, d3                                 ; $009254 [361f] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $009256 [4e75] Regresa usando la dirección de retorno de la pila.
        lea.l $e75e.w, a0                                ; $009258 [41f8e75e] Calcula una dirección y la deja en un registro de direcciones.
        bsr.w $9264                                      ; $00925C [61000006] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        lea.l $e886.w, a0                                ; $009260 [41f8e886] Calcula una dirección y la deja en un registro de direcciones.
        lea.l $93a8(pc), a1                              ; $009264 [43fa0142] Calcula una dirección y la deja en un registro de direcciones.
        bsr.w $937e                                      ; $009268 [61000114] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.b $ba(a0), d1                               ; $00926C [122800ba] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        btst.l d1, d0                                    ; $009270 [0300] Comprueba el bit indicado y actualiza la condición de cero.
        beq.b $9298                                      ; $009272 [6724] Bifurcación según la condición indicada por el mnemónico.
        bsr.w $939a                                      ; $009274 [61000124] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        tst.b $e73c.w                                    ; $009278 [4a38e73c] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $92b2                                      ; $00927C [6734] Bifurcación según la condición indicada por el mnemónico.
        cmpi.w #$2, $e9c4.w                              ; $00927E [0c780002e9c4] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $937c                                      ; $009284 [660000f6] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$d, $5b(a0)                              ; $009288 [0c28000d005b] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $937c                                      ; $00928E [670000ec] Bifurcación según la condición indicada por el mnemónico.
        lea.l $9471(pc), a1                              ; $009292 [43fa01dd] Calcula una dirección y la deja en un registro de direcciones.
        bra.b $92b2                                      ; $009296 [601a] Bifurcación según la condición indicada por el mnemónico.
        move.b $bb(a0), d1                               ; $009298 [122800bb] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        btst.l d1, d0                                    ; $00929C [0300] Comprueba el bit indicado y actualiza la condición de cero.
        beq.w $937c                                      ; $00929E [670000dc] Bifurcación según la condición indicada por el mnemónico.
        tst.b $e73c.w                                    ; $0092A2 [4a38e73c] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $937c                                      ; $0092A6 [660000d4] Bifurcación según la condición indicada por el mnemónico.
        bsr.w $939a                                      ; $0092AA [610000ee] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        lea.l $941a(pc), a1                              ; $0092AE [43fa016a] Calcula una dirección y la deja en un registro de direcciones.
        lea.l $94(a0), a2                                ; $0092B2 [45e80094] Calcula una dirección y la deja en un registro de direcciones.
        move.b $b6(a0), d0                               ; $0092B6 [102800b6] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.w #$1f, d0                                  ; $0092BA [0240001f] Operación lógica o máscara de bits.
        move.b (a2, d0.w), d1                            ; $0092BE [12320000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.b #$f, d1                                   ; $0092C2 [0201000f] Operación lógica o máscara de bits.
        move.b d1, (a2, d0.w)                            ; $0092C6 [15810000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        beq.b $92da                                      ; $0092CA [670e] Bifurcación según la condición indicada por el mnemónico.
        move.b d0, d2                                    ; $0092CC [1400] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        subq.b #$2, d2                                   ; $0092CE [5502] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d2                                  ; $0092D0 [0242001f] Operación lógica o máscara de bits.
        cmp.b (a2, d2.w), d1                             ; $0092D4 [b2322000] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $92e0                                      ; $0092D8 [6606] Bifurcación según la condición indicada por el mnemónico.
        subq.b #$2, d0                                   ; $0092DA [5500] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d0                                  ; $0092DC [0240001f] Operación lógica o máscara de bits.
        move.b $b7(a0), d1                               ; $0092E0 [122800b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        andi.w #$1f, d1                                  ; $0092E4 [0241001f] Operación lógica o máscara de bits.
        move.w d0, d2                                    ; $0092E8 [3400] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        sub.w d1, d2                                     ; $0092EA [9441] Operación aritmética de suma o resta sobre los operandos.
        bpl.b $92f2                                      ; $0092EC [6a04] Bifurcación según la condición indicada por el mnemónico.
        addi.w #$20, d2                                  ; $0092EE [06420020] Operación aritmética de suma o resta sobre los operandos.
        lsr.w #$1, d2                                    ; $0092F2 [e24a] Desplaza o rota bits según la operación indicada.
        beq.w $9376                                      ; $0092F4 [67000080] Bifurcación según la condición indicada por el mnemónico.
        subq.w #$2, d0                                   ; $0092F8 [5540] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d0                                  ; $0092FA [0240001f] Operación lógica o máscara de bits.
        move.b (a1)+, d3                                 ; $0092FE [1619] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        beq.b $9376                                      ; $009300 [6774] Bifurcación según la condición indicada por el mnemónico.
        cmp.b d3, d2                                     ; $009302 [b403] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $934c                                      ; $009304 [6546] Bifurcación según la condición indicada por el mnemónico.
        move.b d2, d5                                    ; $009306 [1a02] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w d0, d3                                    ; $009308 [3600] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b (a1)+, d4                                 ; $00930A [1819] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        beq.w $9354                                      ; $00930C [67000046] Bifurcación según la condición indicada por el mnemónico.
        tst.b d4                                         ; $009310 [4a04] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bmi.b $931e                                      ; $009312 [6b0a] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$c, $1(a2, d3.w)                         ; $009314 [0c32000c3001] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bls.b $9328                                      ; $00931A [630c] Bifurcación según la condición indicada por el mnemónico.
        bra.b $934c                                      ; $00931C [602e] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$1e, $1(a2, d3.w)                        ; $00931E [0c32001e3001] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $934c                                      ; $009324 [6526] Bifurcación según la condición indicada por el mnemónico.
        move.b (a1)+, d4                                 ; $009326 [1819] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.b (a2, d3.w), d4                             ; $009328 [b8323000] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $9342                                      ; $00932C [6714] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$4, $1(a2, d3.w)                         ; $00932E [0c3200043001] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.b $934c                                      ; $009334 [6416] Bifurcación según la condición indicada por el mnemónico.
        subq.w #$2, d3                                   ; $009336 [5543] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d3                                  ; $009338 [0243001f] Operación lógica o máscara de bits.
        subq.b #$1, d5                                   ; $00933C [5305] Operación aritmética de suma o resta sobre los operandos.
        bpl.b $9310                                      ; $00933E [6ad0] Bifurcación según la condición indicada por el mnemónico.
        bra.b $934c                                      ; $009340 [600a] Bifurcación según la condición indicada por el mnemónico.
        subq.w #$2, d3                                   ; $009342 [5543] Operación aritmética de suma o resta sobre los operandos.
        andi.w #$1f, d3                                  ; $009344 [0243001f] Operación lógica o máscara de bits.
        subq.b #$1, d5                                   ; $009348 [5305] Operación aritmética de suma o resta sobre los operandos.
        bpl.b $930a                                      ; $00934A [6abe] Bifurcación según la condición indicada por el mnemónico.
        tst.b (a1)+                                      ; $00934C [4a19] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $934c                                      ; $00934E [66fc] Bifurcación según la condición indicada por el mnemónico.
        addq.w #$1, a1                                   ; $009350 [5249] Operación aritmética de suma o resta sobre los operandos.
        bra.b $92fe                                      ; $009352 [60aa] Bifurcación según la condición indicada por el mnemónico.
        move.b (a1)+, d4                                 ; $009354 [1819] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$d, d4                                   ; $009356 [0c04000d] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $9362                                      ; $00935A [6706] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$14, d4                                  ; $00935C [0c040014] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.b $9372                                      ; $009360 [6610] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$4, $5b(a0)                              ; $009362 [0c280004005b] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $92fe                                      ; $009368 [6594] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$8, $5b(a0)                              ; $00936A [0c280008005b] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bhi.b $92fe                                      ; $009370 [628c] Bifurcación según la condición indicada por el mnemónico.
        move.b d4, $b9(a0)                               ; $009372 [114400b9] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $b6(a0), $b7(a0)                          ; $009376 [116800b600b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $00937C [4e75] Regresa usando la dirección de retorno de la pila.
        move.b $1d(a0), d0                               ; $00937E [1028001d] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $b5(a0), d1                               ; $009382 [122800b5] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        beq.b $9398                                      ; $009386 [6710] Bifurcación según la condición indicada por el mnemónico.
        move.b $1b(a0), d0                               ; $009388 [1028001b] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        btst.l d1, d0                                    ; $00938C [0300] Comprueba el bit indicado y actualiza la condición de cero.
        bne.b $9396                                      ; $00938E [6606] Bifurcación según la condición indicada por el mnemónico.
        clr.w d0                                         ; $009390 [4240] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        bset.b d1, d0                                    ; $009392 [03c0] Establece el bit indicado.
        bra.b $9398                                      ; $009394 [6002] Bifurcación según la condición indicada por el mnemónico.
        clr.w d0                                         ; $009396 [4240] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        rts                                              ; $009398 [4e75] Regresa usando la dirección de retorno de la pila.
        tst.b $b5(a0)                                    ; $00939A [4a2800b5] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $93a2                                      ; $00939E [6702] Bifurcación según la condición indicada por el mnemónico.
        clr.b d1                                         ; $0093A0 [4201] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b d1, $b5(a0)                               ; $0093A2 [114100b5] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $0093A6 [4e75] Regresa usando la dirección de retorno de la pila.

; Movimiento rápido original reutilizado por el parche. Los ensayos observan cruce sin daño ni activación de golpe; no confundirlo con un ataque que también cruce.
; Fuente: evidence/side-switch/native-summary.json
        org $01631C
cambio_lado_nativo:
        move.b $4(a0), $8000.w                           ; $01631C [11e800048000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $209dc.l                                     ; $016322 [4eb9000209dc] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.b d5, $4(a0)                                ; $016328 [11450004] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        tst.b $e9b7.w                                    ; $01632C [4a38e9b7] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $16352                                     ; $016330 [66000020] Bifurcación según la condición indicada por el mnemónico.
        move.b $8000.w, $4(a0)                           ; $016334 [117880000004] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b #$ff, $83(a0)                             ; $01633A [117c00ff0083] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b $59(a0), d0                               ; $016340 [10280059] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        eori.b #$1, d0                                   ; $016344 [0a000001] Operación lógica o máscara de bits.
        move.b d0, $59(a0)                               ; $016348 [11400059] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jmp $20cd6.l                                     ; $01634C [4ef900020cd6] Salta a otra dirección sin apilar un retorno nuevo.
        tst.w $42(a0)                                    ; $016352 [4a680042] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $163d8                                     ; $016356 [66000080] Bifurcación según la condición indicada por el mnemónico.
        jsr $1335c(pc)                                   ; $01635A [4ebad000] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.w #$1, $42(a0)                              ; $01635E [317c00010042] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b #$12, $83(a0)                             ; $016364 [117c00120083] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.b $84(a0)                                    ; $01636A [42280084] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b #$11, $85(a0)                             ; $01636E [117c00110085] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.b $86(a0)                                    ; $016374 [42280086] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b #$ff, $87(a0)                             ; $016378 [117c00ff0087] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$1, $59(a1)                              ; $01637E [0c2900010059] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $16398                                     ; $016384 [67000012] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $016388 [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        subi.w #$38, d0                                  ; $01638C [04400038] Operación aritmética de suma o resta sobre los operandos.
        bmi.w $163c0                                     ; $016390 [6b00002e] Bifurcación según la condición indicada por el mnemónico.
        bra.w $163aa                                     ; $016394 [60000014] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $016398 [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addi.w #$38, d0                                  ; $01639C [06400038] Operación aritmética de suma o resta sobre los operandos.
        move.w $e722.w, d1                               ; $0163A0 [3238e722] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.w d1, d0                                     ; $0163A4 [b041] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $163c0                                     ; $0163A6 [64000018] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a0), d0                                ; $0163AA [3028000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.w $a(a1), d0                                 ; $0163AE [b069000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $163d2                                     ; $0163B2 [6400001e] Bifurcación según la condición indicada por el mnemónico.
        move.b #$1, $42(a0)                              ; $0163B6 [117c00010042] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        bra.w $163d8                                     ; $0163BC [6000001a] Bifurcación según la condición indicada por el mnemónico.
        move.b $8000.w, $4(a0)                           ; $0163C0 [117880000004] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.b #$ff, $83(a0)                             ; $0163C6 [117c00ff0083] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jmp $20cd6.l                                     ; $0163CC [4ef900020cd6] Salta a otra dirección sin apilar un retorno nuevo.
        move.b #$0, $42(a0)                              ; $0163D2 [117c00000042] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$0, d0                                   ; $0163D8 [303c0000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        lea.l $164ea(pc), a1                             ; $0163DC [43fa010c] Calcula una dirección y la deja en un registro de direcciones.
        nop                                              ; $0163E0 [4e71] Instrucción sin efecto lógico previsto.
        lea.l $164eb(pc), a2                             ; $0163E2 [45fa0107] Calcula una dirección y la deja en un registro de direcciones.
        nop                                              ; $0163E6 [4e71] Instrucción sin efecto lógico previsto.
        lea.l $164ec(pc), a3                             ; $0163E8 [47fa0102] Calcula una dirección y la deja en un registro de direcciones.
        nop                                              ; $0163EC [4e71] Instrucción sin efecto lógico previsto.
        jsr $1985c(pc)                                   ; $0163EE [4eba346c] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        nop                                              ; $0163F2 [4e71] Instrucción sin efecto lógico previsto.
        move.b $e9b7.w, d4                               ; $0163F4 [1838e9b7] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$80, d4                                  ; $0163F8 [0c040080] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        tst.w $3a(a0)                                    ; $0163FC [4a68003a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $1640a                                     ; $016400 [66000008] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a0), $3a(a0)                           ; $016404 [3168000a003a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w $6(a0), $800c.w                           ; $01640A [31e80006800c] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$190, $8002.w                            ; $016410 [31fc01908002] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$1, $8006.w                              ; $016416 [31fc00018006] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $13b84(pc)                                   ; $01641C [4ebad766] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.w $800c.w, d0                               ; $016420 [3038800c] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.w $6(a0), d0                                 ; $016424 [b0680006] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $164e8                                     ; $016428 [660000be] Bifurcación según la condición indicada por el mnemónico.
        jsr $1335c(pc)                                   ; $01642C [4ebacf2e] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.b $42(a0), d0                               ; $016430 [10280042] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.b $59(a0), d0                                ; $016434 [b0280059] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bne.w $164b4                                     ; $016438 [6600007a] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a0), d0                                ; $01643C [3028000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w $a(a1), d1                                ; $016440 [3229000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        sub.w d1, d0                                     ; $016444 [9041] Operación aritmética de suma o resta sobre los operandos.
        bpl.w $1644c                                     ; $016446 [6a000004] Bifurcación según la condición indicada por el mnemónico.
        neg.w d0                                         ; $01644A [4440] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        cmpi.w #$38, d0                                  ; $01644C [0c400038] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $16460                                     ; $016450 [6400000e] Bifurcación según la condición indicada por el mnemónico.
        move.b #$ff, $83(a0)                             ; $016454 [117c00ff0083] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jmp $20cd6.l                                     ; $01645A [4ef900020cd6] Salta a otra dirección sin apilar un retorno nuevo.
        cmpi.b #$1, $42(a0)                              ; $016460 [0c2800010042] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $16490                                     ; $016466 [67000028] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $01646A [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.w $a(a0), d0                                 ; $01646E [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $1647c                                     ; $016472 [64000008] Bifurcación según la condición indicada por el mnemónico.
        jmp $20cd6.l                                     ; $016476 [4ef900020cd6] Salta a otra dirección sin apilar un retorno nuevo.
        subi.w #$38, d0                                  ; $01647C [04400038] Operación aritmética de suma o resta sobre los operandos.
        cmp.w $a(a0), d0                                 ; $016480 [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $164e8                                     ; $016484 [64000062] Bifurcación según la condición indicada por el mnemónico.
        addq.w #$1, $6(a0)                               ; $016488 [52680006] Operación aritmética de suma o resta sobre los operandos.
        bra.w $164e8                                     ; $01648C [6000005a] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $016490 [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmp.w $a(a0), d0                                 ; $016494 [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.w $164a2                                     ; $016498 [65000008] Bifurcación según la condición indicada por el mnemónico.
        jmp $20cd6.l                                     ; $01649C [4ef900020cd6] Salta a otra dirección sin apilar un retorno nuevo.
        addi.w #$38, d0                                  ; $0164A2 [06400038] Operación aritmética de suma o resta sobre los operandos.
        cmp.w $a(a0), d0                                 ; $0164A6 [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.w $164e8                                     ; $0164AA [6500003c] Bifurcación según la condición indicada por el mnemónico.
        addq.w #$1, $6(a0)                               ; $0164AE [52680006] Operación aritmética de suma o resta sobre los operandos.
        bra.b $164e8                                     ; $0164B2 [6034] Bifurcación según la condición indicada por el mnemónico.
        cmpi.b #$1, $42(a0)                              ; $0164B4 [0c2800010042] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.w $164d4                                     ; $0164BA [67000018] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $0164BE [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        subi.w #$38, d0                                  ; $0164C2 [04400038] Operación aritmética de suma o resta sobre los operandos.
        cmp.w $a(a0), d0                                 ; $0164C6 [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.w $164e8                                     ; $0164CA [6500001c] Bifurcación según la condición indicada por el mnemónico.
        addq.w #$1, $6(a0)                               ; $0164CE [52680006] Operación aritmética de suma o resta sobre los operandos.
        bra.b $164e8                                     ; $0164D2 [6014] Bifurcación según la condición indicada por el mnemónico.
        move.w $a(a1), d0                                ; $0164D4 [3029000a] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addi.w #$38, d0                                  ; $0164D8 [06400038] Operación aritmética de suma o resta sobre los operandos.
        cmp.w $a(a0), d0                                 ; $0164DC [b068000a] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcc.w $164e8                                     ; $0164E0 [64000006] Bifurcación según la condición indicada por el mnemónico.
        addq.w #$1, $6(a0)                               ; $0164E4 [52680006] Operación aritmética de suma o resta sobre los operandos.
        rts                                              ; $0164E8 [4e75] Regresa usando la dirección de retorno de la pila.

; Selecciona programa/acción y reinicia campos de animación y estado. La entrada 20B7E modifica el retorno en la pila: no es una función normal intercambiable con cualquier JSR.
; Fuente: evidence/side-switch/native-summary.json y src/gameplay/v3/side.asm
        org $020B7A
cambio_y_reinicio_estado:
        cmp.w (a0), d0                                   ; $020B7A [b050] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        beq.b $20b9e                                     ; $020B7C [6720] Bifurcación según la condición indicada por el mnemónico.
        move.b d1, $5b(a0)                               ; $020B7E [1141005b] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        cmpi.b #$20, d1                                  ; $020B82 [0c010020] Actualiza las condiciones para comprobar valores; no sustituye el operando comparado.
        bcs.b $20b96                                     ; $020B86 [650e] Bifurcación según la condición indicada por el mnemónico.
        move.w d0, -(a7)                                 ; $020B88 [3f00] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$20, d0                                  ; $020B8A [303c0020] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $1318a.l                                     ; $020B8E [4eb90001318a] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.w (a7)+, d0                                 ; $020B94 [301f] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        bsr.w $20ba0                                     ; $020B96 [61000008] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.w d0, (a0)                                  ; $020B9A [3080] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        addq.w #$4, a7                                   ; $020B9C [584f] Operación aritmética de suma o resta sobre los operandos.
        rts                                              ; $020B9E [4e75] Regresa usando la dirección de retorno de la pila.
        move.w d0, -(a7)                                 ; $020BA0 [3f00] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$8003, d0                                ; $020BA2 [303c8003] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $1319a.l                                     ; $020BA6 [4eb90001319a] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        move.w #$1400, d0                                ; $020BAC [303c1400] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $131ae.l                                     ; $020BB0 [4eb9000131ae] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        clr.w $6(a0)                                     ; $020BB6 [42680006] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.b $5a(a0)                                    ; $020BBA [4228005a] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $3a(a0)                                    ; $020BBE [4268003a] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $e(a0)                                     ; $020BC2 [4268000e] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $14(a0)                                    ; $020BC6 [42680014] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $40(a0)                                    ; $020BCA [42680040] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.w $42(a0)                                    ; $020BCE [42680042] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.b $bd(a0)                                    ; $020BD2 [422800bd] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        clr.b $c8(a0)                                    ; $020BD6 [422800c8] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.b #$ff, $83(a0)                             ; $020BDA [117c00ff0083] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        clr.b $cb(a0)                                    ; $020BE0 [422800cb] Transforma el operando: borrar, negar, extender signo o intercambiar mitades.
        move.w (a7)+, d0                                 ; $020BE4 [301f] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $020BE6 [4e75] Regresa usando la dirección de retorno de la pila.
