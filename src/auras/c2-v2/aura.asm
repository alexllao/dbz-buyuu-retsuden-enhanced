; Assemble at 0x7B400. Replace 0x9ECE..0x9ED3 with JMP aura_entry.
; Original caller invokes each fighter approximately every other display frame.
; New PROVISIONAL per-actor state: 110 magic,111 phase,112 last frame,114 last HP.
; 116..117 stay untouched. Existing controls108..10F and native118+ stay untouched.
; Native BD flag is read only: retaining it would suppress the ground shadow.
; C2 v2: eight animation frames; each frame has plain100/75/50/25,
; then bolts100/75/50/25. Dust and intermittent long bolts belong in maps.
; Builder must fill 128 longword pointers (512 bytes) at aura_map_table.
; First64 maps include ground dust, second64 maps omit dust.
; Dust is selected only at known physical ground Y=0x1C0 (camera independent).
; Frame index=((engine counter >> 2)&7); pointer offset=frame*32+bolts*16+scale*4.
; Timer, actor RAM and native return behavior match the tested v1 hook.

aura_entry:
 cmpi.b #0xc2,(0x110,A0)
 beq.w @aura_initialized
 move.b #0xc2,(0x110,A0)
 clr.b (0x111,A0)
 move.w (0xffffe6a8).w,(0x112,A0)
 move.w (0x24,A0),(0x114,A0)
aura_initialized:
 move.w (0x24,A0),D0
 cmp.w (0x114,A0),D0
 bcs.w @aura_hit_cancel
 move.w D0,(0x114,A0)
 move.w (0xffffe6a8).w,D2
 move.w D2,D4
 sub.w (0x112,A0),D4
 move.w D2,(0x112,A0)
 cmpi.w #0x10,D4
 bcs.w @aura_elapsed_valid
 clr.b (0x111,A0)
 moveq #0,D4
aura_elapsed_valid:
 tst.b (0xbd,A0)
 beq.w @aura_inactive
 cmpi.b #0x0f,(0x5b,A0)
 bne.w @aura_sustain
 ; Same charge bindings as original handler at 0x1A692.
 move.w (0x1a,A0),D0
 moveq #0,D1
 move.b (0xba,A0),D1
 btst.l D1,D0
 beq.w @aura_release
 move.b (0xbb,A0),D1
 btst.l D1,D0
 beq.w @aura_release
aura_sustain:
 move.b #0x80,(0x111,A0)
 moveq #0,D5
 bra.w @aura_draw
aura_inactive:
 ; Residual is only permitted during idle or native charge recovery.
 move.b (0x5b,A0),D0
 beq.w @aura_release
 cmpi.b #0x0f,D0
 bne.w @aura_cancel
aura_release:
 cmpi.b #0x80,(0x111,A0)
 bne.w @aura_countdown
 move.b #0x0c,(0x111,A0)
 moveq #0,D5
 bra.w @aura_draw
aura_countdown:
 moveq #0,D0
 move.b (0x111,A0),D0
 beq.w @aura_return
 sub.w D4,D0
 ble.w @aura_cancel
 move.b D0,(0x111,A0)
 moveq #0,D5
 cmpi.w #0x0a,D0
 bcc.w @aura_draw
 moveq #1,D5
 cmpi.w #0x07,D0
 bcc.w @aura_draw
 moveq #2,D5
 cmpi.w #0x04,D0
 bcc.w @aura_draw
 moveq #3,D5
aura_draw:
 ; D5 holds scale index0..3, converted to longword byte offset.
 lsl.w #0x2,D5
 cmpi.b #0x01,(0x58,A0)
 beq.w @aura_bolts
 cmpi.b #0x05,(0x58,A0)
 bne.w @aura_animation
aura_bolts:
 addi.w #0x10,D5
aura_animation:
 move.w (0xffffe6a8).w,D6
 ; Counter bits2..4 become frame byte offsets0,32,...,224.
 andi.w #0x1c,D6
 lsl.w #0x3,D6
 add.w D6,D5
 ; Native jump changes worldY without changing the depth-plane bit.
 ; Known ground is worldY0x1C0; all other heights use no-dust maps.
 cmpi.w #0x01c0,(0x10,A0)
 beq.w @aura_ground_map
 addi.w #0x0100,D5
aura_ground_map:
 ; Recreate native screen coordinates, including native Y bias.
 move.w (0x0a,A0),D0
 sub.w (0x16,A0),D0
 move.w (0x10,A0),D1
 sub.w (0x18,A0),D1
 addi.w #0x20,D1
 lea (@aura_map_table).l,A1
 adda.w D5,A1
 movea.l (A1),A0
 jsr 0x00001c66.l
 bra.w @aura_return
aura_hit_cancel:
 move.w D0,(0x114,A0)
aura_cancel:
 clr.b (0x111,A0)
aura_return:
 jmp 0x00009f08.l
aura_map_table:
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000
 .hex 00000000000000000000000000000000

