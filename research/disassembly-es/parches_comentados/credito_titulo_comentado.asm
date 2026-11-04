; Ayuda propia del título: carga los glifos añadidos y reproduce la inicialización desplazada.
; El mapa y los dibujos de las letras son datos separados, no instrucciones.
; Este extracto corresponde a los bytes del registro consultado, no al fuente del juego.
        org $3F0500
cargar_credito_titulo:
        movem.l d0-d7/a0-a6, -(a7)                       ; $3F0500 [48e7fffe] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        lea.l $3f0000.l, a0                              ; $3F0504 [41f9003f0000] Calcula una dirección y la deja en un registro de direcciones.
        movea.w #$d000, a1                               ; $3F050A [327cd000] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        jsr $15d2.l                                      ; $3F050E [4eb9000015d2] Llama a la rutina indicada; revisar aparte las ayudas que modifican el retorno.
        movem.l (a7)+, d0-d7/a0-a6                       ; $3F0514 [4cdf7fff] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        move.w #$50, $e9e6.w                             ; $3F0518 [31fc0050e9e6] Transfiere valores entre los operandos; el sufijo indica el tamaño.
        rts                                              ; $3F051E [4e75] Regresa usando la dirección de retorno de la pila.
