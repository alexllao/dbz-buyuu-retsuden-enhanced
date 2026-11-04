; Buyuu Retsuden control prototype. Stored in original FF padding at 0x7B000.
; Per-player reserved tail 0x108..0x10F: magic, TTL, mask, previous action,
; recovery-shortened latch, remaining animation units, settle count, settle pose.

input_entry:
 tst.b (0xffffe744).w
 bne.w @input_body
 jsr 0x00009066.l
 bcs.w @input_blocked
input_body:
 jsr 0x00008f68.l
 .hex 48e7fffe
 .hex 40e7
 tst.b (0xffffe744).w
 bne.w @input_done
 lea (0xffffe75e).w,A0
 jsr @actor_input.l
 lea (0xffffe886).w,A0
 jsr @actor_input.l
input_done:
 .hex 46df
 .hex 4cdf7fff
 rts
input_blocked:
 jmp 0x00009054.l

actor_input:
 tst.b (0xbe,A0)
 bne.w @actor_cpu
 cmpi.b #0xc7,(0x108,A0)
 beq.w @actor_initialized
 clr.l (0x108,A0)
 clr.l (0x10c,A0)
 move.b #0xc7,(0x108,A0)
actor_initialized:
 moveq #0,D0
 moveq #0,D1
 move.b (0x5b,A0),D0
 move.b (0x10b,A0),D1
 cmp.b D1,D0
 beq.w @actor_same_action
 clr.b (0x10c,A0)
 move.b D0,(0x10b,A0)
 tst.b D0
 bne.w @actor_new_nonidle
 cmpi.b #0x20,D1
 bcs.w @actor_same_action
 cmpi.b #0x27,D1
 bhi.w @actor_same_action
 btst.b #0x4,(0x1e,A0)
 bne.w @actor_same_action
 move.b (0x4,A0),(0x10f,A0)
 move.b #0x02,(0x10e,A0)
 bra.w @actor_same_action
actor_new_nonidle:
 clr.b (0x10e,A0)
 cmpi.b #0x20,D0
 bcs.w @clear_queue_new_action
 cmpi.b #0x27,D0
 bls.w @actor_same_action
clear_queue_new_action:
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
actor_same_action:
 tst.b (0x109,A0)
 beq.w @actor_queue_aged
 subq.b #0x1,(0x109,A0)
 bne.w @actor_queue_aged
 clr.b (0x10a,A0)
actor_queue_aged:
 tst.b D0
 bne.w @actor_not_idle
 tst.b (0x109,A0)
 beq.w @actor_return
 move.b (0x10a,A0),D1
 or.b D1,(0x1a,A0)
 or.b D1,(0x1b,A0)
 or.b D1,(0x1c,A0)
 or.b D1,(0x1d,A0)
 clr.b (0x109,A0)
 clr.b (0x10a,A0)
 rts
actor_not_idle:
 cmpi.b #0x1,D0
 beq.w @actor_walking
 cmpi.b #0x2,D0
 beq.w @actor_walking
 cmpi.b #0x20,D0
 bcs.w @actor_return
 cmpi.b #0x27,D0
 bhi.w @actor_return
 btst.b #0x4,(0x1e,A0)
 bne.w @actor_return
 ; Record an edge for five updates. Early inputs expire before guard;
 ; only an edge close enough to the end survives to be replayed.
 moveq #0,D1
 moveq #0,D2
 move.b (0xba,A0),D2
 bset.l D2,D1
 move.b (0xbb,A0),D2
 bset.l D2,D1
 move.b (0x1d,A0),D2
 and.b D1,D2
 beq.w @actor_return
 move.b D2,D3
 subq.b #0x1,D3
 and.b D2,D3
 bne.w @actor_return
 move.b D2,(0x10a,A0)
 move.b #0x06,(0x109,A0)
actor_return:
 rts
actor_cpu:
 cmpi.b #0xc7,(0x108,A0)
 bne.w @actor_return
 clr.l (0x108,A0)
 clr.l (0x10c,A0)
 rts

actor_walking:
 ; Keep native walking, double-tap dash and release inertia.
 rts

animation_entry:
 .hex 48e70060
 jsr 0x00020a4c.l
 .hex 48e7fffe
 .hex 40e7
 jsr @animation_recovery.l
 .hex 46df
 .hex 4cdf7fff
 jmp 0x000209e4.l

animation_recovery:
 cmpa.l #0xffffe75e,A0
 beq.w @animation_actor_valid
 cmpa.l #0xffffe886,A0
 bne.w @animation_return
animation_actor_valid:
 cmpi.b #0xc7,(0x108,A0)
 bne.w @animation_return
 tst.b (0xbe,A0)
 bne.w @animation_return
 move.w D1,D7
 mulu.w D2w,D7
 move.b (0x5b,A0),D1
 cmpi.b #0x20,D1
 bcs.w @animation_clear_remaining
 cmpi.b #0x27,D1
 bhi.w @animation_clear_remaining
 btst.b #0x4,(0x1e,A0)
 bne.w @animation_clear_remaining
 move.w D7,D1
 sub.w (0x6,A0),D1
 bls.w @animation_clear_remaining
 cmpi.w #0xff,D1
 bhi.w @animation_clear_remaining
 move.b D1,(0x10d,A0)
 cmpi.w #0x03,D1
 bne.w @animation_return
 tst.b (0x10c,A0)
 bne.w @animation_return
 tst.w (0x6,A0)
 beq.w @animation_return
 movea.l A1,A3
 moveq #0,D4
animation_scan_phase:
 move.b (A3)+,D6
 beq.w @animation_last_phase
 bmi.w @animation_return
 addq.w #0x1,D4
 cmpi.w #0x08,D4
 bhi.w @animation_return
 bra.w @animation_scan_phase
animation_last_phase:
 cmpi.w #0x02,D4
 bcs.w @animation_return
 subq.w #0x1,D4
 adda.w D4,A2
 move.b (A2),D6
 cmp.b (0x4,A0),D6
 bne.w @animation_return
 addq.w #0x2,(0x6,A0)
 move.b #0x1,(0x10c,A0)
 move.b #0x1,(0x10d,A0)
animation_return:
 rts
animation_clear_remaining:
 clr.b (0x10d,A0)
 rts

animation_exit:
 .hex 4cdf0600
 .hex 48e7fbfe
 .hex 40e7
 jsr @animation_settle.l
 .hex 46df
 .hex 4cdf7fdf
 rts

animation_settle:
 cmpa.l #0xffffe75e,A0
 beq.w @settle_actor_valid
 cmpa.l #0xffffe886,A0
 bne.w @settle_return
settle_actor_valid:
 cmpi.b #0xc7,(0x108,A0)
 bne.w @settle_return
 tst.b (0xbe,A0)
 bne.w @settle_cancel
 tst.b (0x5b,A0)
 bne.w @settle_cancel
 btst.b #0x4,(0x1e,A0)
 bne.w @settle_cancel
 tst.b (0x10e,A0)
 beq.w @settle_return
 subq.b #0x1,(0x10e,A0)
 beq.w @settle_neutral_pose
 moveq #0,D5
 move.b (0x10f,A0),D5
 rts
settle_neutral_pose:
 moveq #0x02,D5
settle_return:
 rts
settle_cancel:
 clr.b (0x10e,A0)
 rts
