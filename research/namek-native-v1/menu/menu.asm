; Escenarios adicionales: indice virtual9..11 solo en el selector.
; E741 conserva un escenario fisico0..8: las variantes usan el motor de Namek6.
; F7C0:0=original,1=Namek nuevo,2=aldea,3=Porunga.
variant_index:
 clr.l D0
 cmpi.b #6,(0xffffe741).w
 bne.w @no_variant
 move.b (0xfffff7c0).w,D0
 cmpi.w #3,D0
 bls.w @variant_done
no_variant:
 clr.b (0xfffff7c0).w
 clr.w D0
variant_done:
 tst.w D0
 rts

get_selection:
 bsr.w @variant_index
 beq.w @selection_original
 addi.w #8,D0
 rts
selection_original:
 move.b (0xffffe741).w,D0
 rts

commit_selection:
 clr.b (0xfffff7c0).w
 cmpi.w #9,D0
 bcs.w @commit_original
 subi.w #8,D0
 move.b D0,(0xfffff7c0).w
 move.b #6,(0xffffe741).w
 rts
commit_original:
 move.b D0,(0xffffe741).w
 rts

select_previous:
 bsr.w @get_selection
 subq.w #1,D0
 bpl.w @previous_ready
 moveq #11,D0
previous_ready:
 bsr.w @commit_selection
 jmp 0x3a948.l

select_next:
 bsr.w @get_selection
 addq.w #1,D0
 cmpi.w #12,D0
 bcs.w @next_ready
 clr.w D0
next_ready:
 bsr.w @commit_selection
 jmp 0x3aa04.l

; Limpia la variante al iniciar una seleccion de personajes nueva.
; Reproduce exactamente la llamada nativa desplazada.
character_select_tick:
 jsr 0x72e.l
 tst.w (0xffffe750).w
 bne.w @character_select_done
 clr.b (0xfffff7c0).w
character_select_done:
 rts

; Devuelve A0 con los graficos comprimidos; D0 se conserva como en el original.
load_graphics:
 move.l D0,-(SP)
 bsr.w @variant_index
 beq.w @graphics_original
 subq.w #1,D0
 swap D0
 movea.l #0x300000,A0
 adda.l D0,A0
 bra.w @graphics_done
graphics_original:
 move.b (0xffffe741).w,D0
 add.w D0,D0
 add.w D0,D0
 movea.l #0x1769ca,A0
 adda.w D0,A0
 movea.l (A0),A0
graphics_done:
 move.l (SP)+,D0
 rts

; Mantiene los diez colores compartidos del HUD y efectos sin tocarlos.
load_palette:
 bsr.w @variant_index
 beq.w @palette_original
 subq.w #1,D0
 swap D0
 movea.l #0x309100,A0
 adda.l D0,A0
 jmp 0x90e0.l
palette_original:
 move.b (0xffffe741).w,D0
 jmp 0x90d0.l

; A0 apunta a la lista de tres franjas de512 px. El indice fisico sigue siendo6.
lookup_map:
 move.l D0,-(SP)
 bsr.w @variant_index
 beq.w @map_original
 subq.w #1,D0
 lsl.w #4,D0
 movea.l #0x332000,A0
 adda.w D0,A0
 bra.w @map_done
map_original:
 move.b (0xffffe741).w,D0
 add.w D0,D0
 movea.l #0x18c168,A0
 adda.w D0,A0
 adda.w (A0),A0
map_done:
 move.l (SP)+,D0
 rts

load_map:
 bsr.w @lookup_map
 rts

load_map_a1:
 bsr.w @lookup_map
 movea.l A0,A1
 jmp 0xa3fa.l

load_map_menu:
 bsr.w @lookup_map
 jmp 0x369bc.l

; Rotulos propios en el espacio de fuente ya reservado por el selector nativo.
; No se amplian tablas de escenarios originales ni se reutiliza el ID9 de destruccion.
draw_stage_label:
 jsr 0x1fe6.l
 bsr.w @variant_index
 beq.w @label_original
 subq.w #1,D0
 mulu.w #0x300,D0
 movea.l #0x331000,A0
 adda.l D0,A0
 movea.l #0x9c00,A1
 move.w #0x300,D0
 jsr 0x1780.l
 bsr.w @variant_index
 subq.w #1,D0
 lsl.w #3,D0
 movea.l #0x332100,A0
 adda.w D0,A0
 move.w #0xe4e0,D4
 move.w #0xd59e,D0
 jsr 0x3aee4.l
 rts
label_original:
 jmp 0x3ac2a.l

; Cuando la historia asigna un escenario desde sus tablas, elimina la variante
; anterior. No altera las transiciones ni los escenarios de la historia.
assign_story_stage:
 move.b (A0),D0
 clr.b (0xfffff7c0).w
 move.b D0,(0xffffe741).w
 rts
